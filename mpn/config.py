import os
from dotenv import load_dotenv
load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")

MONGO_DBNAME = os.getenv("MONGO_DBNAME")
MONGO_USER = os.getenv("MONGO_USER")
MONGO_PASS = os.getenv("MONGO_PASS")
MONGO_URI = os.getenv("MONGO_URI")

#GOOGLE_GEOCODING_API_KEY = os.getenv("GOOGLE_GEOCODING_API_KEY")