from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# 'Booking' नावाचा डेटाबेस टेबल तयार करतो
class Booking(db.Model):
    __tablename__ = 'bookings'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    booking_datetime = db.Column(db.DateTime, nullable=False)
    table_number = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<Booking {self.name}>'