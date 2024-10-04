import os
from llama_index import SimpleDirectoryReader, VectorStoreIndex
from pypdf import PdfReader

class PDFIndexer:
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path
        self.index = None

    def read_pdf(self):
        content = []
        if not os.path.exists(self.pdf_path):
            raise FileNotFoundError(f"Arquivo PDF não encontrado: {self.pdf_path}")
        with open(self.pdf_path, 'rb') as file:
            reader = PdfReader(file)
            for page_num, page in enumerate(reader.pages):
                text = page.extract_text()
                if text:
                    content.append(text)
                else:
                    print(f"⚠️ Aviso: Não foi possível extrair texto da página {page_num + 1}")
        return content

    def create_index(self, documents):
        document_list = [ {"text": doc} for doc in documents ]
        self.index = VectorStoreIndex.from_documents(document_list)
        return self.index

    def save_index(self, index_path="index.json"):
        if not self.index:
            raise ValueError("Índice não encontrado. Crie o índice primeiro com 'create_index'.")
        self.index.save_to_disk(index_path)
        print(f"✅ Índice salvo com sucesso em: {index_path}")

    def load_index(self, index_path="index.json"):
        if not os.path.exists(index_path):
            raise FileNotFoundError(f"Arquivo de índice não encontrado: {index_path}")
        self.index = VectorStoreIndex.load_from_disk(index_path)
        print(f"✅ Índice carregado com sucesso de: {index_path}")
        return self.index

    def query_index(self, query_text):
        if not self.index:
            raise ValueError("Índice não carregado. Crie ou carregue um índice primeiro.")
        query_engine = self.index.as_query_engine()
        response = query_engine.query(query_text)
        return response