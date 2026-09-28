import os

from dotenv import load_dotenv
load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')
secret = os.getenv('JWT_SECRET')

