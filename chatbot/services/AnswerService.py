# chatbot/services/answer_service.py

import os
import pickle
from flask import jsonify
from chatbot.llm.generate_answer import GenerateAnswer

class AnswerService:
    def __init__(self):
        self.index_generator = GenerateAnswer()

    def load_index(self, index_dir, index_name):
        index_file = os.path.join(index_dir, f'{index_name}')
        try:
            with open(index_file, 'rb') as f:
                index = pickle.load(f)
        except FileNotFoundError:
            return None
        self.index_generator.documents = index['documents']
        self.index_generator.embeddings = index['embeddings']
        self.index_generator.nn_model = index['nn_model']
        return self.index_generator

    def ask_question(self, question, index_dir, index_name):
        index_generator = self.load_index(index_dir, index_name)
        if index_generator is None:
            return jsonify({'error': 'Index not found'}), 404
        answer = index_generator.query_index(question)
        return jsonify({'answer': answer})