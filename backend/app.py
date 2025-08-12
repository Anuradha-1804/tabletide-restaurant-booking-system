from flask import Flask, render_template, request, jsonify
from datetime import datetime
from models import db, Booking
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__, static_folder='../frontend/static', template_folder='../frontend/templates')

# Get the database URL from the environment variable.
# This keeps your sensitive information secure.
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Create database tables if they don't exist
with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/book', methods=['POST'])
def book_table():
    data = request.json
    name = data.get('name')
    email = data.get('email')
    date_str = data.get('date')
    time_str = data.get('time')
    table_number = data.get('table_number')

    if not all([name, email, date_str, time_str, table_number]):
        return jsonify({'message': 'All fields are required.'}), 400

    try:
        booking_datetime = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")

        existing_booking = Booking.query.filter_by(
            table_number=table_number, booking_datetime=booking_datetime
        ).first()

        if existing_booking:
            return jsonify({'message': 'This table is already booked at this time.'}), 409

        new_booking = Booking(
            name=name,
            email=email,
            booking_datetime=booking_datetime,
            table_number=table_number
        )
        db.session.add(new_booking)
        db.session.commit()
        
        return jsonify({'message': 'Booking successful!', 'booking_id': new_booking.id}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'An error occurred during booking.', 'error': str(e)}), 500

@app.route('/api/bookings', methods=['GET'])
def get_bookings():
    bookings = Booking.query.order_by(Booking.booking_datetime).all()
    bookings_list = []
    for booking in bookings:
        bookings_list.append({
            'name': booking.name,
            'email': booking.email,
            'datetime': booking.booking_datetime.isoformat(),
            'table_number': booking.table_number
        })
    return jsonify(bookings_list)

if __name__ == '__main__':
    app.run(debug=True)