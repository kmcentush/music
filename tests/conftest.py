import os

os.environ["TEST"] = "true"

from music.models import create_db

# Create database
create_db()
