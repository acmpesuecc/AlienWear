'''# from openai import OpenAI
# import json
# # client = OpenAI()
# # defaults to getting the key using os.environ.get("OPENAI_API_KEY")
# # if you saved the key under a different environment variable name, you can do something like:
# client = OpenAI(
#   api_key='sk-proj-FXWeftP1rksQ54yrB2uNT3BlbkFJKRquq7MP8KkL3UqGkUT5',
# )

# def get_embedding(text, model="text-embedding-3-small"):
#    text = text.replace("\n", " ")
#    return client.embeddings.create(input = [text], model=model).data[0].embedding


# # print(get_embedding("Once upon a time..."))


# input_val=(item["Category"] + "," + item["Individual_category"] + "," + item["category_by_Gender"] + "," + item['Description'])

'''    


from openai import OpenAI
import json

client = OpenAI(
  api_key='sk-proj-FXWeftP1rksQ54yrB2uNT3BlbkFJKRquq7MP8KkL3UqGkUT5',
)

def get_embedding(text, model="text-embedding-3-small"):
   text = text.replace("\n", " ")
   return client.embeddings.create(input = [text], model=model).data[0].embedding

# Load the JSON file
with open('../data/NewMyntra25k.json') as f:
    data = json.load(f)

# Iterate over each entry in the JSON file
for item in data:
    input_val = item["Category"] + "," + item["Individual_category"] + "," + item["category_by_Gender"] + "," + item['Description']
    item['embedding'] = get_embedding(input_val)

# Write the updated entries to a new JSON file
with open('../data/NewMyntra25k_embed.json', 'w') as f:
    json.dump(data, f)