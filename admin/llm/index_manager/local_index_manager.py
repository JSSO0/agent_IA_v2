import numpy as np
from sentence_transformers import SentenceTransformer
import json
from admin.repository.index_database_manager import IndexDatabaseManager
import os
import pickle
from datetime import datetime
from sklearn.neighbors import NearestNeighbors

class LocalIndexGenerator:
    def __init__(self, base_index_dir="indices", model_name='all-MiniLM-L6-v2', client_id=None):
        self.model = SentenceTransformer(model_name)
        self.base_index_dir = base_index_dir
        self.client_id = client_id
        self.documents = []
        self.embeddings = None
        self.nn_model = None
        self.db_manager = IndexDatabaseManager()

    def create_index(self, documents, index_name="default_index", client_id=None):
        self.client_id = client_id or self.client_id
        self.validate_documents(documents)
        self.documents = documents
        self.embeddings = self.generate_embeddings(documents)
        self.nn_model = self.create_nearest_neighbors_model(self.embeddings)
        client_dir = self.ensure_client_directory_exists()
        file_path = self.save_index_to_file(client_dir, index_name)
        print(f"✅ Índice salvo localmente no arquivo '{file_path}'.")

    def validate_documents(self, documents):
        if not documents or not isinstance(documents, list):
            raise ValueError("Uma lista válida de documentos deve ser fornecida para criar o índice.")
        if not self.client_id:
            raise ValueError("client_id é obrigatório para salvar o índice.")
    
    def generate_embeddings(self, documents):
        print(f"📄 Gerando embeddings para {len(documents)} documentos...")
        embeddings = self.model.encode(documents, show_progress_bar=True)
        return embeddings
    
    def create_nearest_neighbors_model(self, embeddings):
        print(f"🔍 Criando o modelo de vizinhos mais próximos...")
        nn_model = NearestNeighbors(n_neighbors=5, metric='cosine').fit(embeddings)
        print(f"✅ Modelo de vizinhos mais próximos criado com sucesso.")
        return nn_model

    def ensure_client_directory_exists(self):
        client_dir = os.path.join(self.base_index_dir, str(self.client_id))
        os.makedirs(client_dir, exist_ok=True)
        return client_dir

    def save_index_to_file(self, client_dir, index_name):
        file_name = f"{index_name}.pkl"
        file_path = os.path.join(client_dir, file_name)

        with open(file_path, 'wb') as f:
            pickle.dump({
                "documents": self.documents,
                "embeddings": self.embeddings,
                "nn_model": self.nn_model
            }, f)

        return file_path

