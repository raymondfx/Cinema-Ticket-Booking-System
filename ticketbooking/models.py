from ticketbooking import db


class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False, unique=False)
    email = db.Column(db.String(120), unique=False, nullable=False)
    booked_tickets = db.relationship(
        "BookedTickets", backref="tickets_owner", lazy=True
    )

    def __repr__(self):
        return f"Booking('{self.name}','{self.email}')"


class BookedTickets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    seat_no = db.Column(db.Integer, nullable=False)
    booking_id = db.Column(db.Integer, db.ForeignKey("booking.id"), nullable=False)

    def __repr__(self):
        return f"BookedTickets('{self.seat_no}')"
