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
        if not documents or not isinstance(documents, list):
            raise ValueError("Uma lista válida de documentos deve ser fornecida para criar o índice.")
        self.client_id = client_id or self.client_id
        if not self.client_id:
            raise ValueError("client_id é obrigatório para salvar o índice.")
        self.documents = documents
        print(f"📄 Gerando embeddings para {len(documents)} documentos...")
        self.embeddings = self.model.encode(documents, show_progress_bar=True)
        self.nn_model = NearestNeighbors(n_neighbors=5, metric='cosine').fit(self.embeddings)
        print(f"✅ Índice criado com sucesso para os documentos fornecidos.")
        client_dir = os.path.join(self.base_index_dir, str(self.client_id))
        os.makedirs(client_dir, exist_ok=True)
        file_name = f"{index_name}.pkl"
        file_path = os.path.join(client_dir, file_name)
        with open(file_path, 'wb') as f:
            pickle.dump({
                "documents": self.documents,
                "embeddings": self.embeddings,
                "nn_model": self.nn_model
            }, f)
        print(f"✅ Índice salvo localmente no arquivo '{file_path}'.")
        
    def save_index_to_db(self, index_name):
        print(f"✅ Salvando o index no Database")
        index_data = {
            "documents": self.documents,
            "embeddings": self.embeddings.tolist(),
            "metadata": {
                "client_id": self.client_id,
                "index_name": index_name,
                "created_at": datetime.now().isoformat()
            }
        }
        index_json = json.dumps(index_data)
        self.db_manager.save_index_metadata(index_name, index_json)


    def query_index(self, query_text):
        if not self.nn_model or not self.embeddings.any():
            raise ValueError("O índice não está disponível. Crie o índice primeiro.")
        query_embedding = self.model.encode([query_text])
        distances, indices = self.nn_model.kneighbors(query_embedding)
        similar_documents = [self.documents[idx] for idx in indices[0]]
        return similar_documents

    def save_index(self, index_path="index.pkl"):
        if not self.nn_model or not self.embeddings.any():
            raise ValueError("O índice não está disponível para ser salvo. Crie o índice primeiro.")
        index_data = {
            "documents": self.documents,
            "embeddings": self.embeddings,
            "nn_model": self.nn_model
        }
        with open(index_path, 'wb') as f:
            pickle.dump(index_data, f)
            print(f"✅ Índice salvo com sucesso em '{index_path}'")

    def load_index(self, index_path="index.pkl"):
        if not os.path.exists(index_path):
            raise FileNotFoundError(f"O arquivo de índice '{index_path}' não foi encontrado.")
        with open(index_path, 'rb') as f:
            index_data = pickle.load(f)
        self.documents = index_data["documents"]
        self.embeddings = index_data["embeddings"]
        self.nn_model = index_data["nn_model"]
        print(f"✅ Índice carregado com sucesso de '{index_path}'")
