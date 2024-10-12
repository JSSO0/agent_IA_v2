from admin.controller.adminRoutes import app 

def main():
    print("Inicializando a API Flask...")
    app.run(host='0.0.0.0', port=5000, debug=True)

if __name__ == "__main__":
    main()