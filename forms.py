from wtforms import StringField, SelectField, SelectMultipleField, DateTimeField, BooleanField
from wtforms.validators import DataRequired, URL, Optional, Regexp
from flask_wtf import FlaskForm as Form
from enums import Genre, State
from datetime import datetime


class ShowForm(Form):
    artist_id = SelectField('artist_id', validate_choice=False, choices=[])
    venue_id = SelectField('venue_id', validate_choice=False, choices=[])
    start_time = DateTimeField('start_time', default=datetime.today())


class VenueForm(Form):
    name = StringField(
        'name', validators=[DataRequired()]
    )
    city = StringField(
        'city', validators=[DataRequired()]
    )
    state = SelectField(
        'state', validators=[DataRequired()],
        choices=State.choices()
    )
    address = StringField(
        'address', validators=[DataRequired()]
    )
    phone = StringField(
        'phone', validators=[DataRequired(), 
            Regexp('^(\([0-9]{3}\) |[0-9]{3}-)[0-9]{3}-[0-9]{4}$',
            message='Invalid phone number format')]
    )
    image_link = StringField(
        'image_link', validators=[URL(message='Invalid Image Link'), 
            Optional()], default='https://placeimg.com/640/480/arch'
    )
    genres = SelectMultipleField(
        'genres', validators=[DataRequired()],
        choices=Genre.choices()
    )
    facebook_link = StringField(
        'Facebook Link', validators=[URL(message='Invalid Facebook Link'), 
            Optional()], default='https://facebook.com'
    )
    website = StringField(
        'website', validators=[URL(message='Invalid Website Link'), 
            Optional()]
    )
    seeking_talent = BooleanField('seeking_talent')
    seeking_description = StringField('seeking_description')


class ArtistForm(Form):
    name = StringField(
        'name', validators=[DataRequired()]
    )
    city = StringField(
        'city', validators=[DataRequired()]
    )
    state = SelectField(
        'state', validators=[DataRequired()],
        choices=State.choices()
    )
    phone = StringField(
        'phone', validators=[DataRequired(), 
            Regexp('^(\([0-9]{3}\) |[0-9]{3}-)[0-9]{3}-[0-9]{4}$', 
            message='Invalid phone number format')]
    )
    image_link = StringField(
        'image_link', validators=[URL(message='Invalid Image Link'), 
            Optional()], default='https://placeimg.com/640/480/people/sepia'
    )
    genres = SelectMultipleField(
        'genres', validators=[DataRequired()],
        choices=Genre.choices()
     )
    facebook_link = StringField(
        'facebook_link', validators=[URL(message='Invalid Facebook Link'), 
            Optional()], default='https://facebook.com'
     )
    website = StringField(
        'website', validators=[URL(message='Invalid Website Link'), Optional()]
     )
    seeking_venue = BooleanField('seeking_venue')
    seeking_description = StringField('seeking_description')
