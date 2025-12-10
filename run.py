from app.main import create_app, setup_database

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        setup_database(app)
    print("🚀 Gatherly MVP запущен!")
    print("📂 База данных инициализирована")
    print("🌐 Откройте http://localhost:5000 в браузере")
    app.run(debug=True, host='0.0.0.0', port=5000)
