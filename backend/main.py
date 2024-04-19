#IMPORTS
from flask import Flask,request,jsonify
import json
from openai import OpenAI
from pinecone import Pinecone, ServerlessSpec

#API KEYS
pc = Pinecone(api_key='07aa3ce1-17c1-40cd-bfb9-677aa7ed7af3')
openAiClient = OpenAI(api_key='sk-proj-FXWeftP1rksQ54yrB2uNT3BlbkFJKRquq7MP8KkL3UqGkUT5')

index_name = "alienwear"


#FLASK SETUP
app = Flask("backend")

def get_embedding(query,model = "text-embedding-3-small"):
    return openAiClient.embeddings.create(input=[query], model = model).data[0].embedding

@app.route('/occasion',methods=['GET'])
def process_occasion():
    try:
        if request.method == 'GET':
            data = request.args.get("query","")
            if data != "":
                # return jsonify({"response":data}),200
                pass
    
    except Exception as err:
        return jsonify({"response":err}),500
    L

    
        

@app.route('/query',methods=['GET'])
def process_query():
    try:
        if request.method == 'GET':
            data = request.args.get("query","")
            if data != "":
                return jsonify({"response":data}),200
    
    except Exception as err:
        return jsonify({"response":err}),500

if __name__ == "__main__":
    app.run(debug=True)