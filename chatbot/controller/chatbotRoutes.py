import os
import pickle
from flask import Blueprint, Flask, request, jsonify
from chatbot.services import AnswerService

app = Flask(__name__)
answer_service = AnswerService()
chatbot_routes = Blueprint('chatbot', __name__)

@chatbot_routes.route('/chatbot')
def chatbot():
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
        response = answer_service.ask_question(question, index_dir, index_name)
        return response