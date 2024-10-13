from flask import Flask
from admin.controller import adminRoutes
from chatbot.controller import chatbotRoutes

app = Flask(__name__)

app.register_blueprint(adminRoutes)
app.register_blueprint(chatbotRoutes)

def main():
    print("Inicializando a API Flask...")
    app.run(host='0.0.0.0', port=5000, debug=True)

if __name__ == "__main__":
    main()