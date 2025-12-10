from flask import Flask, render_template, Blueprint
from flask_login import LoginManager, current_user

from .database import db, init_db, User
from .auth import auth_bp
from .events import events_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    
    # Инициализация расширений
    db.init_app(app)
    
    # Flask-Login
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Пожалуйста, войдите для доступа к этой странице.'
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    # Регистрация Blueprint'ов
    app.register_blueprint(auth_bp)
    app.register_blueprint(events_bp)
    
    # Основные маршруты
    @app.route('/')
    def index():
        return render_template('index.html')
    
    @app.route('/dashboard')
    @current_user.authenticated
    def dashboard():
        bookings = current_user.bookings
        return render_template('dashboard.html', 
                             user=current_user, 
                             bookings=bookings)
    
    @app.route('/profile')
    @current_user.authenticated
    def profile():
        return render_template('profile.html', user=current_user)
    
    # Статус приложения
    @app.route('/health')
    def health():
        return {'status': 'ok', 'service': 'gatherly-mvp'}
    
    return app

# Создание таблиц
def setup_database(app):
    with app.app_context():
        init_db()
