from flask import Flask, render_template, request, flash, redirect, url_for
from forms import ArtistForm, VenueForm, ShowForm
from logging import Formatter, FileHandler
from model import db, Artist, Venue, Show
from flask_moment import Moment

import dateutil.parser
import logging
import babel

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db.init_app(app)

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
  artists = Artist.query.order_by(Artist.id.desc()).limit(10).all()
  venues = Venue.query.order_by(Venue.id.desc()).limit(10).all()

  return render_template('pages/home.html', artists=artists, venues=venues)

#----------------------------------------------------------------------------#
#  Venues
#----------------------------------------------------------------------------#

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
  search_term = request.form.get('search_term', '')
  results = Venue.query.filter(Venue.name.ilike(f'%{search_term}%')).all() 
  response = {
    "count": len(results),
    "data": [{'id': result.id, 'name': result.name} for result in results],
  }
  return render_template('pages/search_venues.html', 
    results=response, search_term=search_term)

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  return render_template('pages/show_venue.html', 
    venue=Venue.query.get_or_404(venue_id))

#----------------------------------------------------------------------------#
#  Create Venue
#----------------------------------------------------------------------------#

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  return render_template('forms/new_venue.html', form=VenueForm())

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  form = VenueForm(request.form)

  if not form.validate():
    for _, messages in form.errors.items():
      for message in messages:
        flash(message)
    return render_template('forms/new_venue.html', form=form)

  try:
    venue = Venue()
    form.populate_obj(venue)
    db.session.add(venue)
    db.session.commit()
    flash(f'Venue {form.name.data} was successfully listed!')
  except Exception as error:
    app.logger.error(error)
    flash(f'An error occurred. Venue {form.name.data} could not be listed.')
    db.session.rollback()
  finally:
    db.session.close()

  return render_template('pages/home.html')

#----------------------------------------------------------------------------#
#  Delete Venue
#----------------------------------------------------------------------------#

@app.route('/venues/<venue_id>', methods=['POST'])
def delete_venue(venue_id):
  venue = Venue.query.get_or_404(venue_id)

  try:
    db.session.delete(venue)
    db.session.commit()
    flash(f'Venue {venue.name} was successfully deleted!')
  except Exception as error:
    app.logger.error(error)
    flash(f'An error occurred. Venue {venue.name} could not be deleted.')
    db.session.rollback()
  finally:
    db.session.close()

  return redirect(url_for('index'))

#----------------------------------------------------------------------------#
#  Update Venue
#----------------------------------------------------------------------------#

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  venue = Venue.query.get(venue_id)
  form = VenueForm(obj=venue)

  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  form = VenueForm(request.form)
  venue = Venue.query.get_or_404(venue_id)

  if not form.validate():
    for _, messages in form.errors.items():
      for message in messages:
        flash(message)
    return render_template('forms/edit_venue.html', form=form, venue=venue)

  try:
    form.populate_obj(venue)
    db.session.commit()
    flash(f'Venue {form.name.data} was successfully updated!')
  except Exception as error:
    app.logger.error(error)
    flash(f'An error occurred. Venue {form.name.data} could not be updated.')
    db.session.rollback()
  finally:
    db.session.close()

  return redirect(url_for('show_venue', venue_id=venue_id))

#----------------------------------------------------------------------------#
#  Artists
#----------------------------------------------------------------------------#

@app.route('/artists')
def artists():
  return render_template('pages/artists.html', 
    artists=Artist.query.all())

@app.route('/artists/search', methods=['POST'])
def search_artists():
  search_term = request.form.get('search_term', '')
  results = Artist.query.filter(Artist.name.ilike(f'%{search_term}%')).all() 
  response = {
    "count": len(results),
    "data": [{'id': result.id, 'name': result.name} for result in results],
  }
  return render_template('pages/search_artists.html', results=response, 
    search_term=search_term)

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  return render_template('pages/show_artist.html', 
    artist=Artist.query.get_or_404(artist_id))

#----------------------------------------------------------------------------#
#  Create Artist
#----------------------------------------------------------------------------#

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  return render_template('forms/new_artist.html', form=ArtistForm())

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  form = ArtistForm(request.form)

  if not form.validate():
    for _, messages in form.errors.items():
      for message in messages:
        flash(message)
    return render_template('forms/new_artist.html', form=form)

  try:
    artist = Artist()
    form.populate_obj(artist)
    db.session.add(artist)
    db.session.commit()
    flash(f'Artist {form.name.data} was successfully listed!')
  except Exception as error:
    app.logger.error(error)
    flash(f'An error occurred. Artist {form.name.data} could not be listed.')
    db.session.rollback()
  finally:
    db.session.close()
  return render_template('pages/home.html')

#----------------------------------------------------------------------------#
#  Delete Artist
#  --------------------------------------------------------------------------#

@app.route('/artists/<artist_id>', methods=['POST'])
def delete_artist(artist_id):
  artist = Artist.query.get_or_404(artist_id)

  try:
    db.session.delete(artist)
    db.session.commit()
    flash(f'Artist {artist.name} was successfully deleted!')
  except Exception as error:
    app.logger.error(error)
    flash(f'An error occurred. Artist {artist.name} could not be deleted.')
    db.session.rollback()
  finally:
    db.session.close()

  return redirect(url_for('index'))

#----------------------------------------------------------------------------#
#  Update Artist
#  --------------------------------------------------------------------------#

@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  artist = Artist.query.get_or_404(artist_id)
  form = ArtistForm(obj=artist)

  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  form = ArtistForm(request.form)
  artist = Artist.query.get_or_404(artist_id)

  if not form.validate():
    for _, messages in form.errors.items():
      for message in messages:
        flash(message)
    return render_template('forms/edit_artist.html', form=form, artist=artist)

  try:
    form.populate_obj(artist)
    db.session.commit()
    flash(f'Artist {form.name.data} was successfully updated!')
  except Exception as error:
    app.logger.error(error)
    flash(f'An error occurred. Artist {form.name.data} could not be updated.')
    db.session.rollback()
  finally:
    db.session.close()

  return redirect(url_for('show_artist', artist_id=artist_id))

#----------------------------------------------------------------------------#
#  Shows
#----------------------------------------------------------------------------#

@app.route('/shows')
def shows():
  return render_template('pages/shows.html', shows=Show.query.all())


#----------------------------------------------------------------------------#
#  Create Shows
#----------------------------------------------------------------------------#

@app.route('/shows/create')
def create_shows():
  return render_template('forms/new_show.html', form=ShowForm())

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  form = ShowForm(request.form)

  if not form.validate():
    for _, messages in form.errors.items():
      for message in messages:
        flash(message)
    return render_template('forms/new_show.html', form=form)

  try:
    show = Show()
    form.populate_obj(show)
    db.session.add(show)
    db.session.commit()
    flash('Show was successfully listed!')
  except Exception as error:
    app.logger.error(error)
    flash('An error occurred. Show could not be listed.')
    db.session.rollback()
  finally:
    db.session.close()

  return render_template('pages/home.html')

#----------------------------------------------------------------------------#
#  Error pages
#----------------------------------------------------------------------------#

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter(
          '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
          )
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#


if __name__ == '__main__':
    app.run()