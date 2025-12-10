# config.py
import os

class Config:
    # Обязательные настройки
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    # База данных (Railway автоматически добавляет DATABASE_URL)
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///app.db')
    
    # Если Railway использует PostgreSQL с postgres://, нужно преобразовать
    if SQLALCHEMY_DATABASE_URI and SQLALCHEMY_DATABASE_URI.startswith('postgres://'):
        SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace('postgres://', 'postgresql://', 1)
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Дополнительные настройки
    DEBUG = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
