import os
from dotenv import load_dotenv

load_dotenv()

STORAGE_ACCOUNT = os.getenv("STORAGE_ACCOUNT")

CONTAINER = os.getenv("CONTAINER")