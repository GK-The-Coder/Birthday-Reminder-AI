from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from bson import ObjectId
from datetime import datetime

from dependencies import get_current_user
from database import birthdays_collection, email_logs_collection, users_collection
from models.user_model import UserRegister, UserLogin
from models.birthday_model import Birthday, WishRequest, EmailRequest
from auth import hash_password, verify_password, create_token
from ai_service import generate_birthday_message
from email_service import send_email

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173",
                   "https://birthday-reminder-ai.vercel.app/"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {"message": "Birthday Reminder API Running"}


@app.get("/birthdays")
def get_birthdays(user=Depends(get_current_user)):
    birthdays = []
    for birthday in birthdays_collection.find({"userId": user["userId"]}):
        birthday["_id"] = str(birthday["_id"])
        birthdays.append(birthday)
    return birthdays


@app.get("/birthdays/{id}")
def get_birthday(id: str, user=Depends(get_current_user)):
    try:
        birthday = birthdays_collection.find_one({"_id": ObjectId(id), "userId": user["userId"]})
        if not birthday:
            raise HTTPException(status_code=404, detail="Birthday not found")
        birthday["_id"] = str(birthday["_id"])
        return birthday
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid ID")


@app.post("/birthdays")
def create_birthday(data: Birthday, user=Depends(get_current_user)):
    birthday = data.model_dump()
    birthday["userId"] = user["userId"]
    birthdays_collection.insert_one(birthday)
    return {"message": "Birthday Added"}


@app.put("/birthdays/{id}")
def update_birthday(id: str, data: Birthday, user=Depends(get_current_user)):
    try:
        result = birthdays_collection.update_one(
            {"_id": ObjectId(id), "userId": user["userId"]},
            {"$set": data.model_dump()},
        )
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Birthday not found")
        return {"message": "Updated Successfully"}
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid ID")


@app.delete("/birthdays/{id}")
def delete_birthday(id: str, user=Depends(get_current_user)):
    try:
        result = birthdays_collection.delete_one({"_id": ObjectId(id), "userId": user["userId"]})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Birthday not found")
        return {"message": "Deleted Successfully"}
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid ID")


@app.post("/generate-wish")
def generate_wish(data: WishRequest):
    wish = generate_birthday_message(data.name)
    return {"wish": wish}


@app.post("/send-birthday-email")
def send_birthday_email(data: EmailRequest, user=Depends(get_current_user)):
    wish = generate_birthday_message(data.name)
    send_email(data.email, "Happy Birthday 🎂", wish)
    email_logs_collection.insert_one({
        "userId": user["userId"],
        "name": data.name,
        "email": data.email,
        "status": "sent",
        "timestamp": datetime.now(),
    })
    return {"message": "Email Sent Successfully"}


@app.get("/stats")
def get_stats(user=Depends(get_current_user)):
    birthdays = list(birthdays_collection.find({"userId": user["userId"]}))
    emails = list(email_logs_collection.find())
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
    logs = []
    for log in email_logs_collection.find({"userId": user["userId"]}).sort("timestamp", -1):
        log["_id"] = str(log["_id"])
        logs.append(log)
    return logs


@app.post("/register")
def register(user: UserRegister):
    existing = users_collection.find_one({"email": user.email})
    if existing:
        raise HTTPException(status_code=400, detail="Email already exists")
    users_collection.insert_one(
        {
            "name": user.name,
            "email": user.email,
            "password": hash_password(user.password),
        }
    )
    return {"message": "User Registered"}


@app.post("/login")
def login(user: UserLogin):
    db_user = users_collection.find_one({"email": user.email})
    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid Credentials")
    if not verify_password(user.password, db_user["password"]):
        raise HTTPException(status_code=401, detail="Invalid Credentials")
    token = create_token({"userId": str(db_user["_id"]), "email": db_user["email"]})
    return {"access_token": token}
