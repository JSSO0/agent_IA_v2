# backend/api.py

import flask
import backend.chatbot

from flask import Flask, request, jsonify
from backend.chatbot import Chatbot

app = Flask(__name__)
PDF_PATH = "./DocumentodeExemploParaTestes.pdf"
INDEX_PATH = "./meu_indice.json"
chatbot = Chatbot(pdf_path=PDF_PATH, index_path=INDEX_PATH)

@app.route('/ask-to-chatbot', methods=['POST'])
def ask_question():
    try:
        question = request.json.get("question")
        if not question:
            return jsonify({"error": "Pergunta não fornecida."}), 400
        response = chatbot.get_response(question)
        return jsonify({"response": response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/create-pdf-index', methods=['POST'])
def create_pdf_index():
    try:
        pdf_path = request.json.get("pdf_path")
        index_path = request.json.get("index_path")
        if not pdf_path:
            return jsonify({"error": "Caminho para o PDF não fornecido."}), 400
        if not index_path:
            return jsonify({"error": "Caminho para o índice não fornecido."}), 400
        chatbot.create_index(pdf_path=pdf_path, index_path=index_path)
        return jsonify({"message": "Índice criado com sucesso."})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
