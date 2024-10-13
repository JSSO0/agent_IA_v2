class GenerateAnswer:
    def __init__(self, index_generator):
        self.index_generator = index_generator

    def generate_asnwer(self, documentos_relevantes, pergunta):
        resposta = ""
        todas_as_frases = []
        for doc in documentos_relevantes:
            frases = doc.split(". ")
            todas_as_frases.extend(frases)
        frases_embeddings = self.model.encode(todas_as_frases)
        pergunta_embedding = self.model.encode([pergunta])
        similaridades = np.inner(pergunta_embedding, frases_embeddings)[0]
        frases_ordenadas = [frase for _, frase in sorted(zip(similaridades, todas_as_frases), reverse=True)]
        resposta = " ".join(frases_ordenadas[:3])
        return f"Resposta baseada nas informações mais relevantes: {resposta.strip()}"
    
    def query_index(self, query_text):
        if not self.nn_model or self.embeddings is None or not len(self.embeddings):
            raise ValueError("O índice não está disponível. Crie o índice primeiro.")
        query_embedding = self.model.encode([query_text])
        distances, indices = self.nn_model.kneighbors(query_embedding)
        similar_documents = [self.documents[idx] for idx in indices[0]]
        resposta = self.gerar_resposta_estruturada(similar_documents, query_text)
        return resposta