from openai import OpenAI
import json
import concurrent.futures
import os

# Securely load your API key from environment variables
api_key = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=api_key)

def get_embedding(text, model="text-embedding-3-small"):
    text = text.replace("\n", " ").strip()
    try:
        response = client.embeddings.create(input=[text], model=model)
        return response.data[0].embedding
    except Exception as e:
        print(f"Error retrieving embedding: {e}")
        return None  # or handle as appropriate

def process_item(item):
    input_val = f"{item['Category']}, {item['Individual_category']}, {item['category_by_Gender']}, {item['Description']}"
    item['values'] = get_embedding(input_val)
    return item

# Load the JSON file
with open('../data/Final100k.json') as f:
    data = json.load(f)

# Use a ThreadPoolExecutor to process the items in parallel
with concurrent.futures.ThreadPoolExecutor() as executor:
    data = list(executor.map(process_item, data[25000:]))

# Write the updated entries to a new JSON file
with open('../data/Final100kEmbed.json', 'w') as f:
    json.dump(data, f)
