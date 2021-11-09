#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

from flask import Flask, render_template, request, flash, redirect, url_for
from forms import ArtistForm, VenueForm, ShowForm
from sqlalchemy.ext.hybrid import hybrid_property
from logging import Formatter, FileHandler
from flask_moment import Moment
from flask_wtf import Form
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

import dateutil.parser
import logging
import babel
import json
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)


class Venue(db.Model):
  __tablename__ = 'Venue'

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(120), nullable=False)
  city = db.Column(db.String(120), nullable=False)
  state = db.Column(db.String(120), nullable=False)
  address = db.Column(db.String(120), nullable=False)
  phone = db.Column(db.String(120))
  genres = db.Column(db.ARRAY(db.String(500)), nullable=False)
  facebook_link = db.Column(db.String(500))
  image_link = db.Column(db.String(500))
  website = db.Column(db.String(500))
  seeking_talent = db.Column(db.Boolean, nullable=False, default=False)
  seeking_description = db.Column(db.String(500))
  shows = db.relationship('Show', back_populates='venue', 
    cascade='all, delete', lazy='joined')


  @hybrid_property
  def upcoming_shows(self):
    return [show for show in self.shows if show._start_time > datetime.now()]


  @hybrid_property
  def past_shows(self):
    return [show for show in self.shows if show._start_time < datetime.now()]


  @hybrid_property
  def upcoming_shows_count(self):
    return len(self.upcoming_shows)


  @hybrid_property
  def past_shows_count(self):
    return len(self.past_shows)


  def update(self, data):
    for key, value in data.items():
      setattr(self, key, value)

  
  def __repr__(self):
      return f'<Venue {self.id}, {self.name}>'


class Artist(db.Model):
  __tablename__ = 'Artist'

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(120), nullable=False)
  city = db.Column(db.String(120), nullable=False)
  state = db.Column(db.String(120), nullable=False)
  phone = db.Column(db.String(120))
  genres = db.Column(db.ARRAY(db.String(500)), nullable=False)
  facebook_link = db.Column(db.String(500))
  image_link = db.Column(db.String(500))
  website = db.Column(db.String(500))
  seeking_venue = db.Column(db.Boolean, nullable=False, default=False)
  seeking_description = db.Column(db.String(500))
  shows = db.relationship('Show', back_populates='artist',
    cascade='all, delete', lazy='joined')


  @hybrid_property
  def upcoming_shows(self):
    return [show for show in self.shows if show._start_time > datetime.now()]


  @hybrid_property
  def past_shows(self):
    return [show for show in self.shows if show._start_time < datetime.now()]


  @hybrid_property
  def upcoming_shows_count(self):
    return len(self.upcoming_shows)


  @hybrid_property
  def past_shows_count(self):
    return len(self.past_shows)


  def update(self, data):
    for key, value in data.items():
      setattr(self, key, value)


  def __repr__(self):
    return f'<Artist {self.id}, {self.name}>'


class Show(db.Model):
  __tablename__ = 'Show'

  id = db.Column(db.Integer, primary_key=True)
  artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'), nullable=False)
  venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'), nullable=False)
  _start_time = db.Column(db.DateTime, nullable=False)
  artist = db.relationship('Artist', back_populates='shows')
  venue = db.relationship('Venue', back_populates='shows')


  @property
  def start_time(self):
    return self._start_time.strftime('%Y-%m-%d %H:%M:%S')


  @start_time.setter
  def start_time(self, value):
    self._start_time = value


  def __repr__(self):
    return f'<Show {self.id}, Artist {self.artist_id}, Venue {self.venue_id}>'


def populate():
  import workbench
  db.drop_all()
  db.create_all()

  for artist in workbench.artists:
    a = Artist(**artist)
    db.session.add(a)

  for venue in workbench.venues:
    v = Venue(**venue)
    db.session.add(v)

  for show in workbench.shows:
    s = Show(**show)
    db.session.add(s)

  db.session.commit()
  db.session.close()

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
    format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
    format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime


#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  venues = Venue.query.all()
  places = Venue.query.distinct(Venue.city, Venue.state).all()
  areas = []
  for place in places:
      areas.append({
          'city': place.city,
          'state': place.state,
          'venues': [{
              'id': venue.id,
              'name': venue.name,
          } for venue in venues if venue.city == place.city 
            and venue.state == place.state]
      })
  return render_template('pages/venues.html', areas=areas)

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  response={
    "count": 1,
    "data": [{
      "id": 2,
      "name": "The Dueling Pianos Bar",
      "num_upcoming_shows": 0,
    }]
  }
  return render_template('pages/search_venues.html', 
    results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  return render_template('pages/show_venue.html', 
    venue=Venue.query.get(venue_id))

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  try:
    # new_venue.html: website_link renamed website to be consistent
    form_data = VenueForm(request.form).to_dict()
    db.session.add(Venue(**form_data))
    db.session.commit()
    flash(f"Venue {request.form['name']} was successfully listed!")
  except Exception as e:
    print(e)
    flash(f"An error occurred. Venue {request.form['name']} could not be listed.")
  finally:
    db.session.close()
  return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  return None

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  return render_template('pages/artists.html', 
    artists=Artist.query.all())

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  response={
    "count": 1,
    "data": [{
      "id": 4,
      "name": "Guns N Petals",
      "num_upcoming_shows": 0,
    }]
  }
  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  return render_template('pages/show_artist.html', 
    artist=Artist.query.get(artist_id))

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  artist = Artist.query.get(artist_id)
  form = ArtistForm(**vars(artist))
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  try:
    artist = Artist.query.get(artist_id)
    form_data = ArtistForm(request.form).to_dict()
    artist.update(form_data)
    db.session.commit()
    flash(f"Artist {request.form['name']} was successfully updated!")
  except Exception as e:
    print(e)
    flash(f"An error occurred. Artist {request.form['name']} could not be updated.")
  finally:
    db.session.close()

  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  venue = Venue.query.get(venue_id)
  form = VenueForm(**vars(venue))
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  try:
    venue = Venue.query.get(venue_id)
    form_data = VenueForm(request.form).to_dict()
    venue.update(form_data)
    db.session.commit()
    flash(f"Venue {request.form['name']} was successfully updated!")
  except Exception as e:
    print(e)
    flash(f"An error occurred. Venue {request.form['name']} could not be updated.")
  finally:
    db.session.close()
  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  return render_template('forms/new_artist.html', form=ArtistForm())

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  try:
    # new_artist.html: website_link renamed website to be consistent
    form_data = ArtistForm(request.form).to_dict()
    db.session.add(Artist(**form_data))
    db.session.commit()
    flash(f"Artist {request.form['name']} was successfully listed!")
  except Exception as e:
    print(e)
    flash(f"An error occurred. Artist {request.form['name']} could not be listed.")
  finally:
    db.session.close()
  return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  return render_template('pages/shows.html', shows=Show.query.all())

@app.route('/shows/create')
def create_shows():
  return render_template('forms/new_show.html', form=ShowForm())

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  try:
    form_data = ShowForm(request.form).to_dict()
    db.session.add(Show(**form_data))
    db.session.commit()
    flash('Show was successfully listed!')
  except Exception as e:
    print(e)
    flash('An error occurred. Show could not be listed.')
  finally:
    db.session.close()
  return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
