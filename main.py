from backend.chatbot import Chatbot

def main():
    # Caminho para o PDF e o índice (altere conforme o caminho do seu arquivo PDF)
    pdf_path = "./DocumentodeExemploParaTestes.pdf"
    index_path = "./meu_indice.json"

    # Inicializar o chatbot com o caminho para o PDF e/ou o índice salvo
    chatbot = Chatbot(pdf_path=pdf_path, index_path=index_path)

    # Loop de perguntas para interação com o usuário
    while True:
        question = input("Pergunte algo sobre o PDF: ")
        if question.lower() in ["sair", "exit", "quit"]:
            print("👋 Encerrando o chatbot. Até mais!")
            break

        # Obter a resposta do chatbot
        response = chatbot.get_response(question)
        print(f"🤖 Resposta: {response}")

if __name__ == "__main__":
    main()