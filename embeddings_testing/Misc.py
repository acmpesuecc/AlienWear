import json

# Open the input file
with open('../data/new_25k_items_embed.json', 'r') as read_file:
    # Load the JSON data
    data = json.load(read_file)
    
    # Iterate over each item in the JSON data
    for item in data:
        # Rename the "Product_id" to "id"
        item["id"] = item.pop("Product_id")
        
        # Create a new dictionary for metadata
        metadata = {
            "Category": item["Category"],
            "Individual_category": item["Individual_category"],
            "category_by_Gender": item["category_by_Gender"],
            "Description": item["Description"]
        }
        
        # Assign the metadata to a new key
        item["metadata"] = metadata
        
        # Remove the original headers
        del item["Category"]
        del item["Individual_category"]
        del item["category_by_Gender"]
        del item["Description"]

# Write the modified data back to the file
with open('../data/Final25kEmbed.json', 'w') as write_file:
    json.dump(data, write_file, indent=4)
