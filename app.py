from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Модель для записей на приём
class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100))
    doctor = db.Column(db.String(50), nullable=False)
    date = db.Column(db.String(20), nullable=False)
    time = db.Column(db.String(10), nullable=False)
    message = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Appointment {self.patient_name}>'

# Модель для врачей
class Doctor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    specialty = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    image_url = db.Column(db.String(200))
    is_active = db.Column(db.Boolean, default=True)

# Создаём таблицы
with app.app_context():
    db.create_all()
    # Добавляем тестовых врачей, если их нет
    if Doctor.query.count() == 0:
        doctors = [
            Doctor(name='Др. Иванов Иван', specialty='Кардиолог',
                   description='Опытный кардиолог с 15-летним стажем',
                   image_url='https://via.placeholder.com/150/4CAF50/white?text=Cardio'),
            Doctor(name='Др. Петрова Анна', specialty='Невролог',
                   description='Специалист по заболеваниям нервной системы',
                   image_url='https://via.placeholder.com/150/2196F3/white?text=Neuro'),
            Doctor(name='Др. Сидоров Сергей', specialty='Ортопед',
                   description='Лечение заболеваний опорно-двигательного аппарата',
                   image_url='https://via.placeholder.com/150/FF9800/white?text=Ortho'),
        ]
        for d in doctors:
            db.session.add(d)
        db.session.commit()

@app.route('/')
def index():
    doctors = Doctor.query.filter_by(is_active=True).all()
    return render_template('index.html', doctors=doctors)

@app.route('/appointments', methods=['GET', 'POST'])
def appointments():
    if request.method == 'POST':
        try:
            appointment = Appointment(
                patient_name=request.form.get('name'),
                phone=request.form.get('phone'),
                email=request.form.get('email'),
                doctor=request.form.get('doctor'),
                date=request.form.get('date'),
                time=request.form.get('time'),
                message=request.form.get('message')
            )
            db.session.add(appointment)
            db.session.commit()
            return jsonify({'success': True, 'message': 'Запись успешно создана!'})
        except Exception as e:
            return jsonify({'success': False, 'message': str(e)}), 400

    doctors = Doctor.query.filter_by(is_active=True).all()
    return render_template('appointments.html', doctors=doctors)

@app.route('/admin')
def admin():
    appointments = Appointment.query.order_by(Appointment.created_at.desc()).all()
    doctors = Doctor.query.all()
    return render_template('admin.html', appointments=appointments, doctors=doctors)

@app.route('/api/appointments', methods=['GET'])
def get_appointments():
    appointments = Appointment.query.order_by(Appointment.created_at.desc()).all()
    return jsonify([{
        'id': a.id,
        'patient_name': a.patient_name,
        'phone': a.phone,
        'email': a.email,
        'doctor': a.doctor,
        'date': a.date,
        'time': a.time,
        'message': a.message,
        'created_at': a.created_at.strftime('%Y-%m-%d %H:%M')
    } for a in appointments])

@app.route('/api/appointments/<int:id>', methods=['DELETE'])
def delete_appointment(id):
    appointment = Appointment.query.get_or_404(id)
    db.session.delete(appointment)
    db.session.commit()
    return jsonify({'success': True})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)