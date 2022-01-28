from sqlalchemy.ext.hybrid import hybrid_property
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class Venue(db.Model):
    """Venue data model connected to artist model through Show model"""

    __tablename__ = "Venue"

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
    shows = db.relationship(
        "Show", back_populates="venue", cascade="all, delete", lazy="joined"
    )

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

    def __repr__(self):
        return f"<Venue {self.id}, {self.name}>"


class Artist(db.Model):
    """Artist data model connected to venue model through Show model"""

    __tablename__ = "Artist"

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
    shows = db.relationship(
        "Show", back_populates="artist", cascade="all, delete", lazy="joined"
    )

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

    def __repr__(self):
        return f"<Artist {self.id}, {self.name}>"


class Show(db.Model):
    """Connecting model for Artist and Venue models"""

    __tablename__ = "Show"

    id = db.Column(db.Integer, primary_key=True)
    artist_id = db.Column(db.Integer, db.ForeignKey(
        "Artist.id"), nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey("Venue.id"), nullable=False)
    _start_time = db.Column(db.DateTime, nullable=False)
    artist = db.relationship("Artist", back_populates="shows")
    venue = db.relationship("Venue", back_populates="shows")

    @property
    def start_time(self):
        return self._start_time.strftime("%Y-%m-%d %H:%M:%S")

    @start_time.setter
    def start_time(self, value):
        self._start_time = value

    def __repr__(self):
        return f"<Show {self.id}, Artist {self.artist_id}, \
            Venue {self.venue_id}>"
