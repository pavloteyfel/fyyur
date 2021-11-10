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
    venue=Venue.query.get(venue_id))

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  form = VenueForm(request.form)
  if form.validate():
    try:
      # new_venue.html: website_link renamed website to be consistent
      venue = Venue()
      form.populate_obj(venue)
      db.session.add(venue)
      db.session.commit()
      flash(f'Venue {form.name.data} was successfully listed!')
    except Exception as error:
      flash(f'An error occurred. Venue {form.name.data} could not be listed.')
      print(error)
      db.session.rollback()
    finally:
      db.session.close()
  else:
      message = []
      for field, err in form.errors.items():
          message.append(field + ' ' + '|'.join(err))
      flash('Errors ' + str(message))
  return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  print(venue_id)
  try:
    venue = Venue.query.get(venue_id)
    db.session.delete(venue)
    db.session.commit()
    flash(f"Venue {request.form['name']} was successfully deleted!")
  except Exception as e:
    print(e)
    flash(f"An error occurred. Venue {request.form['name']} could not be deleted.")
    db.session.rollback()
  finally:
    db.session.close()
  return redirect(url_for('index'))

#  Artists
#  ----------------------------------------------------------------
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
    artist=Artist.query.get(artist_id))

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  artist = Artist.query.get(artist_id)
  form = ArtistForm(obj=artist)
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  try:
    artist = Artist.query.get(artist_id)
    ArtistForm(request.form).populate_obj(artist)
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
  form = VenueForm(obj=venue)
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  try:
    venue = Venue.query.get(venue_id)
    VenueForm(request.form).populate_obj(venue)
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
    artist = Artist()
    ArtistForm(request.form).populate_obj(artist)
    db.session.add(artist)
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
    show = Show()
    ShowForm(request.form).populate_obj(show)
    db.session.add(show)
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
