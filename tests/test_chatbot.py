# tests/test_chatbot.py

import unittest
from admin.services.agentIA.chatbot import Chatbot

class TestChatbot(unittest.TestCase):
    def setUp(self):
        # Configuração inicial para os testes
        self.chatbot = Chatbot(pdf_path="documento_exemplo.pdf", index_path="meu_indice_test.json")

    def test_get_response(self):
        # Testa se o chatbot responde corretamente a uma pergunta
        response = self.chatbot.get_response("Qual é o resumo do documento?")
        self.assertIsNotNone(response)
        self.assertTrue(len(response) > 0)

    def test_empty_question(self):
        # Testa resposta para uma pergunta vazia
        response = self.chatbot.get_response("")
        self.assertEqual(response, "⚠️ Pergunta vazia. Por favor, forneça uma pergunta válida.")

if __name__ == "__main__":
    unittest.main()
