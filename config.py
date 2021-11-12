import os


SECRET_KEY = os.urandom(32)

# CSRF protection configuration
WTF_CSRF_ENABLED = True

# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# Connect to the database
SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:postgres@localhost:5432/fyyur'

# Don't track modifications of objects and emit signals.
SQLALCHEMY_TRACK_MODIFICATIONS = False
