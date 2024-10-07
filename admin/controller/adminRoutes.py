from operator import index

from flask import Flask, request, jsonify
from yaml.reader import Reader

from admin.repository.index_database_manager import IndexDatabaseManager
from admin.services.index_generator.index_generator import IndexGenerator
from admin.services.index_generator.local_index_generator import LocalIndexGenerator
from admin.services.pdf_reader.pdf_reader import PdfReader

app = Flask(__name__)
index_generator = IndexGenerator()
local_index_generator = LocalIndexGenerator()
index_database_manager = IndexDatabaseManager()


@app.route('/read-pdf', methods=['POST'])
def read_pdf():
    data = request.json
    pdf_path = data.get("pdf_path")
    print(f"Recebido: {data}")
    try:
        index_generator.pdf_path = pdf_path
        pdf_content = index_generator.read_pdf()
        return jsonify({"status": "success", "content": pdf_content}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

@app.route('/status', methods=['GET'])
def status():
    return jsonify({"message": "API está funcionando corretamente."}), 200

@app.route('/local-create-index', methods=['POST'])
def local_create_index():
    data = request.json
    pdf_link = data.get("pdf_link")
    client_id=data.get("client_id")

    if not pdf_link:
        return jsonify({"status": "error", "message": "Link do PDF não fornecido."}), 400
    try:
        index_generator.pdf_path = pdf_link
        reader = PdfReader(pdf_link)
        #pdf_content = index_generator.read_pdf()
        pdf_content = reader.read_pdf()
        local_index_generator.client_id = client_id
        index_name = reader.file_name
        index = local_index_generator.create_index(pdf_content, index_name=index_name)        #database_repository = local_index_generator.save_index_to_db(index)
        return jsonify({"status": "success", "message": "Índice criado com sucesso."}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/create-index', methods=['POST'])
def create_index():
    """Endpoint para criar um índice a partir de um PDF fornecido por link."""
    data = request.json
    pdf_link = data.get("pdf_path")

    # Validar se o link do PDF foi fornecido corretamente
    if not pdf_link:
        return jsonify({"status": "error", "message": "Link do PDF não fornecido."}), 400

    try:
        # Atribuir o link do PDF ao IndexGenerator
        index_generator.pdf_path = pdf_link

        # Ler o conteúdo do PDF a partir do link
        pdf_content = index_generator.read_pdf()

        # Criar índice a partir do conteúdo lido do PDF
        index = index_generator.create_index(pdf_content)
        return jsonify({"status": "success", "message": "Índice criado com sucesso."}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/query-index', methods=['POST'])
def query_index():
    data = request.json
    query_text = data.get("query_text")

    try:
        response = local_index_generator.query_index(query_text)
        return jsonify({"status": "success", "response": response}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

@app.route('/load-index', methods=['POST'])
def load_index():
    data = request.json
    index_path = data.get("index_path")

    try:
        index_generator.index_path = index_path
        index_generator.load_index(index_path)
        return jsonify({"status": "success", "message": "Índice carregado com sucesso."}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

@app.route('/save-index', methods=['POST'])
def save_index():
    data = request.json
    index_path = data.get("index_path")

    try:
        index_generator.index_path = index_path
        index_generator.save_index()
        return jsonify({"status": "success", "message": "Índice salvo com sucesso."}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

for rule in app.url_map.iter_rules():
    print(f"Endpoint: {rule.endpoint}, URL: {rule}")
