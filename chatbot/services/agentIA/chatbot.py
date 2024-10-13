# chatbot.py
from admin.llm.index_generator.index_generator import IndexGenerator

class Chatbot:
    def __init__(self, pdf_path=None, index_path="index.json"):
        self.index_generator = IndexGenerator(pdf_path=pdf_path)
        self.index_path = index_path
        self.initialize_indexer()
    def initialize_indexer(self):
        try:
            self.index_generator.load_index(self.index_path)
            print(f"✅ Índice carregado com sucesso de '{self.index_path}'")
        except FileNotFoundError:
            print(f"⚠️ Índice não encontrado em '{self.index_path}', criando um novo...")
            if self.index_generator.pdf_path:
                pdf_content = self.index_generator.read_pdf()
                self.index_generator.create_index(documents=pdf_content)
                self.index_generator.save_index(self.index_path)
                print(f"✅ Novo índice criado e salvo como '{self.index_path}'")
            else:
                raise ValueError("Nenhum índice salvo ou caminho do PDF fornecido. Impossível criar o índice.")
    def get_response(self, question):
        if not question:
            return "⚠️ Pergunta vazia. Por favor, forneça uma pergunta válida."
        response = self.index_generator.query_index(query_text=question)
        return str(response)
