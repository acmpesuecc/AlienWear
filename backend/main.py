from fastapi import FastAPI, Request, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI
from pinecone import Pinecone
import google.generativeai as genai
from bs4 import BeautifulSoup
from PIL import Image
from dotenv import load_dotenv, dotenv_values
import requests, json, io, base64, re

app = FastAPI(title="AlienWear Backend")

load_dotenv()
env_var = dotenv_values(".env")

pineconeKey = env_var.get("PINECONE_API_KEY")
openAiApiKey = env_var.get("OPENAI_API_KEY")
geminiApiKey = env_var.get("GEMINI_API_KEY")

pc = Pinecone(api_key=pineconeKey)
openAiClient = OpenAI(api_key=openAiApiKey)
genai.configure(api_key=geminiApiKey)

model = genai.GenerativeModel("gemini-pro")
index = pc.Index("alien-wear-threehundred")

app = FastAPI(title="AlienWear Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_embedding(query, model="text-embedding-3-small"):
    return openAiClient.embeddings.create(input=[query], model=model).data[0].embedding


def get_image_link(url):
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5)"
            " AppleWebKit/537.36 (KHTML, like Gecko)"
            " Chrome/84.0.4147.89 Safari/537.36"
        )
    }
    try:
        res = requests.get(url, headers=headers, verify=False)
        soup = BeautifulSoup(res.text, "lxml")
        script = next((s.get_text(strip=True) for s in soup.find_all("script") if "pdpData" in s.text), None)
        if not script:
            return None
        json_data = json.loads(script[script.index("{"):])
        return json_data["pdpData"]["media"]["albums"][0]["images"][0]["imageURL"]
    except Exception as e:
        print(f"Error fetching image for URL {url}: {e}")
        return None


def process_products(product_info, original_query):
    response = model.generate_content(
        f"For the Query: {original_query}\n\n{product_info}\n"
        "Filter and return the top 6 Product IDs as space-separated values."
    )
    return response.text.split()


def find_product_info(product_id, data):
    for item in data:
        if item["Product_id"] == product_id:
            return {
                "Product_id": item.get("Product_id", ""),
                "DiscountPrice (in Rs)": item.get("DiscountPrice (in Rs)", ""),
                "OriginalPrice (in Rs)": item.get("OriginalPrice (in Rs)", ""),
                "DiscountOffer": item.get("DiscountOffer", ""),
                "URL": item.get("URL", ""),
                "Description": item.get("Description", ""),
            }
    return None


def normalize_product_info(product_info):
    if not product_info.get("DiscountPrice (in Rs)") or not product_info.get("DiscountOffer"):
        product_info.pop("DiscountPrice (in Rs)", None)
        product_info.pop("DiscountOffer", None)
        product_info["Price"] = int(product_info.pop("OriginalPrice (in Rs)", 0))
    else:
        product_info["Price"] = int(product_info.pop("DiscountPrice (in Rs)", 0))
        product_info.pop("OriginalPrice (in Rs)", None)
        product_info.pop("DiscountOffer", None)
    return product_info


@app.get("/occasion")
def process_occasion(query: str = Query(...)):
    query_embed = get_embedding(query)
    similar = index.query(namespace="ns1", vector=query_embed, top_k=30, include_metadata=True)

    with open("../data/OGMyntraFasionClothing.json", "r") as f:
        data = json.load(f)

    items = []
    for result in similar["matches"]:
        product = find_product_info(result["id"], data)
        if not product:
            continue
        product = normalize_product_info(product)
        product.update(result["metadata"])
        product["Product_id"] = result["id"]
        items.append(product)

    top_ids = process_products(items, query)
    final_results = []
    for pid in top_ids:
        product = find_product_info(pid, data)
        if not product:
            continue
        product = normalize_product_info(product)
        product["ImageURL"] = get_image_link(product["URL"])
        final_results.append(product)

    return {"response": final_results}


class ChatMessage(BaseModel):
    message: str


chat = model.start_chat(history=[])


@app.post("/chat")
def chatbot_response(body: ChatMessage):
    response = chat.send_message(body.message, stream=False)
    return {"message": response.text}


@app.get("/chat")
def chat_recommendations():
    history = str(chat.history)
    matches = re.findall(r'parts\s*{\s*text:\s*"([^"]+)"\s*}', history)
    if not matches:
        return {"response": []}

    last_text = matches[-1]
    query_embed = get_embedding(last_text)
    similar = index.query(namespace="ns1", vector=query_embed, top_k=20, include_metadata=True)

    with open("../data/OGMyntraFasionClothing.json", "r") as f:
        data = json.load(f)

    results = []
    for result in similar["matches"]:
        product = find_product_info(result["id"], data)
        if not product:
            continue
        product = normalize_product_info(product)
        product["ImageURL"] = get_image_link(product["URL"])
        product.pop("URL", None)
        results.append(product)

    return {"response": results}


class ImageRequest(BaseModel):
    imgURI: str
    text: str = ""


@app.post("/imagecapture")
def process_image(body: ImageRequest):
    img_data = body.imgURI[23:]
    decoded = io.BytesIO(base64.b64decode(img_data))
    img = Image.open(decoded)

    model_vision = genai.GenerativeModel("gemini-pro-vision")
    prompt = [body.text, img]
    description = model_vision.generate_content(prompt).text
    query_embed = get_embedding(description)

    similar = index.query(namespace="ns1", vector=query_embed, top_k=20, include_metadata=True)
    with open("../data/OGMyntraFasionClothing.json", "r") as f:
        data = json.load(f)

    results = []
    for result in similar["matches"]:
        product = find_product_info(result["id"], data)
        if not product:
            continue
        product = normalize_product_info(product)
        product["ImageURL"] = get_image_link(product["URL"])
        product.pop("URL", None)
        results.append(product)

    return {"response": results}


@app.get("/")
def home():
    return {"message": "AlienWear FastAPI backend running"}
