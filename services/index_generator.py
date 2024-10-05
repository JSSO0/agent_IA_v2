# index_generator.py
import pickle
from services.pdf_reader import PDFReader 
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Document  
class IndexGenerator:  
    def __init__(self, pdf_path=None, index_path=None):
        self.pdf_path = pdf_path
        self.index_path = index_path  # Caminho do índice adicionado
        self.index = None
    def read_pdf(self):
        if not self.pdf_path:
            raise ValueError("Caminho do PDF não fornecido para o IndexGenerator.")
        reader = PDFReader(self.pdf_path)
        return reader.read_pdf()
    def create_index(self, documents):
        document_list = [Document(text=doc) for doc in documents]
        self.index = VectorStoreIndex.from_documents(document_list)
        print(f"✅ Índice criado com sucesso para o documento fornecido.")
        return self.index
    
    def query_index(self, query_text):
        """Consulta o índice para uma resposta a partir de uma pergunta."""
        if not self.index:
            raise ValueError("Índice não está carregado. Por favor, crie ou carregue um índice primeiro.")
        response = self.index.query(query_text)
        return response
    
    def load_index(self):
        """Carrega o índice salvo de um arquivo utilizando 'pickle'."""
        # Usando self.index_path ao invés de index_path
        if not self.index_path:
            raise ValueError("Caminho para o arquivo de índice não fornecido.")

        try:
            with open(self.index_path, 'rb') as file:  # Usando self.index_path
                self.index = pickle.load(file)
                print(f"✅ Índice carregado com sucesso de '{self.index_path}'")
        except FileNotFoundError:
            raise FileNotFoundError(f"⚠️ Arquivo de índice '{self.index_path}' não encontrado. Por favor, forneça um caminho válido.")

    def save_index(self):
        """Salva o índice em um arquivo utilizando 'pickle'."""
        # Usando self.index_path ao invés de index_path
        if not self.index:
            raise ValueError("⚠️ Nenhum índice disponível para salvar. Crie o índice primeiro.")
        if not self.index_path:
            raise ValueError("Caminho para o arquivo de índice não fornecido.")

        try:
            with open(self.index_path, 'wb') as file:  # Usando self.index_path
                pickle.dump(self.index, file)
                print(f"✅ Índice salvo com sucesso em '{self.index_path}'")
        except Exception as e:
            raise IOError(f"Erro ao salvar o índice em '{self.index_path}': {str(e)}")
