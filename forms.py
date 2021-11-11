from wtforms import StringField, SelectField, SelectMultipleField, DateTimeField, BooleanField
from wtforms.validators import DataRequired, URL, Optional, Regexp
from datetime import datetime
from flask_wtf import Form


genres = [
    ('Alternative', 'Alternative'),
    ('Blues', 'Blues'),
    ('Classical', 'Classical'),
    ('Country', 'Country'),
    ('Electronic', 'Electronic'),
    ('Folk', 'Folk'),
    ('Funk', 'Funk'),
    ('Hip-Hop', 'Hip-Hop'),
    ('Heavy Metal', 'Heavy Metal'),
    ('Instrumental', 'Instrumental'),
    ('Jazz', 'Jazz'),
    ('Musical Theatre', 'Musical Theatre'),
    ('Pop', 'Pop'),
    ('Punk', 'Punk'),
    ('R&B', 'R&B'),
    ('Reggae', 'Reggae'),
    ('Rock n Roll', 'Rock n Roll'),
    ('Soul', 'Soul'),
    ('Other', 'Other'),
]

states = [
    ('AL', 'AL'),
    ('AK', 'AK'),
    ('AZ', 'AZ'),
    ('AR', 'AR'),
    ('CA', 'CA'),
    ('CO', 'CO'),
    ('CT', 'CT'),
    ('DE', 'DE'),
    ('DC', 'DC'),
    ('FL', 'FL'),
    ('GA', 'GA'),
    ('HI', 'HI'),
    ('ID', 'ID'),
    ('IL', 'IL'),
    ('IN', 'IN'),
    ('IA', 'IA'),
    ('KS', 'KS'),
    ('KY', 'KY'),
    ('LA', 'LA'),
    ('ME', 'ME'),
    ('MT', 'MT'),
    ('NE', 'NE'),
    ('NV', 'NV'),
    ('NH', 'NH'),
    ('NJ', 'NJ'),
    ('NM', 'NM'),
    ('NY', 'NY'),
    ('NC', 'NC'),
    ('ND', 'ND'),
    ('OH', 'OH'),
    ('OK', 'OK'),
    ('OR', 'OR'),
    ('MD', 'MD'),
    ('MA', 'MA'),
    ('MI', 'MI'),
    ('MN', 'MN'),
    ('MS', 'MS'),
    ('MO', 'MO'),
    ('PA', 'PA'),
    ('RI', 'RI'),
    ('SC', 'SC'),
    ('SD', 'SD'),
    ('TN', 'TN'),
    ('TX', 'TX'),
    ('UT', 'UT'),
    ('VT', 'VT'),
    ('VA', 'VA'),
    ('WA', 'WA'),
    ('WV', 'WV'),
    ('WI', 'WI'),
    ('WY', 'WY'),
]


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
        choices=states
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
        choices=genres
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
        choices=states
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
        choices=genres
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
