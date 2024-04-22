from pinecone import Pinecone, ServerlessSpec
import json

pc = Pinecone(api_key='YOUR_API_KEY')

index_name = "alien-wear-threehundred"

# pc.create_index(
#     name=index_name,
#     dimension=1536,
#     metric="cosine",
#     spec=ServerlessSpec(
#         cloud='aws', 
#         region='us-east-1'
#     ) 
# ) 

index = pc.Index(index_name)

fp = open("../data/Final100kEmbed_pineconeready.json", "r")
vectors = json.load(fp)

num_vectors = len(vectors)
start_index = 69668 # Starting index for upserting
batch_size = 300 # Size of each batch

# Loop through the vectors in batches of 300
for i in range(start_index, num_vectors, batch_size):
    end_index = min(i + batch_size, num_vectors) # Ensure we don't go out of bounds
    batch_vectors = vectors[i:end_index]
    
    # Upsert the batch of vectors
    index.upsert(
        vectors=batch_vectors,
        namespace="ns1"
    )
fp.close()

# index.upsert(
#     vectors=[
#         {"id": "vec5", "metadata": {"description": "hello"}, "values": [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]},
#         {"id": "vec6", "metadata": {"description": "hello"}, "values": [0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6]},
#         {"id": "vec7", "metadata": {"description": "hello"}, "values": [0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7]},
#         {"id": "vec8", "metadata": {"description": "hello"}, "values": [0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8]}
#     ],
#     namespace="ns2"
# )

# print(index.describe_index_stats())

# res1=index.query(
#     namespace="ns1",
#     vector=[0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3],
#     top_k=3,
#     include_values=True,
#     include_metadata=True
# )

# res2=index.query(
#     namespace="ns2",
#     vector=[0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7],
#     top_k=3,
#     include_values=True,
#     include_metadata=True
    
# )

# Returns:
# {'matches': [{'id': 'vec3',
#               'score': 0.0,
#               'values': [0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3]},
#              {'id': 'vec4',
#               'score': 0.0799999237,
#               'values': [0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4]},
#              {'id': 'vec2',
#               'score': 0.0800000429,
#               'values': [0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2]}],
#  'namespace': 'ns1',
#  'usage': {'read_units': 6}}
# {'matches': [{'id': 'vec7',
#               'score': 0.0,
#               'values': [0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7]},
#              {'id': 'vec8',
#               'score': 0.0799999237,
#               'values': [0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8]},
#              {'id': 'vec6',
#               'score': 0.0799999237,
#               'values': [0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6]}],
#  'namespace': 'ns2',
#  'usage': {'read_units': 6}}

# print(res1)





