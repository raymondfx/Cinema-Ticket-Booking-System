import json
from ticketbooking import app, db, mail
from ticketbooking.models import Booking, BookedTickets
from flask import render_template, redirect, url_for, request, jsonify
from ticketbooking.forms import BookingForm
from flask_mail import Message


@app.route("/")
@app.route("/home")
def home():
    try:
        no_of_seats = 20
        form = BookingForm()
        list_of_seats = []  # List of Booked Seats
        seats = (
            BookedTickets.query.all()
        )  # Query get all the seats that are booked.The result will be in tuple form so
        # we'll convert it into list
        for seat in seats:  # Appending tuple data in list
            list_of_seats.append(seat.seat_no)
        return render_template(
            "layout.html",
            no_of_seats=no_of_seats,
            form=form,
            list_of_seats=list_of_seats,
            seats=seats,
        )
    except Exception as e:
        return redirect(url_for("home"))


def get_seats_html():
    seats = BookedTickets.query.all()
    list_of_seats = []  # List of Booked Seats

    for row in seats:
        list_of_seats.append(row.seat_no)

    no_of_seats = 20
    seats_html = render_template(
        "seats.html", no_of_seats=no_of_seats, list_of_seats=list_of_seats
    )
    return seats_html


@app.route("/confirm_booking/", methods=["GET", "POST"])
def confirm_booking():
    try:
        form = BookingForm()
        total_booked_seats = request.form.getlist("seat_no")
        new_list = []
        email = request.form["email"]
        for e in total_booked_seats:
            for sub_e in e.split(","):
                new_list.append(sub_e)
        if form.validate_on_submit():
            if request.method == "POST":
                booking_information = Booking(name=request.form["name"], email=email)
                db.session.add(booking_information)
                db.session.commit()

                for seat in new_list:
                    booked_seat = BookedTickets(
                        seat_no=seat, booking_id=booking_information.id
                    )
                    db.session.add(booked_seat)
                    db.session.commit()

                if booking_information:
                    seats_html = get_seats_html()
                    send_mail = [email]
                    send_email(
                        send_mail,
                        "<p>Seat numbers booked by you are: {}.</p>".format(
                            ", ".join(total_booked_seats)
                        ),
                    )
                    return (
                        json.dumps(
                            {
                                "status": True,
                                "msg": "Booking Confirmed",
                                "seats_html": seats_html,
                            }
                        ),
                        200,
                    )
        else:
            errors_string = ""
            for field, errors in form.errors.items():
                errors_string += field + " : " + ", ".join(errors) + "\n"
                seats_html = get_seats_html()
                return (
                    jsonify(
                        {
                            "status": False,
                            "msg": errors_string,
                            "seats_html": seats_html,
                        }
                    ),
                    404,
                )
    except Exception as e:
        return redirect(url_for("home"))


def send_email(send_mail, message):
    msg = Message(
        "Cinema Ticket Booking",
        sender=app.config["MAIL_USERNAME"],
        recipients=send_mail,
    )
    msg.html = message
    mail.send(msg)


@app.route("/booking_cancellation/", methods=["POST"])
def booking_cancellation():
    try:
        seats = request.form.getlist("seat_no")
        email = request.form.get("email")

        if seats:
            booking = (
                Booking.query.join(
                    BookedTickets, Booking.id == BookedTickets.booking_id
                )
                .filter(BookedTickets.seat_no == seats, Booking.email == email)
                .first()
            )
        if booking:
            booking_id = booking.id
            booked_seats = BookedTickets.query.filter_by(booking_id=booking_id).all()
            if len(seats) == len(booked_seats):
                BookedTickets.query.filter_by(booking_id=booking_id).delete()
                Booking.query.filter_by(id=booking_id).delete()
                db.session.commit()
            else:
                for seat in seats:
                    BookedTickets.query.filter_by(seat_no=seat).delete()
                    db.session.commit()
            seats_html = get_seats_html()
            return (
                json.dumps(
                    {
                        "status": True,
                        "msg": "Ticket cancellation confirmed",
                        "seats_html": seats_html,
                    }
                ),
                200,
            )
        else:
            seats_html = get_seats_html()
            return (
                json.dumps(
                    {
                        "status": False,
                        "msg": "Ticket cancellation rejected. Please fill the correct email",
                        "seats_html": seats_html,
                    }
                ),
                404,
            )
    except Exception as e:
        return redirect(url_for("home"))
