from openai import OpenAI
import json
import concurrent.futures

client = OpenAI(
  api_key='sk-proj-FXWeftP1rksQ54yrB2uNT3BlbkFJKRquq7MP8KkL3UqGkUT5',
)

def get_embedding(text, model="text-embedding-3-small"):
   text = text.replace("\n", " ")
   return client.embeddings.create(input = [text], model=model).data[0].embedding

def process_item(item):
    input_val = item["Category"] + "," + item["Individual_category"] + "," + item["category_by_Gender"] + "," + item['Description']
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