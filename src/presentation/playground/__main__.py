from presentation.playground import playground

if __name__ == "__main__":
    # Executar o playground usando a API correta do Agno
    print("🚀 Iniciando o playground...")
    if playground.teams:
        print(f"📊 Teams: {len(playground.teams)}")
    print("🌐 Acesse: https://app.agno.com/playground?endpoint=localhost%3A7777/v1")

    # Obter a aplicação FastAPI e servir
    app = playground.get_app()
    playground.serve(app=app, host="localhost", port=7777)
