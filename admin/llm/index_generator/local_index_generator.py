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
        """
        Consulta o índice usando o modelo de vizinhos mais próximos e gera uma resposta estruturada com base nos documentos encontrados.
        """
        if not self.nn_model or self.embeddings is None or not len(self.embeddings):
            raise ValueError("O índice não está disponível. Crie o índice primeiro.")
        
        # Gerar o embedding da pergunta
        query_embedding = self.model.encode([query_text])
        
        # Encontrar os documentos mais próximos
        distances, indices = self.nn_model.kneighbors(query_embedding)

        # Coletar os documentos semelhantes
        similar_documents = [self.documents[idx] for idx in indices[0]]

        # Construir uma resposta com base nos documentos encontrados
        resposta = self.gerar_resposta_estruturada(similar_documents, query_text)
        
        return resposta
    def gerar_resposta_estruturada(self, documentos_relevantes, pergunta):
        """
        Gera uma resposta estruturada com base no conteúdo dos documentos relevantes.
        Aqui usamos o modelo all-MiniLM-L6-v2 para encontrar as frases mais relevantes.
        """
        resposta = ""

        # Quebrar os documentos relevantes em frases ou sentenças
        todas_as_frases = []
        for doc in documentos_relevantes:
            frases = doc.split(". ")  # Separar por frases (simplesmente usando pontos finais)
            todas_as_frases.extend(frases)

        # Gerar embeddings para todas as frases
        frases_embeddings = self.model.encode(todas_as_frases)

        # Gerar o embedding da pergunta
        pergunta_embedding = self.model.encode([pergunta])

        # Calcular a similaridade entre a pergunta e cada frase
        similaridades = np.inner(pergunta_embedding, frases_embeddings)[0]

        # Ordenar as frases pela similaridade (da maior para a menor)
        frases_ordenadas = [frase for _, frase in sorted(zip(similaridades, todas_as_frases), reverse=True)]

        # Pegar as frases mais relevantes para montar a resposta
        resposta = " ".join(frases_ordenadas[:3])  # Pegamos as 3 frases mais relevantes

        return f"Resposta baseada nas informações mais relevantes: {resposta.strip()}"

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
