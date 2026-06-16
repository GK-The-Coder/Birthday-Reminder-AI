from apscheduler.schedulers.background import (
    BackgroundScheduler
)

from datetime import datetime

from database import (
    birthdays_collection,
    email_logs_collection
)

from ai_service import (
    generate_birthday_message
)

from email_service import (
    send_email
)


def send_daily_birthday_wishes():

    today = datetime.now()

    current_date = today.strftime(
        "%m-%d"
    )

    birthdays = (
        birthdays_collection.find()
    )

    for person in birthdays:

        birthday = (
            person["birthday"]
        )

        birthday_date = (
            datetime.strptime(
                birthday,
                "%Y-%m-%d"
            )
        )

        person_date = (
            birthday_date.strftime(
                "%m-%d"
            )
        )

        if person_date == current_date:

            wish = (
                generate_birthday_message(
                    person["name"]
                )
            )

            send_email(
                person["email"],
                "Happy Birthday 🎂",
                wish
            )

            email_logs_collection.insert_one({

                "name":
                person["name"],

                "email":
                person["email"],

                "status":
                "sent",

                "timestamp":
                datetime.now()

            })

            print(
                f"Email sent to "
                f"{person['name']}"
            )


scheduler = (
    BackgroundScheduler()
)

scheduler.add_job(

    send_daily_birthday_wishes,

    "cron",

    hour=8,

    minute=0

)

scheduler.start()