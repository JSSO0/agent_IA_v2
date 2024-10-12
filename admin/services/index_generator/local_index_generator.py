from sentence_transformers import SentenceTransformer
import json
from admin.repository.index_database_manager import IndexDatabaseManager
import os
import pickle
from datetime import datetime
from sklearn.neighbors import NearestNeighbors


class LocalIndexGenerator:
    def __init__(self, base_index_dir="indices", model_name='all-MiniLM-L6-v2', client_id=None):
        # Inicializar o modelo de embeddings
        self.model = SentenceTransformer(model_name)
        self.base_index_dir = base_index_dir  # Diretório base para salvar os índices
        self.client_id = client_id  # ID do cliente associado ao índice
        self.documents = []  # Lista para armazenar os documentos
        self.embeddings = None  # Armazenar os embeddings dos documentos
        self.nn_model = None  # Modelo de vizinhos mais próximos para busca
        self.db_manager = IndexDatabaseManager()  # Instância do gerenciador de banco de dados

    def create_index(self, documents, index_name="default_index", client_id=None):
        """Cria o índice a partir de uma lista de documentos e salva localmente como arquivo .pkl."""
        if not documents or not isinstance(documents, list):
            raise ValueError("Uma lista válida de documentos deve ser fornecida para criar o índice.")

        # Garantir que o client_id esteja definido
        self.client_id = client_id or self.client_id
        if not self.client_id:
            raise ValueError("client_id é obrigatório para salvar o índice.")

        # Armazenar os documentos e gerar embeddings
        self.documents = documents
        print(f"📄 Gerando embeddings para {len(documents)} documentos...")
        self.embeddings = self.model.encode(documents, show_progress_bar=True)

        # Criar o índice de vizinhos mais próximos
        self.nn_model = NearestNeighbors(n_neighbors=5, metric='cosine').fit(self.embeddings)
        print(f"✅ Índice criado com sucesso para os documentos fornecidos.")

        # Criar a pasta com o client_id como nome, se ainda não existir
        client_dir = os.path.join(self.base_index_dir, str(self.client_id))
        os.makedirs(client_dir, exist_ok=True)  # Criar a pasta, se não existir

        # Salvar o arquivo .pkl com o nome do PDF (index_name) na pasta do cliente
        file_name = f"{index_name}.pkl"
        file_path = os.path.join(client_dir, file_name)  # Usar client_dir para salvar o arquivo

        with open(file_path, 'wb') as f:
            pickle.dump({
                "documents": self.documents,
                "embeddings": self.embeddings,
                "nn_model": self.nn_model
            }, f)

        print(f"✅ Índice salvo localmente no arquivo '{file_path}'.")

        # Salvar metadados no banco de dados
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
