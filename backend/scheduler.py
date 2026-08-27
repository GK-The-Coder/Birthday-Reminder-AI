import logging
import os
from datetime import date, datetime
from zoneinfo import ZoneInfo

from apscheduler.schedulers.background import BackgroundScheduler

from ai_service import generate_birthday_message
from database import birthdays_table, email_logs_table
from email_service import send_email

logger = logging.getLogger(__name__)
SCHEDULER_TIMEZONE = os.getenv("SCHEDULER_TIMEZONE", "UTC")
scheduler = BackgroundScheduler(timezone=ZoneInfo(SCHEDULER_TIMEZONE))


def send_daily_birthday_wishes():
    today = datetime.now(ZoneInfo(SCHEDULER_TIMEZONE))
    delivery_date = today.date()
    birthdays = birthdays_table.select(
        "id, name, email, birthday, user_id"
    ).execute().data

    for person in birthdays:
        birthday_date = date.fromisoformat(person["birthday"])
        if (birthday_date.month, birthday_date.day) != (today.month, today.day):
            continue

        already_sent = email_logs_table.select("id").eq(
            "birthday_id", person["id"]
        ).eq("delivery_date", delivery_date.isoformat()).limit(1).execute().data
        if already_sent:
            logger.info("Birthday email already sent for %s", person["email"])
            continue

        try:
            wish = generate_birthday_message(person["name"])
            send_email(person["email"], "Happy Birthday 🎂", wish)
            email_logs_table.insert({
                "user_id": person["user_id"],
                "birthday_id": person["id"],
                "delivery_date": delivery_date.isoformat(),
                "name": person["name"],
                "email": person["email"],
                "status": "sent",
                "message": wish,
                "timestamp": datetime.now(ZoneInfo(SCHEDULER_TIMEZONE)).isoformat(),
            }).execute()
            logger.info("Birthday email sent to %s", person["email"])
        except Exception:
            logger.exception("Birthday email failed for %s", person["email"])


def start_scheduler():
    if scheduler.running:
        return
    scheduler.add_job(
        send_daily_birthday_wishes,
        "cron",
        hour=8,
        minute=0,
        id="daily-birthday-wishes",
        replace_existing=True,
        coalesce=True,
        max_instances=1,
        misfire_grace_time=3600,
    )
    scheduler.start()
    logger.info("Birthday scheduler started with timezone %s", SCHEDULER_TIMEZONE)


def stop_scheduler():
    if scheduler.running:
        scheduler.shutdown(wait=True)
        logger.info("Birthday scheduler stopped")
