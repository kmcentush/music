import os

os.environ["TEST"] = "true"  # mark test before any imports


import music.models  # noqa: F401  # import models before creating database
from music.data import create_db

# Create database
create_db()
