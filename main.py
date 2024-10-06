from admin.controller.adminRoutes import app  # Importe o `app` do `adminRoutes.py`

def main():
    print("Inicializando a API Flask...")
    # Inicializar o Flask diretamente no main
    
    app.run(host='0.0.0.0', port=5000, debug=True)
    print("API Flask inicializada. Aguardando perguntas...")


if __name__ == "__main__":
    main()