import json
import os

# Load the JSON file
input_path = '../data/Final100kEmbed.json'
output_path = '../data/Final100kEmbed_pineconeready.json'

try:
    with open(input_path, 'r') as read_file:
        data = json.load(read_file)
        
        for item in data:
            # Safely get Product_id and assign it to id
            item["id"] = item.pop("Product_id", None)
            
            # Create metadata with existence checks
            metadata = {
                "Category": item.get("Category"),
                "Individual_category": item.get("Individual_category"),
                "category_by_Gender": item.get("category_by_Gender"),
                "Description": item.get("Description")
            }
            
            item["metadata"] = metadata
            
            # Remove original fields using a loop
            for key in metadata.keys():
                item.pop(key, None)  # Safe pop with default None
            
except FileNotFoundError:
    print(f"Error: The file {input_path} does not exist.")
except json.JSONDecodeError:
    print("Error: Failed to decode JSON from the input file.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")

# Write the updated entries to a new JSON file
try:
    with open(output_path, 'w') as write_file:
        json.dump(data, write_file, indent=4)
except Exception as e:
    print(f"Error writing to file {output_path}: {e}")
