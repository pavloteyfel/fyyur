from forms import ArtistForm, VenueForm, ShowForm
from logging import Formatter, FileHandler
from model import db, Artist, Venue, Show
from sqlalchemy.exc import SQLAlchemyError
from flask_wtf.csrf import CSRFProtect, CSRFError
from flask_migrate import Migrate
from flask_moment import Moment
from flask import Flask, render_template, request, flash, redirect, url_for

import dateutil.parser
import logging
import babel

# ----------------------------------------------------------------------------#
# App Config.
# ----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object("config")
csrf = CSRFProtect(app)
db.init_app(app)
migrate = Migrate(app, db)


# ----------------------------------------------------------------------------#
# Filters.
# ----------------------------------------------------------------------------#


def format_datetime(value, format_="medium"):
    date = dateutil.parser.parse(value)
    if format_ == "full":
        format_ = "EEEE MMMM, d, y 'at' h:mma"
    elif format_ == "medium":
        format_ = "EE MM, dd, y h:mma"
    return babel.dates.format_datetime(date, format_, locale="en")


app.jinja_env.filters["datetime"] = format_datetime


# ----------------------------------------------------------------------------#
# Controllers.
# ----------------------------------------------------------------------------#


@app.route("/")
def index():
    """
    App's main entry point

    Returns:
        on GET: Lists recently listed Artists and Venues
    """

    artists = Artist.query.order_by(Artist.id.desc()).limit(10).all()
    venues = Venue.query.order_by(Venue.id.desc()).limit(10).all()

    return render_template("pages/home.html", artists=artists, venues=venues)


# ----------------------------------------------------------------------------#
#  Venues
# ----------------------------------------------------------------------------#


@app.route("/venues")
def venues():
    """
    Shows available venues grouped by place.
    """

    venues = Venue.query.all()
    places = Venue.query.distinct(Venue.city, Venue.state).all()
    areas = []
    for place in places:
        areas.append(
            {
                "city": place.city,
                "state": place.state,
                "venues": [
                    {
                        "id": venue.id,
                        "name": venue.name,
                        "upcoming_shows_count": venue.upcoming_shows_count,
                    }
                    for venue in venues
                    if venue.city == place.city and venue.state == place.state
                ],
            }
        )
    return render_template("pages/venues.html", areas=areas)


@app.route("/venues/search", methods=["POST"])
def search_venues():
    """
    Search function called from venues page.

    Returns:
        on POST: Searches for venues and lists found entries.
    """

    search_term = request.form.get("search_term", "")
    results = Venue.query.filter(Venue.name.ilike(f"%{search_term}%")).all()
    response = {
        "count": len(results),
        "data": [
            {
                "id": result.id,
                "name": result.name,
                "upcoming_shows_count": result.upcoming_shows_count,
            }
            for result in results
        ],
    }
    return render_template(
        "pages/search_venues.html", results=response, search_term=search_term
    )


@app.route("/venues/<int:venue_id>")
def show_venue(venue_id):
    """
    Loads venue's page.

    Args:
        venue_id: Venue identifier.

    Returns:
        on GET: Shows venue's detailed page based on the id.
    """
    return render_template(
        "pages/show_venue.html", venue=Venue.query.get_or_404(venue_id)
    )


# ----------------------------------------------------------------------------#
#  Create Venue
# ----------------------------------------------------------------------------#


@app.route("/venues/create", methods=["GET"])
def create_venue_form():
    """
    Loads form page for creating a new venue.
    """
    return render_template("forms/new_venue.html", form=VenueForm())


@app.route("/venues/create", methods=["POST"])
def create_venue_submission():
    """
    Handles the form for submission. Applies form validation.
    """
    form = VenueForm(request.form)

    if not form.validate():
        for _, messages in form.errors.items():
            for message in messages:
                flash(message)
        return render_template("forms/new_venue.html", form=form)

    try:
        venue = Venue()
        form.populate_obj(venue)
        db.session.add(venue)
        db.session.commit()
        flash(f"Venue {form.name.data} was successfully listed!")
    except SQLAlchemyError as error:
        app.logger.error(error)
        flash(f"An error occurred. Venue {form.name.data} could not be listed.")
        db.session.rollback()
    finally:
        db.session.close()

    return redirect(url_for("index"))


# ----------------------------------------------------------------------------#
#  Delete Venue
# ----------------------------------------------------------------------------#


@app.route("/venues/<venue_id>", methods=["POST"])
def delete_venue(venue_id):
    """
    Completely deletes venue from database.

    Args:
        venue_id: Venue identifier.

    Returns:
        on POST: Deletes venue row from database.
    """
    venue = Venue.query.get_or_404(venue_id)

    try:
        db.session.delete(venue)
        db.session.commit()
        flash(f"Venue {venue.name} was successfully deleted!")
    except SQLAlchemyError as error:
        app.logger.error(error)
        flash(f"An error occurred. Venue {venue.name} could not be deleted.")
        db.session.rollback()
    finally:
        db.session.close()

    return redirect(url_for("index"))


# ----------------------------------------------------------------------------#
#  Update Venue
# ----------------------------------------------------------------------------#


@app.route("/venues/<int:venue_id>/edit", methods=["GET"])
def edit_venue(venue_id):
    """
    Loads venue form page for modification.
    """
    venue = Venue.query.get(venue_id)
    form = VenueForm(obj=venue)

    return render_template("forms/edit_venue.html", form=form, venue=venue)


@app.route("/venues/<int:venue_id>/edit", methods=["POST"])
def edit_venue_submission(venue_id):
    """
    Handles the form for modification. Applies form validation.
    """
    form = VenueForm(request.form)
    venue = Venue.query.get_or_404(venue_id)

    if not form.validate():
        for _, messages in form.errors.items():
            for message in messages:
                flash(message)
        return render_template("forms/edit_venue.html", form=form, venue=venue)

    try:
        form.populate_obj(venue)
        db.session.commit()
        flash(f"Venue {form.name.data} was successfully updated!")
    except Exception as error:
        app.logger.error(error)
        flash(f"An error occurred. Venue {form.name.data} could not be updated.")
        db.session.rollback()
    finally:
        db.session.close()

    return redirect(url_for("show_venue", venue_id=venue_id))


# ----------------------------------------------------------------------------#
#  Artists
# ----------------------------------------------------------------------------#


@app.route("/artists")
def artists():
    """
    Shows available artists.

    Returns:
        on GET: Lists all artists from the database
    """
    return render_template("pages/artists.html", artists=Artist.query.all())


@app.route("/artists/search", methods=["POST"])
def search_artists():
    """
    Search function called from artist page.

    Returns:
        on POST: Searches for artist and lists found entries.
    """
    search_term = request.form.get("search_term", "")
    results = Artist.query.filter(Artist.name.ilike(f"%{search_term}%")).all()
    response = {
        "count": len(results),
        "data": [
            {
                "id": result.id,
                "name": result.name,
                "upcoming_shows_count": result.upcoming_shows_count,
            }
            for result in results
        ],
    }
    return render_template(
        "pages/search_artists.html", results=response, search_term=search_term
    )


@app.route("/artists/<int:artist_id>")
def show_artist(artist_id):
    """
    Loads artist's page.

    Args:
        artist_id: Venue identifier.

    Returns:
        on GET: Shows artist's detailed page based on the id.
    """
    return render_template(
        "pages/show_artist.html", artist=Artist.query.get_or_404(artist_id)
    )


# ----------------------------------------------------------------------------#
#  Create Artist
# ----------------------------------------------------------------------------#


@app.route("/artists/create", methods=["GET"])
def create_artist_form():
    """
    Loads form page for creating a new artist.
    """
    return render_template("forms/new_artist.html", form=ArtistForm())


@app.route("/artists/create", methods=["POST"])
def create_artist_submission():
    """
    Handles the form for submission. Applies form validation.
    """
    form = ArtistForm(request.form)

    if not form.validate():
        for _, messages in form.errors.items():
            for message in messages:
                flash(message)
        return render_template("forms/new_artist.html", form=form)

    try:
        artist = Artist()
        form.populate_obj(artist)
        db.session.add(artist)
        db.session.commit()
        flash(f"Artist {form.name.data} was successfully listed!")
    except Exception as error:
        app.logger.error(error)
        flash(f"An error occurred. Artist {form.name.data} could not be listed.")
        db.session.rollback()
    finally:
        db.session.close()
    return redirect(url_for("index"))


# ----------------------------------------------------------------------------#
#  Delete Artist
#  --------------------------------------------------------------------------#


@app.route("/artists/<artist_id>", methods=["POST"])
def delete_artist(artist_id):
    """
    Completely deletes artist from database.

    Args:
        artist_id: Artist identifier.

    Returns:
        on POST: Deletes artist row from database.
    """
    artist = Artist.query.get_or_404(artist_id)

    try:
        db.session.delete(artist)
        db.session.commit()
        flash(f"Artist {artist.name} was successfully deleted!")
    except Exception as error:
        app.logger.error(error)
        flash(f"An error occurred. Artist {artist.name} could not be deleted.")
        db.session.rollback()
    finally:
        db.session.close()

    return redirect(url_for("index"))


# ----------------------------------------------------------------------------#
#  Update Artist
#  --------------------------------------------------------------------------#


@app.route("/artists/<int:artist_id>/edit", methods=["GET"])
def edit_artist(artist_id):
    """
    Handles the form for submission. Applies form validation.

    Args:
        artist_id: Artist identifier.
    """
    artist = Artist.query.get_or_404(artist_id)
    form = ArtistForm(obj=artist)

    return render_template("forms/edit_artist.html", form=form, artist=artist)


@app.route("/artists/<int:artist_id>/edit", methods=["POST"])
def edit_artist_submission(artist_id):
    """
    Handles the form for submission. Applies form validation.

    Args:
        artist_id: Artist identifier.
    """
    form = ArtistForm(request.form)
    artist = Artist.query.get_or_404(artist_id)

    if not form.validate():
        for _, messages in form.errors.items():
            for message in messages:
                flash(message)
        return render_template("forms/edit_artist.html", form=form, artist=artist)

    try:
        form.populate_obj(artist)
        db.session.commit()
        flash(f"Artist {form.name.data} was successfully updated!")
    except Exception as error:
        app.logger.error(error)
        flash(f"An error occurred. Artist {form.name.data} could not be updated.")
        db.session.rollback()
    finally:
        db.session.close()

    return redirect(url_for("show_artist", artist_id=artist_id))


# ----------------------------------------------------------------------------#
#  Shows
# ----------------------------------------------------------------------------#


@app.route("/shows")
def shows():
    """
    Shows available shows.
    """
    return render_template("pages/shows.html", shows=Show.query.all())


# ----------------------------------------------------------------------------#
#  Create Shows
# ----------------------------------------------------------------------------#


@app.route("/shows/create")
def create_shows():
    """
    Prepares the form for submission. Applies form validation. Uses drop-down
    list to get the artist_id and venue_id.
    """
    form = ShowForm()
    artists = Artist.query.order_by(Artist.id).all()
    venues = Venue.query.order_by(Venue.id).all()
    form.artist_id.choices = [(a.id, a.name) for a in artists]
    form.venue_id.choices = [(v.id, v.name) for v in venues]
    return render_template("forms/new_show.html", form=form)


@app.route("/shows/create", methods=["POST"])
def create_show_submission():
    """
    Handles the form for submission. Applies form validation.
    """
    form = ShowForm(request.form)

    if not form.validate():
        for _, messages in form.errors.items():
            for message in messages:
                flash(message)
        return redirect(url_for("create_shows"))

    try:
        show = Show()
        form.populate_obj(show)
        db.session.add(show)
        db.session.commit()
        flash("Show was successfully listed!")
    except Exception as error:
        app.logger.error(error)
        flash("An error occurred. Show could not be listed.")
        db.session.rollback()
    finally:
        db.session.close()

    return redirect(url_for("index"))


# ----------------------------------------------------------------------------#
#  Error pages
# ----------------------------------------------------------------------------#


@app.errorhandler(404)
def not_found_error(error):
    """
    Client related response error page.
    """
    app.logger.error(error)
    return render_template("errors/404.html"), 404


@app.errorhandler(500)
def server_error(error):
    """
    Server related response error page.
    """
    app.logger.error(error)
    return render_template("errors/500.html"), 500


@app.errorhandler(CSRFError)
def server_error(error):
    """
    Shows error if CSRF token is missing.
    """
    app.logger.error(error)
    return render_template("errors/csrf.html"), 400


if not app.debug:
    file_handler = FileHandler("error.log")
    file_handler.setFormatter(
        Formatter("%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]")
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
