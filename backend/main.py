from flask import Flask, request, jsonify
import json
from openai import OpenAI
from pinecone import Pinecone
from bs4 import BeautifulSoup
import requests
from flask_cors import CORS
import re
from PIL import Image
import io
import base64
from dotenv import load_dotenv, dotenv_values
from llama_cpp import Llama

load_dotenv()

env_var = dotenv_values('.env')
pineconeKey = env_var.get("PINECONE_API_KEY")
openAiApiKey = env_var.get('OPENAI_API_KEY')

pc = Pinecone(api_key=pineconeKey)
openAiClient = OpenAI(api_key=openAiApiKey)

llama = Llama(model_path="/path/to/llama-3.2-3b-chat.ggmlv3.q4_0.bin")

index_name = "alien-wear-threehundred"
index = pc.Index(index_name)

app = Flask("backend")
CORS(app)

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

def process_products(product_info, originalQuery):
    prompt = f"""For the Query: {originalQuery}

    {product_info}
    Keeping the above vector as context, can you filter out the best 6 results and return me the product IDs of the Top 6 products.
    Let the format be space separated product ids only."""
    
    response = llama(prompt, max_tokens=100)
    respContent = response['choices'][0]['text'].strip().split()
    print(respContent)
    return respContent

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

@app.route('/occasion', methods=['GET'])
def process_occasion():
    if request.method == 'GET':
        originQuery = request.args.get("query", "")
        if originQuery != "":
            queryEmbed = get_embedding(originQuery)
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
                        product_info.pop("URL", None)
                        product_info.pop("Description", None)
                        
                        if product_info["DiscountOffer"] == '' or product_info["DiscountPrice (in Rs)"] == '':
                            product_info.pop("DiscountPrice (in Rs)", None)
                            product_info.pop("DiscountOffer", None)
                            product_info["Price"] = product_info.pop("OriginalPrice (in Rs)")
                        else:
                            product_info["Price"] = int(product_info["DiscountPrice (in Rs)"])
                            product_info.pop("OriginalPrice (in Rs)", None)
                            product_info.pop("DiscountPrice (in Rs)", None)
                            product_info.pop("DiscountOffer", None)

                        for i in result["metadata"]:
                            product_info[i] = result["metadata"][i]

                        product_info["Product_id"] = product_id_to_find
                        lst.append(product_info)
                    else:
                        print("Product not found.")

            finResp = []
            resp = process_products(lst, originQuery)
            for items in resp:
                product_info = find_product_info(items, data)

                if product_info:
                    if product_info["DiscountOffer"] == '' or product_info["DiscountPrice (in Rs)"] == '':
                        product_info.pop("DiscountPrice (in Rs)", None)
                        product_info.pop("DiscountOffer", None)
                        product_info["Price"] = int(product_info.pop("OriginalPrice (in Rs)"))
                    else:
                        product_info["Price"] = int(product_info["DiscountPrice (in Rs)"])
                        product_info.pop("OriginalPrice (in Rs)", None)
                        product_info.pop("DiscountPrice (in Rs)", None)
                        product_info.pop("DiscountOffer", None)

                    product_info["ImageURL"] = get_image_link(product_info["URL"])
                    finResp.append(product_info)

            return jsonify({"response": finResp}), 200

chat_history = []
@app.route('/chat', methods=['POST', 'GET'])
def chatbot_response():
    global chat_history
    if request.method == 'POST':
        data = request.json
        prompt = data.get("message", "")

        chat_history.append({"role": "user", "content": prompt})
        full_prompt = "\n".join([f"{msg['role']}: {msg['content']}" for msg in chat_history])

        response = llama(full_prompt, max_tokens=200)
        response_text = response['choices'][0]['text'].strip()

        chat_history.append({"role": "assistant", "content": response_text})

        return jsonify({"message": response_text}), 200
    
    if request.method == "GET":
        last_text_section = chat_history[-1]['content'] if chat_history else ""

        if last_text_section != "":
            queryEmbed = get_embedding(last_text_section)
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
                        if product_info["DiscountOffer"] == '' or product_info["DiscountPrice (in Rs)"] == '':
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

        return jsonify({"response": lst}), 200

@app.route('/imagecapture', methods=['POST'])
def process_image():
    if request.method == 'POST':
        content = request.json
        imgUri = content.get("imgURI", "")
        imgUri = imgUri[23:]
        text = content.get("text", "")
        
        decoded_image = io.BytesIO(base64.b64decode(imgUri))
        img = Image.open(decoded_image)

        # Note: Llama 2 doesn't have built-in image processing capabilities.
        # You might need to use a different model or service for image description.
        # For now, we'll use the text as the description.
        image_description = text

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
                    if product_info["DiscountOffer"] == '' or product_info["DiscountPrice (in Rs)"] == '':
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

        return jsonify({"response": lst}), 200

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")