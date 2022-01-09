import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.environ.get("SECRET_KEY")

# CSRF protection configuration
WTF_CSRF_ENABLED = os.environ.get("WTF_CSRF_ENABLED", False) == "true"

# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = os.environ.get("DEBUG", False) == "true"

# Connect to the database
SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI")

# Don't track modifications of objects and emit signals.
SQLALCHEMY_TRACK_MODIFICATIONS = (
    os.environ.get("SQLALCHEMY_TRACK_MODIFICATIONS", False) == "true"
)
