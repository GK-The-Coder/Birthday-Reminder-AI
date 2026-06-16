from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

client = MongoClient(
    os.getenv("MONGO_URI")
)

db = client["birthdayDB"]

birthdays_collection = db["birthdays"]

email_logs_collection = db["email_logs"]

users_collection = db["users"]