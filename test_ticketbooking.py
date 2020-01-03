import unittest
from ticketbooking import db, app, mail
from ticketbooking.models import Booking, BookedTickets


class Testing(unittest.TestCase):
    def setUp(self):
        app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:root@localhost/cinematicketbooking"
        self.app = app.test_client()
        db.drop_all()
        db.create_all()
        mail.init_app(app)
        self.assertEqual(app.debug, False)

    def test_booking(self):
        response = self.confirm_booking("sourabh", "sourabh123@gmail.com", ["1,2"])
        self.assertEqual(response.status_code, 200)

    def test_replicated_booking(self):
        seat_nos = [1, 2, 3]

        booking = Booking(name="sourabh", email="sourabh123@gmail.com")
        db.session.add(booking)
        db.session.commit()
        for seat_no in seat_nos:
            booked_seat = BookedTickets(booking_id=booking.id, seat_no=seat_no)
            db.session.add(booked_seat)
            db.session.commit()

        response = self.confirm_booking("sourabh", "sourabh123@gmail.com", ["1,2,3"])
        self.assertEqual(response.status_code, 200)

    def testing_name_error(self):
        response = self.confirm_booking("", "sourabh123@gmail.com", ["1,2,3"])
        self.assertEqual(response.status_code, 200)

    def testing_email_error(self):
        response = self.confirm_booking("sourabh", "", ["1,2"])
        self.assertEqual(response.status_code, 200)

    def testing_seat_no_error(self):
        response = self.confirm_booking("sourabh", "sourabh123@gmail.com", None)
        self.assertEqual(response.status_code, 200)

    def confirm_booking(self, name, email, seat_no):
        return self.app.post(
            "/confirm_booking/",
            data=dict(name=name, email=email, seat_no=seat_no),
            follow_redirects=True,
        )

    def testing_booking_cancellation(self):
        response = self.booking_cancellation("sourabh123@gmail.com", [1])
        self.assertEqual(response.status_code, 200)

    def testing_booking_cancellation_seat_no_error(self):
        response = self.booking_cancellation("sourabh123@gmail.com", [9])
        self.assertEqual(response.status_code, 200)

    def testing_booking_cancellation_email_error(self):
        response = self.booking_cancellation("sourabh123@gmail.com", [1])
        self.assertEqual(response.status_code, 200)

    def booking_cancellation(self, email, seat_nos):
        seats = [1, 2, 3, 4, 5, 6]

        booking = Booking(name="sourabh", email="sourabh123@gmail.com")
        db.session.add(booking)
        db.session.commit()

        for seat_no in seats:
            booked_seat = BookedTickets(booking_id=booking.id, seat_no=seat_no)
            db.session.add(booked_seat)
            db.session.commit()

        return self.app.post(
            "/booking_cancellation/",
            data=dict(email=email, seat_no=seat_nos),
            follow_redirects=True,
        )


if __name__ == "__main__":
    unittest.main()
