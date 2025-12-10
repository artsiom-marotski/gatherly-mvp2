from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    avatar = db.Column(db.String(200))
    is_verified = db.Column(db.Boolean, default=True)  # В MVP сразу верифицируем
    is_organizer = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    events = db.relationship('Event', backref='organizer', lazy=True)
    bookings = db.relationship('Booking', backref='user', lazy=True)

class Event(db.Model):
    __tablename__ = 'events'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    location = db.Column(db.String(200), nullable=False)
    image_url = db.Column(db.String(200), default='/static/images/default-event.jpg')
    max_participants = db.Column(db.Integer, default=100)
    is_published = db.Column(db.Boolean, default=True)  # В MVP сразу публикуем
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    organizer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    tickets = db.relationship('Ticket', backref='event', lazy=True)
    bookings = db.relationship('Booking', backref='event', lazy=True)

class Ticket(db.Model):
    __tablename__ = 'tickets'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False, default=0.0)
    quantity = db.Column(db.Integer, nullable=False, default=100)
    sold_count = db.Column(db.Integer, default=0)
    
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False)

class Booking(db.Model):
    __tablename__ = 'bookings'
    
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(20), default='confirmed')  # В MVP сразу подтверждаем
    tickets_count = db.Column(db.Integer, nullable=False, default=1)
    total_amount = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False)
    ticket_id = db.Column(db.Integer, db.ForeignKey('tickets.id'), nullable=False)

def init_db():
    db.create_all()
    
    # Тестовые данные
    if User.query.count() == 0:
        from werkzeug.security import generate_password_hash
        
        # Тестовый организатор
        organizer = User(
            email='organizer@example.com',
            password_hash=generate_password_hash('password123'),
            first_name='Иван',
            last_name='Организаторов',
            is_organizer=True
        )
        
        # Тестовый пользователь
        user = User(
            email='user@example.com',
            password_hash=generate_password_hash('password123'),
            first_name='Анна',
            last_name='Участникова'
        )
        
        db.session.add(organizer)
        db.session.add(user)
        db.session.commit()
        
        # Тестовые мероприятия
        from datetime import datetime, timedelta
        
        event1 = Event(
            title='Джазовый вечер в City Club',
            description='Приглашаем на незабываемый джазовый вечер с лучшими музыкантами города.',
            category='Концерт',
            date=datetime.now() + timedelta(days=10),
            location='Москва, ул. Тверская, 10',
            organizer_id=organizer.id
        )
        
        event2 = Event(
            title='Мастер-класс по керамике',
            description='Научитесь создавать керамические изделия своими руками.',
            category='Мастер-класс',
            date=datetime.now() + timedelta(days=15),
            location='Москва, Арбат, 25',
            organizer_id=organizer.id
        )
        
        db.session.add(event1)
        db.session.add(event2)
        db.session.commit()
        
        # Тестовые билеты
        ticket1 = Ticket(name='Стандартный', price=1500.00, quantity=100, event_id=event1.id)
        ticket2 = Ticket(name='VIP', price=3000.00, quantity=20, event_id=event1.id)
        ticket3 = Ticket(name='Участие', price=2500.00, quantity=20, event_id=event2.id)
        
        db.session.add_all([ticket1, ticket2, ticket3])
        db.session.commit()
