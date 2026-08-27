import os

from dotenv import load_dotenv
from supabase import Client, create_client

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise RuntimeError("SUPABASE_URL and SUPABASE_KEY must be configured")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

birthdays_table = supabase.table("birthdays")
email_logs_table = supabase.table("email_logs")
users_table = supabase.table("users")
