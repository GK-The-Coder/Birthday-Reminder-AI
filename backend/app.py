from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from datetime import datetime
import os

from dependencies import get_current_user
from database import birthdays_table, email_logs_table, users_table
from models.user_model import UserRegister, UserLogin
from models.birthday_model import Birthday, WishRequest, EmailRequest
from database import supabase
from ai_service import generate_birthday_message
from email_service import send_email
import logging

logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(_app):
    from scheduler import start_scheduler, stop_scheduler

    start_scheduler()
    yield
    stop_scheduler()


app = FastAPI(lifespan=lifespan)


@app.exception_handler(Exception)
async def handle_unexpected_error(_request: Request, exc: Exception):
    logger.exception("Unhandled API error", exc_info=exc)
    return JSONResponse(
        status_code=500,
        content={"detail": "An unexpected server error occurred."},
    )

default_origins = ",".join([
    "http://localhost:5173",
    "https://wish-mate.vercel.app",
])
origins = [origin.strip() for origin in os.getenv(
    "CORS_ORIGINS", default_origins
).split(",") if origin.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "WishMate API Running"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/ready")
def readiness():
    try:
        supabase.table("users").select("id").limit(1).execute()
        return {"status": "ready", "database": "ok"}
    except Exception:
        logger.exception("Readiness check failed")
        raise HTTPException(status_code=503, detail="Database is not ready")


@app.get("/birthdays")
def get_birthdays(user=Depends(get_current_user)):
    response = birthdays_table.select("id, name, email, birthday").eq(
        "user_id", user["userId"]
    ).execute()
    return [{"_id": birthday["id"], "name": birthday["name"],
             "email": birthday["email"], "birthday": birthday["birthday"]}
            for birthday in response.data]


@app.get("/birthdays/{id}")
def get_birthday(id: str, user=Depends(get_current_user)):
    response = birthdays_table.select("id, name, email, birthday").eq(
        "id", id
    ).eq("user_id", user["userId"]).maybe_single().execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="Birthday not found")
    birthday = response.data
    return {"_id": birthday["id"], "name": birthday["name"],
            "email": birthday["email"], "birthday": birthday["birthday"]}


@app.post("/birthdays")
def create_birthday(data: Birthday, user=Depends(get_current_user)):
    birthdays_table.insert({**data.model_dump(mode="json"), "user_id": user["userId"]}).execute()
    return {"message": "Birthday Added"}


@app.put("/birthdays/{id}")
def update_birthday(id: str, data: Birthday, user=Depends(get_current_user)):
    response = birthdays_table.update(data.model_dump(mode="json")).eq(
        "id", id
    ).eq("user_id", user["userId"]).execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="Birthday not found")
    return {"message": "Updated Successfully"}


@app.delete("/birthdays/{id}")
def delete_birthday(id: str, user=Depends(get_current_user)):
    response = birthdays_table.delete().eq("id", id).eq(
        "user_id", user["userId"]
    ).execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="Birthday not found")
    return {"message": "Deleted Successfully"}


@app.post("/generate-wish")
def generate_wish(data: WishRequest):
    try:
        return {"wish": generate_birthday_message(data.name)}
    except Exception:
        logger.exception("Wish generation failed")
        raise HTTPException(status_code=502, detail="Unable to generate a wish right now")


@app.post("/send-birthday-email")
def send_birthday_email(data: EmailRequest, user=Depends(get_current_user)):
    try:
        wish = generate_birthday_message(data.name, user.get("name"))

        send_email(
            data.email,
            "Happy Birthday 🎂",
            wish
        )

        email_logs_table.insert({
            "user_id": user["userId"],
            "name": data.name,
            "email": data.email,
            "status": "sent",
            "timestamp": datetime.now().isoformat(),
        }).execute()

        return {"message": "Email Sent Successfully"}

    except Exception:
        logger.exception("Birthday email failed")
        raise HTTPException(status_code=502, detail="Unable to send the birthday email right now")

@app.get("/stats")
def get_stats(user=Depends(get_current_user)):
    birthdays = birthdays_table.select("birthday").eq(
        "user_id", user["userId"]
    ).execute().data
    emails = email_logs_table.select("id").eq(
        "user_id", user["userId"]
    ).execute().data
    total_birthdays = len(birthdays)
    total_emails = len(emails)
    today = datetime.now()
    today_birthdays = 0
    this_month = 0

    for person in birthdays:
        birth = datetime.strptime(person["birthday"], "%Y-%m-%d")
        if birth.month == today.month:
            this_month += 1
        if birth.month == today.month and birth.day == today.day:
            today_birthdays += 1

    return {
        "totalBirthdays": total_birthdays,
        "todayBirthdays": today_birthdays,
        "thisMonth": this_month,
        "emailsSent": total_emails,
    }


@app.get("/email-logs")
def get_logs(user=Depends(get_current_user)):
    response = email_logs_table.select(
        "id, name, email, status, timestamp, message"
    ).eq("user_id", user["userId"]).order("timestamp", desc=True).execute()
    return [{"_id": log["id"], **{key: log.get(key) for key in
            ("name", "email", "status", "timestamp", "message")}}
            for log in response.data]


@app.post("/register")
def register(user: UserRegister):
    try:
        response = supabase.auth.sign_up({
            "email": user.email,
            "password": user.password,
            "options": {"data": {"name": user.name}},
        })
        if not response.user:
            raise HTTPException(status_code=400, detail="Registration failed")
        users_table.insert({
            "id": str(response.user.id),
            "name": user.name,
            "email": user.email,
        }).execute()
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=400, detail="Email already exists or registration failed")
    return {"message": "User Registered"}


@app.post("/login")
def login(user: UserLogin):
    try:
        response = supabase.auth.sign_in_with_password({
            "email": user.email,
            "password": user.password,
        })
        if not response.session:
            raise HTTPException(status_code=401, detail="Email confirmation required")
        return {"access_token": response.session.access_token}
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid Credentials")
