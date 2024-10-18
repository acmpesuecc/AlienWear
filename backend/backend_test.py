import json
from openai import OpenAI
from pinecone import Pinecone
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv, dotenv_values
from llama_cpp import Llama

load_dotenv()

env_var = dotenv_values('.env')
pineconeKey = env_var.get("PINECONE_API_KEY")
openAiApiKey = env_var.get('OPENAI_API_KEY')

pc = Pinecone(api_key=pineconeKey)
openAiClient = OpenAI(api_key=openAiApiKey)

index_name = "alien-wear-threehundred"
index = pc.Index(index_name)

llama = Llama(model_path="/path/to/llama-3.2-3b-chat.ggmlv3.q4_0.bin")


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

def process_products(product_info):
    prompt = f"""
    Here is a list of product information:
    {product_info}
    
    Based on this information, please filter out the best 6 results and return the product IDs and Image URLs of these top 6 products in JSON format.
    """
    
    response = llama(prompt, max_tokens=1000)
    
    return response['choices'][0]['text']

def find_product_info(product_id, data):
    for item in data:
        if item["Product_id"] == product_id:
            return {
                "DiscountPrice (in Rs)": item.get("DiscountPrice (in Rs)", ""),
                "OriginalPrice (in Rs)": item.get("OriginalPrice (in Rs)", ""),
                "DiscountOffer": item.get("DiscountOffer", ""),
                "URL": item.get("URL", "")
            }
    return None

def get_embedding(query, model="text-embedding-3-small"):
    return openAiClient.embeddings.create(input=[query], model=model).data[0].embedding

queryEmbed = get_embedding("Kurta for girls")
similarVectors = index.query(
    namespace="ns1",
    vector=queryEmbed,
    top_k=10,
    include_values=False,
    include_metadata=True
)

lst = []
for result in similarVectors['matches']:
    product_id_to_find = result['id']
    print(result['id'])
    with open('../data/OGMyntraFasionClothing.json', 'r') as read_file:
        data = json.load(read_file)
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

            for i in result["metadata"]:
                product_info[i] = result["metadata"][i]

            product_info["Product_id"] = product_id_to_find
            product_info["ImageURL"] = get_image_link(product_info["URL"])
            lst.append(product_info)
        else:
            print("Product not found.")

print(process_products(lst))