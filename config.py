from dotenv import load_dotenv
from os import environ

load_dotenv()

SA_KEY_PATH = environ["SA_KEY_PATH"]
BUCKET_NAME = environ["BUCKET_NAME"]
DATABASE_NAME = environ["DATABASE_NAME"]
JWT_KEY = environ["JWT_KEY"]
ELASTIC_HOST = environ["ELASTIC_HOST"]

GOOGLE_CLIENT_ID = environ["GOOGLE_CLIENT_ID"]
GOOGLE_CLIENT_SECRET = environ["GOOGLE_CLIENT_SECRET"]

environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

FRONT_END_GOOGLE_LOGIN_URL = environ.get("FRONT_END_GOOGLE_LOGIN_URL")
