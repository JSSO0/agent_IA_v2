import numpy as np

class GenerateAnswer:
    def __init__(self, index_generator):
        self.index_generator = index_generator

    def generate_answer(self, relevant_documents, question):
        response = ""
        all_phrases = []
        for document in relevant_documents:
            phrases = document.split(". ")
            all_phrases.extend(phrases)
        phrase_embeddings = self.model.encode(all_phrases)
        question_embedding = self.model.encode([question])
        similarities = np.inner(question_embedding, phrase_embeddings)[0]
        ordered_phrases = [phrase for _, phrase in sorted(zip(similarities, all_phrases), reverse=True)]
        response = " ".join(ordered_phrases[:3])
        return f"Answer based on the most relevant information: {response.strip()}"

    def query_index(self, query_text):
        if not self.nn_model or self.embeddings is None or not len(self.embeddings):
            raise ValueError("Index is not available. Create the index first.")
        query_embedding = self.model.encode([query_text])
        distances, indices = self.nn_model.kneighbors(query_embedding)
        similar_documents = [self.documents[idx] for idx in indices[0]]
        response = self.generate_answer(similar_documents, query_text)
        return response