from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from datetime import datetime

from .database import db, Event, Ticket, Booking, User
from .forms import EventForm, BookingForm

events_bp = Blueprint('events', __name__)

@events_bp.route('/events')
def events_list():
    category = request.args.get('category')
    search = request.args.get('search')
    
    query = Event.query.filter_by(is_published=True)
    
    if category and category != 'all':
        query = query.filter_by(category=category)
    
    if search:
        query = query.filter(
            (Event.title.ilike(f'%{search}%')) | 
            (Event.description.ilike(f'%{search}%'))
        )
    
    events = query.order_by(Event.date.asc()).all()
    
    # Получаем уникальные категории
    categories = db.session.query(Event.category).distinct().all()
    categories = [cat[0] for cat in categories]
    
    return render_template('events.html', 
                         events=events, 
                         categories=categories,
                         selected_category=category)

@events_bp.route('/events/<int:event_id>')
def event_detail(event_id):
    event = Event.query.get_or_404(event_id)
    
    if not event.is_published and (not current_user.is_authenticated or 
                                  current_user.id != event.organizer_id):
        flash('Мероприятие не найдено или недоступно', 'error')
        return redirect(url_for('events.events_list'))
    
    form = BookingForm()
    
    return render_template('event_detail.html', 
                         event=event, 
                         form=form)

@events_bp.route('/events/<int:event_id>/book', methods=['POST'])
@login_required
def book_event(event_id):
    event = Event.query.get_or_404(event_id)
    form = BookingForm()
    
    if not event.is_published:
        flash('Мероприятие недоступно для бронирования', 'error')
        return redirect(url_for('events.event_detail', event_id=event_id))
    
    if form.validate_on_submit():
        # Берем первый доступный билет
        ticket = event.tickets[0] if event.tickets else None
        
        if not ticket:
            flash('Нет доступных билетов', 'error')
            return redirect(url_for('events.event_detail', event_id=event_id))
        
        if ticket.sold_count >= ticket.quantity:
            flash('К сожалению, все билеты проданы', 'error')
            return redirect(url_for('events.event_detail', event_id=event_id))
        
        # Создание бронирования
        booking = Booking(
            user_id=current_user.id,
            event_id=event_id,
            ticket_id=ticket.id,
            tickets_count=form.tickets_count.data,
            total_amount=ticket.price * form.tickets_count.data,
            status='confirmed'
        )
        
        db.session.add(booking)
        ticket.sold_count += form.tickets_count.data
        db.session.commit()
        
        flash(f'Бронирование успешно! Стоимость: {booking.total_amount} руб.', 'success')
        return redirect(url_for('user.dashboard'))
    
    return render_template('event_detail.html', event=event, form=form)

@events_bp.route('/events/create', methods=['GET', 'POST'])
@login_required
def create_event():
    if not current_user.is_organizer:
        current_user.is_organizer = True
        db.session.commit()
        flash('Теперь вы организатор!', 'success')
    
    form = EventForm()
    
    if form.validate_on_submit():
        event = Event(
            title=form.title.data,
            description=form.description.data,
            category=form.category.data,
            date=form.date.data,
            location=form.location.data,
            max_participants=form.max_participants.data,
            organizer_id=current_user.id
        )
        
        db.session.add(event)
        db.session.commit()
        
        # Создаем билет
        ticket = Ticket(
            name=form.ticket_name.data,
            price=form.ticket_price.data,
            quantity=form.max_participants.data,
            event_id=event.id
        )
        db.session.add(ticket)
        db.session.commit()
        
        flash('Мероприятие успешно создано!', 'success')
        return redirect(url_for('events.event_detail', event_id=event.id))
    
    return render_template('create_event.html', form=form)

@events_bp.route('/api/events')
def api_events():
    events = Event.query.filter_by(is_published=True).all()
    
    events_data = []
    for event in events:
        available_tickets = sum(t.quantity - t.sold_count for t in event.tickets)
        
        events_data.append({
            'id': event.id,
            'title': event.title,
            'description': event.description[:100] + '...' if len(event.description) > 100 else event.description,
            'category': event.category,
            'date': event.date.isoformat() if event.date else None,
            'location': event.location,
            'image_url': event.image_url,
            'organizer': event.organizer.first_name + ' ' + event.organizer.last_name,
            'available_tickets': available_tickets,
            'price': event.tickets[0].price if event.tickets else 0
        })
    
    return jsonify(events_data)
