import json

with open('../data/Final100kEmbed.json', 'r') as read_file:
    data = json.load(read_file)
    
    for item in data:
        item["id"] = item.pop("Product_id")
        
        metadata = {
            "Category": item["Category"],
            "Individual_category": item["Individual_category"],
            "category_by_Gender": item["category_by_Gender"],
            "Description": item["Description"]
        }
        
        item["metadata"] = metadata
        
        del item["Category"]
        del item["Individual_category"]
        del item["category_by_Gender"]
        del item["Description"]

with open('../data/Final100kEmbed_pineconeready.json', 'w') as write_file:
    json.dump(data, write_file, indent=4)
