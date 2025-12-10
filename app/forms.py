from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SelectField, IntegerField, FloatField, DateTimeField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo
from datetime import datetime

class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    first_name = StringField('Имя', validators=[DataRequired(), Length(min=2, max=50)])
    last_name = StringField('Фамилия', validators=[DataRequired(), Length(min=2, max=50)])
    password = PasswordField('Пароль', validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField('Подтвердите пароль', 
                                    validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Зарегистрироваться')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')

class EventForm(FlaskForm):
    title = StringField('Название мероприятия', validators=[DataRequired(), Length(max=200)])
    description = TextAreaField('Описание', validators=[DataRequired()])
    category = SelectField('Категория', choices=[
        ('Концерт', 'Концерт'),
        ('Мастер-класс', 'Мастер-класс'),
        ('Спорт', 'Спорт'),
        ('Встреча', 'Встреча'),
        ('Выставка', 'Выставка'),
        ('Фестиваль', 'Фестиваль'),
        ('Другое', 'Другое')
    ], validators=[DataRequired()])
    date = DateTimeField('Дата и время', 
                        validators=[DataRequired()], 
                        format='%Y-%m-%d %H:%M',
                        default=datetime.now)
    location = StringField('Место проведения', validators=[DataRequired(), Length(max=200)])
    max_participants = IntegerField('Максимальное количество участников', 
                                   validators=[DataRequired()], default=100)
    ticket_name = StringField('Название билета', validators=[DataRequired()], default='Стандартный')
    ticket_price = FloatField('Цена билета (руб.)', validators=[DataRequired()], default=0.0)
    submit = SubmitField('Создать мероприятие')

class BookingForm(FlaskForm):
    tickets_count = IntegerField('Количество', 
                                validators=[DataRequired()], 
                                default=1)
    submit = SubmitField('Забронировать')
