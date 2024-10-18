from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
from pinecone import Pinecone
import google.generativeai as genai
from bs4 import BeautifulSoup
import requests
import json
import base64
from PIL import Image
import io
from dotenv import load_dotenv, dotenv_values


load_dotenv()

# Environment Variables
env_var = dotenv_values('.env')
pineconeKey = env_var.get("PINECONE_API_KEY")
openAiApiKey = env_var.get('OPENAI_API_KEY')
geminiApiKey = env_var.get('GEMINI_API_KEY')

# Initialize Clients
pc = Pinecone(api_key=pineconeKey)
openAiClient = OpenAI(api_key=openAiApiKey)
geminiClient = genai.configure(api_key=geminiApiKey)

# Model selection
model = genai.GenerativeModel('gemini-pro')

index_name = "alien-wear-threehundred"
index = pc.Index(index_name)

# FastAPI app setup
app = FastAPI()

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Helper Functions
def get_embedding(query, model="text-embedding-3-small"):
    return openAiClient.embeddings.create(input=[query], model=model).data[0].embedding


def get_image_link(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'
    }
    try:
        res = requests.get(url, headers=headers, verify=False)
        soup = BeautifulSoup(res.text, "lxml")
        script = None
        for s in soup.find_all("script"):
            if 'pdpData' in s.text:
                script = s.get_text(strip=True)
                break
        json_data = json.loads(script[script.index('{'):])
        image_link = json_data["pdpData"]["media"]["albums"][0]["images"][0]["imageURL"]
        return image_link
    except Exception as e:
        print(f"Error fetching image for URL {url}: {e}")
        return None


def find_product_info(product_id, data):
    for item in data:
        if item["Product_id"] == product_id:
            return {
                "Product_id": item.get("Product_id", ""),
                "DiscountPrice (in Rs)": item.get("DiscountPrice (in Rs)", ""),
                "OriginalPrice (in Rs)": item.get("OriginalPrice (in Rs)", ""),
                "DiscountOffer": item.get("DiscountOffer", ""),
                "URL": item.get("URL", ""),
                "Description": item.get("Description", "")
            }
    return None


def serializer(obj):
    if hasattr(obj, "__dict__"):
        return obj.__dict__
    return str(obj)


# Models for API Requests/Responses
class ChatRequest(BaseModel):
    message: str


class ImageCaptureRequest(BaseModel):
    imgURI: str
    text: str


# FastAPI Routes
@app.get('/occasion')
async def process_occasion(query: str):
    if query:
        queryEmbed = get_embedding(query)
        similarVectors = index.query(
            namespace="ns1",
            vector=queryEmbed,
            top_k=30,
            include_values=False,
            include_metadata=True
        )

        lst = []
        with open('../data/OGMyntraFasionClothing.json', 'r') as read_file:
            data = json.load(read_file)
            for result in similarVectors['matches']:
                product_id_to_find = result['id']
                product_info = find_product_info(product_id_to_find, data)

                if product_info:
                    if not product_info["DiscountOffer"] or not product_info["DiscountPrice (in Rs)"]:
                        product_info.pop("DiscountPrice (in Rs)", None)
                        product_info.pop("DiscountOffer", None)
                        product_info["Price"] = product_info.pop("OriginalPrice (in Rs)")
                    else:
                        product_info["Price"] = int(product_info["DiscountPrice (in Rs)"])
                        product_info.pop("OriginalPrice (in Rs)", None)
                        product_info.pop("DiscountPrice (in Rs)", None)
                        product_info.pop("DiscountOffer", None)

                    product_info["Product_id"] = product_id_to_find
                    lst.append(product_info)

        if lst:
            return {"response": lst}
        else:
            raise HTTPException(status_code=404, detail="Products not found")


@app.post('/chat')
async def chatbot_response(data: ChatRequest):
    chat = model.start_chat(history=[])
    prompt = data.message

    response = chat.send_message(f"{prompt}", stream=False)
    response_text = response.text

    return {"message": response_text}


@app.post('/imagecapture')
async def process_image(content: ImageCaptureRequest):
    imgUri = content.imgURI[23:]  # Strip the base64 prefix
    text = content.text

    modelVision = genai.GenerativeModel(model_name="gemini-pro-vision")
    decoded_image = io.BytesIO(base64.b64decode(imgUri))
    img = Image.open(decoded_image)

    prompt = [f'{text}', img]
    image_description = modelVision.generate_content(prompt)
    image_description = image_description.text
    queryEmbed = get_embedding(image_description)

    similarVectors = index.query(
        namespace="ns1",
        vector=queryEmbed,
        top_k=20,
        include_values=False,
        include_metadata=True
    )

    lst = []
    with open('../data/OGMyntraFasionClothing.json', 'r') as read_file:
        data = json.load(read_file)
        for result in similarVectors['matches']:
            product_id_to_find = result['id']
            product_info = find_product_info(product_id_to_find, data)

            if product_info:
                if not product_info["DiscountOffer"] or not product_info["DiscountPrice (in Rs)"]:
                    product_info.pop("DiscountPrice (in Rs)", None)
                    product_info.pop("DiscountOffer", None)
                    product_info["Price"] = product_info.pop("OriginalPrice (in Rs)")
                else:
                    product_info["Price"] = int(product_info["DiscountPrice (in Rs)"])
                    product_info.pop("OriginalPrice (in Rs)", None)
                    product_info.pop("DiscountPrice (in Rs)", None)
                    product_info.pop("DiscountOffer", None)

                product_info["ImageURL"] = get_image_link(product_info["URL"])
                product_info.pop("URL", None)
                lst.append(product_info)

    return {"response": lst}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="debug")
