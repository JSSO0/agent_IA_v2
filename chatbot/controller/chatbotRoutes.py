# backend/api.py

import os
import pickle
from flask import Flask, request, jsonify

from admin.llm.index_manager.local_index_manager import LocalIndexGenerator

app = Flask(__name__)

@app.route('/ask', methods=['POST'])
def ask_question():
    data = request.json
    question = data.get('question')
    company_id = data.get('companyId')
    index_name = data.get('index_name')
    user_id = data.get('user_id')
    if not all([question, company_id, index_name, user_id]):
        return jsonify({'error': 'Missing required parameters'}), 400
    index_dir = os.path.join('indices', str(company_id))
    index_file = os.path.join(index_dir, f'{index_name}')
    print(index_dir)
    print(index_file)
    try:
        with open(index_file, 'rb') as f:
            index = pickle.load(f)
    except FileNotFoundError:
        return jsonify({'error': 'Index not found'}), 404
    index_generator = LocalIndexGenerator()
    index_generator.documents = index['documents']
    index_generator.embeddings = index['embeddings']
    index_generator.nn_model = index['nn_model']
    answer = index_generator.query_index(question)
    return jsonify({'answer': answer})