# index_generator.py
import pickle
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Document
from dotenv import load_dotenv
import os

from pypdf import PdfReader

load_dotenv()

# Acessar a chave de API do OpenAI
openai_api_key = os.getenv("OPENAI_API_KEY")

class IndexGenerator:
    def __init__(self, pdf_path=None, index_path=None):
        self.pdf_path = pdf_path
        self.index = None

    def read_pdf(self):
        print(f"📄 Caminho do PDF recebido: {self.pdf_path}")
        if not self.pdf_path:
            raise ValueError("Caminho do PDF não fornecido para o IndexGenerator.")
        reader = PdfReader(self.pdf_path)
        return reader.read_pdf()


    def create_index(self, documents):
        document_list = [Document(text=doc) for doc in documents]
        self.index = VectorStoreIndex.from_documents(document_list)
        print(f"✅ Índice criado com sucesso para o documento fornecido.")
        return self.index
    
    def query_index(self, query_text):
        if not self.index:
            raise ValueError("Índice não está carregado. Por favor, crie ou carregue um índice primeiro.")
        response = self.index.query(query_text)
        return response
