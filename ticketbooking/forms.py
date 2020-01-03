from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email, ValidationError


class BookingForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    submit = SubmitField("Confirm Booking")

    def validate_name(self, name):
        if name.data is None:
            raise ValidationError("Name field is required.")

    def validate_email(self, email):
        if email.data is None:
            raise ValidationError("Email field is required.")
