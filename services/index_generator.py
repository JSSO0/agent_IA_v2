# index_generator.py
from pdf_reader import PDFReader 
from llama_index import VectorStoreIndex
class IndexGenerator:
    def __init__(self, pdf_path=None):
        self.pdf_path = pdf_path
        self.index = None
    def read_pdf(self):
        if not self.pdf_path:
            raise ValueError("Caminho do PDF não fornecido para o IndexGenerator.")
        reader = PDFReader(self.pdf_path)
        return reader.read_pdf()
    def create_index(self, documents):
        document_list = [ {"text": doc} for doc in documents ]
        self.index = VectorStoreIndex.from_documents(document_list)
        print(f"✅ Índice criado com sucesso para o documento fornecido.")
        return self.index
    
    def query_index(self, query_text):
        """Consulta o índice para uma resposta a partir de uma pergunta."""
        if not self.index:
            raise ValueError("Índice não está carregado. Por favor, crie ou carregue um índice primeiro.")
        response = self.index.query(query_text)
        return response
    
    def load_index(self, index_path):
         """Carrega o índice salvo de um arquivo JSON."""
    try:
        with open(index_path, 'r') as file:
            self.index = json.load(file)
            print(f"✅ Índice carregado com sucesso de '{index_path}'")
    except FileNotFoundError:
        raise FileNotFoundError(f"⚠️ Arquivo de índice '{index_path}' não encontrado. Por favor, forneça um caminho válido.")

    def save_index(self, index_path):
     """Salva o índice em um arquivo JSON."""
    if not self.index:
        raise ValueError("⚠️ Nenhum índice disponível para salvar. Crie o índice primeiro.")
    try:
        with open(index_path, 'w') as file:
            json.dump(self.index, file)
            print(f"✅ Índice salvo com sucesso em '{index_path}'")
    except Exception as e:
        raise IOError(f"Erro ao salvar o índice em '{index_path}': {str(e)}")
