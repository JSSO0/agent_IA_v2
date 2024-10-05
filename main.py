from backend.chatbot import Chatbot
import os

from services.index_generator import IndexGenerator

def create_index(pdf_path, index_path):
    """
    Função para criar o índice diretamente, sem interagir com o chatbot.
    """
    try:
        # Instanciar o IndexGenerator com o caminho do PDF
        index_generator = IndexGenerator(pdf_path=pdf_path, index_path=index_path)

        # Ler o conteúdo do PDF
        print(f"📄 Lendo o PDF: {pdf_path}")
        pdf_content = index_generator.read_pdf()

        # Criar o índice a partir do conteúdo do PDF
        print("🔄 Criando o índice...")
        index_generator.create_index(documents=pdf_content)

        # Salvar o índice
        print(f"💾 Salvando o índice em: {index_path}")
        index_generator.save_index()

        print(f"✅ Índice criado e salvo com sucesso em '{index_path}'")
    except Exception as e:
        print(f"⚠️ Erro ao criar o índice: {str(e)}")
def main():
    # Caminho para o PDF e o índice (altere conforme o caminho do seu arquivo PDF)
    pdf_path = "./DocumentodeExemploParaTestes.pdf"
    index_path = "./index.json"

    # Inicializar o chatbot com o caminho para o PDF e/ou o índice salvo
    #chatbot = Chatbot(pdf_path=pdf_path, index_path=index_path)

    # Verificar e criar o índice, se necessário
    #create_index_if_not_exists(chatbot)
    create_index(pdf_path, index_path)

    # Loop de perguntas para interação com o usuário
   
    """
    while True:
        question = input("Pergunte algo sobre o PDF: ")
        if question.lower() in ["sair", "exit", "quit"]:
            print("👋 Encerrando o chatbot. Até mais!")
            break

        # Obter a resposta do chatbot
        response = chatbot.get_response(question)
        print(f"🤖 Resposta: {response}")
    """

if __name__ == "__main__":
    main()