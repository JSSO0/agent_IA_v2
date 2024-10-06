from sentence_transformers import SentenceTransformer
import json
from admin.repository.index_database_manager import IndexDatabaseManager
import os
import pickle
from datetime import datetime
from sklearn.neighbors import NearestNeighbors


class LocalIndexGenerator:
    def __init__(self, index_dir="indices", index_path="index.pkl", client_id = None):

        self.index_dir = index_dir  # Diretório para salvar arquivos .pkl
        os.makedirs(index_dir, exist_ok=True)  # Criar diretório, se não existir
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.documents = []
        self.embeddings = None
        self.nn_model = None
        self.index_path = index_path
        self.client_id = client_id
        self.db_manager = IndexDatabaseManager()

    def create_index(self, documents, index_name="default_index"):
        if not documents or not isinstance(documents, list):
            raise ValueError("Uma lista válida de documentos deve ser fornecida para criar o índice.")
        self.documents = documents
        self.embeddings = self.model.encode(documents, show_progress_bar=True)
        self.nn_model = NearestNeighbors(n_neighbors=5, metric='cosine').fit(self.embeddings)
        #self.save_index_to_db(index_name)
        file_name = f"{index_name}.pkl"  # Nome do arquivo
        file_path = os.path.join(self.index_dir, file_name)
        with open(file_path, 'wb') as f:
            pickle.dump({
                "documents": self.documents,
                "embeddings": self.embeddings,
                "nn_model": self.nn_model
            }, f)
        print(f"✅ Índice salvo localmente no arquivo '{file_path}'.")
        print(self.client_id)
        self.db_manager.save_index_metadata(
            client_id=self.client_id,
            index_name=index_name,
            file_name=file_name
        )

    def save_index_to_db(self, index_name):
        print(f"✅ Salvando o index no Database")
        index_data = {
            "documents": self.documents,
            "embeddings": self.embeddings.tolist(),  # Converter o array NumPy para listas
            "metadata": {
                "client_id": self.client_id,
                "index_name": index_name,
                "created_at": datetime.now().isoformat()
            }
        }
        index_json = json.dumps(index_data)
        self.db_manager.save_index_metadata(index_name, index_json)


    def query_index(self, query_text):
        """Realiza uma consulta ao índice para encontrar documentos similares."""
        if not self.nn_model or not self.embeddings.any():
            raise ValueError("O índice não está disponível. Crie o índice primeiro.")

        # Gerar embedding para a query
        query_embedding = self.model.encode([query_text])

        # Encontrar os documentos mais similares utilizando o índice de vizinhos mais próximos
        distances, indices = self.nn_model.kneighbors(query_embedding)

        # Retornar os documentos mais similares
        similar_documents = [self.documents[idx] for idx in indices[0]]
        return similar_documents

    def save_index(self, index_path="index.pkl"):
        """Salva o índice, documentos e embeddings em um arquivo pickle."""
        if not self.nn_model or not self.embeddings.any():
            raise ValueError("O índice não está disponível para ser salvo. Crie o índice primeiro.")

        # Empacotar os dados em um dicionário para salvar com pickle
        index_data = {
            "documents": self.documents,
            "embeddings": self.embeddings,
            "nn_model": self.nn_model
        }

        with open(index_path, 'wb') as f:
            pickle.dump(index_data, f)
            print(f"✅ Índice salvo com sucesso em '{index_path}'")

    def load_index(self, index_path="index.pkl"):
        """Carrega o índice, documentos e embeddings de um arquivo pickle."""
        if not os.path.exists(index_path):
            raise FileNotFoundError(f"O arquivo de índice '{index_path}' não foi encontrado.")

        with open(index_path, 'rb') as f:
            index_data = pickle.load(f)

        # Restaurar os dados carregados para os atributos da classe
        self.documents = index_data["documents"]
        self.embeddings = index_data["embeddings"]
        self.nn_model = index_data["nn_model"]
        print(f"✅ Índice carregado com sucesso de '{index_path}'")
