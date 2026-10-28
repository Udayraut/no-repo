import os
from dotenv import load_dotenv

load_dotenv()

environment = os.environ.get('DJANGO_SETTINGS_MODULE', 'skyniya.settings.development')
