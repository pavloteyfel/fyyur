from wtforms.validators import DataRequired, URL, Optional
from flask_wtf import FlaskForm
from enums import Genre, State
from datetime import datetime
from wtforms import (
    StringField,
    SelectField,
    SelectMultipleField,
    DateTimeField,
    BooleanField,
)

import re


def is_valid_phone(number):
    """Validate phone numbers like:
    1234567890 - no space
    123.456.7890 - dot separator
    123-456-7890 - dash separator
    123 456 7890 - space separator

    Patterns:
    000 = [0-9]{3}
    0000 = [0-9]{4}
    -.  = ?[-. ]

    Note: (? = optional) - Learn more: https://regex101.com/
    """
    regex = re.compile("^\(?([0-9]{3})\)?[-. ]?([0-9]{3})[-. ]?([0-9]{4})$")
    return regex.match(number)


class ShowForm(FlaskForm):
    """
    All show page form fields and related validation rules.
    """

    artist_id = SelectField("artist_id", validate_choice=False, choices=[])
    venue_id = SelectField("venue_id", validate_choice=False, choices=[])
    start_time = DateTimeField("start_time", default=datetime.today())


class VenueForm(FlaskForm):
    """
    All venue page form fields and related validation rules.
    """

    name = StringField("name", validators=[DataRequired()])
    city = StringField("city", validators=[DataRequired()])
    state = SelectField("state", validators=[DataRequired()], choices=State.choices())
    address = StringField("address", validators=[DataRequired()])
    phone = StringField("phone", validators=[DataRequired()])
    image_link = StringField(
        "image_link",
        validators=[URL(message="Invalid Image Link"), Optional()],
        default="https://placeimg.com/640/480/arch",
    )
    genres = SelectMultipleField(
        "genres", validators=[DataRequired()], choices=Genre.choices()
    )
    facebook_link = StringField(
        "Facebook Link",
        validators=[URL(message="Invalid Facebook Link"), Optional()],
        default="https://facebook.com",
    )
    website = StringField(
        "website", validators=[URL(message="Invalid Website Link"), Optional()]
    )
    seeking_talent = BooleanField("seeking_talent")
    seeking_description = StringField("seeking_description")

    def validate(self):
        """Custom validate method for phone, genre and state"""
        rv = FlaskForm.validate(self)
        if not rv:
            return False
        if not is_valid_phone(self.phone.data):
            self.phone.errors.append("Invalid phone.")
            return False
        if not set(self.genres.data).issubset(dict(Genre.choices()).keys()):
            self.genres.errors.append("Invalid genres.")
            return False
        if self.state.data not in dict(State.choices()).keys():
            self.state.errors.append("Invalid state.")
            return False
        return True


class ArtistForm(FlaskForm):
    """
    Artist page form fields and related validation rules.
    """

    name = StringField("name", validators=[DataRequired()])
    city = StringField("city", validators=[DataRequired()])
    state = SelectField("state", validators=[DataRequired()], choices=State.choices())
    phone = StringField("phone", validators=[DataRequired()])
    image_link = StringField(
        "image_link",
        validators=[URL(message="Invalid Image Link"), Optional()],
        default="https://placeimg.com/640/480/people/sepia",
    )
    genres = SelectMultipleField(
        "genres", validators=[DataRequired()], choices=Genre.choices()
    )
    facebook_link = StringField(
        "facebook_link",
        validators=[URL(message="Invalid Facebook Link"), Optional()],
        default="https://facebook.com",
    )
    website = StringField(
        "website", validators=[URL(message="Invalid Website Link"), Optional()]
    )
    seeking_venue = BooleanField("seeking_venue")
    seeking_description = StringField("seeking_description")

    def validate(self):
        """Custom validate method for phone, genre and state"""
        rv = FlaskForm.validate(self)
        if not rv:
            return False
        if not is_valid_phone(self.phone.data):
            self.phone.errors.append("Invalid phone.")
            return False
        if not set(self.genres.data).issubset(dict(Genre.choices()).keys()):
            self.genres.errors.append("Invalid genres.")
            return False
        if self.state.data not in dict(State.choices()).keys():
            self.state.errors.append("Invalid state.")
            return False
        return True
