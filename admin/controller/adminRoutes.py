from operator import index

from flask import Flask, request, jsonify
from yaml.reader import Reader

from admin.llm.index_manager.local_index_manager import LocalIndexGenerator
from admin.repository.index_database_manager import IndexDatabaseManager
from admin.llm.pdf_reader.pdf_reader import CustomPDFReader, PdfReader
from admin.services.adminServices import adminServices

app = Flask(__name__)
local_index_generator = LocalIndexGenerator()
index_database_manager = IndexDatabaseManager()


@app.route('/status', methods=['GET'])
def status():
    return jsonify({"message": "API está funcionando corretamente."}), 200

@app.route('/local-create-index', methods=['POST'])
def local_create_index():
    admin_services = adminServices()
    data = request.json
    result, status_code = admin_services.local_create_index_services(data)
    return jsonify(result), status_code

for rule in app.url_map.iter_rules():
    print(f"Endpoint: {rule.endpoint}, URL: {rule}")
