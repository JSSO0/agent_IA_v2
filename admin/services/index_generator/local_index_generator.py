import os
import pickle
from sentence_transformers import SentenceTransformer
from sklearn.neighbors import NearestNeighbors


class LocalIndexGenerator:
    def __init__(self, index_path="index.pkl"):
        # Inicializar o modelo de embeddings local e definir o caminho padrão para salvar o índice
        self.model = SentenceTransformer('all-MiniLM-L6-v2')  # Usando um modelo leve e rápido
        self.documents = []  # Lista para armazenar os documentos
        self.embeddings = None  # Armazenar os embeddings dos documentos
        self.nn_model = None  # Modelo de vizinhos mais próximos para busca
        self.index_path = index_path  # Caminho padrão para salvar o índice

    def create_index(self, documents, index_path=None):
        """
        Cria um índice de similaridade a partir de uma lista de documentos e salva em um arquivo.
        """
        if not documents or not isinstance(documents, list):
            raise ValueError("Uma lista válida de documentos deve ser fornecida para criar o índice.")

        # Armazenar os documentos
        self.documents = documents

        # Gerar embeddings para cada documento usando o modelo local
        print(f"📄 Gerando embeddings para {len(documents)} documentos...")
        self.embeddings = self.model.encode(documents, show_progress_bar=True)

        # Criar um índice de busca utilizando NearestNeighbors
        self.nn_model = NearestNeighbors(n_neighbors=5, metric='cosine').fit(self.embeddings)
        print(f"✅ Índice criado com sucesso para os documentos fornecidos.")

        # Definir o caminho para salvar o índice, usando o valor fornecido ou o caminho padrão
        if index_path:
            self.index_path = index_path
        else:
            index_path = self.index_path

        # Salvar o índice no arquivo index.pkl ou no caminho fornecido
        self.save_index(index_path)
        print(f"✅ Índice salvo automaticamente em '{index_path}'.")

        return self.nn_model

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
