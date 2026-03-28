from datetime import timedelta
from django.utils import timezone
from .models import DoseLog
from django.core.mail import send_mail
from twilio.rest import Client
from django.conf import settings


def get_doses_to_remind():
    now = timezone.now()
    soon = now + timedelta(minutes=15)

    return DoseLog.objects.filter(
        status="pending",
        scheduled_datetime__gte=now,
        scheduled_datetime__lte=soon,
        reminder_sent=False,
    )


def get_overdue_to_alert():
    now = timezone.now()

    return DoseLog.objects.filter(
        status="pending",
        scheduled_datetime__lt=now,
        overdue_alert_sent=False,
    )


def send_test_sms(to_number, body):
    to_number = str(to_number).strip()
    to_number = to_number.replace("+", "")
    to_number = "+1" + to_number[-10:]

    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

    message = client.messages.create(
        body=body,
        from_=settings.TWILIO_PHONE_NUMBER,
        to=to_number,
    )

    print(f"Sending from: {settings.TWILIO_PHONE_NUMBER}")
    print(f"Sending to: {to_number}")
    print(f"SMS sent with SID: {message.sid}")


def process_dose_alerts():
    reminder_doses = get_doses_to_remind()
    overdue_doses = get_overdue_to_alert()

    # REMINDERS
    for dose in reminder_doses:
        subject = "Medication Reminder"
        message = (
            f"Medication Reminder\n"
            f"{dose.medication.name} is due at "
            f"{dose.scheduled_datetime.strftime('%I:%M %p')}."
        )

        # EMAIL
        if dose.user.email:
            send_mail(
                subject="Medication Reminder",
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[dose.user.email],
                fail_silently=False,
            )
            print(f"REMINDER sent for dose ID {dose.id}")

            # SMS
            # Actívalo cuando tu campaña de Twilio esté approved
            if hasattr(dose.user, "profile") and dose.user.profile.phone_number:
                print(
                    f"SMS READY → {dose.user.profile.phone_number}: {message}")

        dose.reminder_sent = True
        dose.save()

    # OVERDUE ALERTS
    for dose in overdue_doses:
        subject = "Medication Overdue Alert"
        message = (
            f"Missed Dose Alerts\n"
            f"{dose.medication.name} was scheduled at "
            f"{dose.scheduled_datetime.strftime('%I:%M %p')} and has not been taken."
        )

        # EMAIL
        if dose.user.email:
            send_mail(
                subject="Medication Overdue Alert",
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[dose.user.email],
                fail_silently=False,
            )
            print(f"OVERDUE EMAIL SENT for dose ID{dose.id}")

            # SMS
            # Actívalo cuando Twilio quede aprobado
            if hasattr(dose.user, "profile") and dose.user.profile.phone_number:
                print(
                    f"SMS READY → {dose.user.profile.phone_number}: {message}")

        dose.overdue_alert_sent = True
        dose.save()


def get_next_dose(user):
    now = timezone.now()
    return (
        DoseLog.objects
        .filter(user=user, status='pending', scheduled_datetime__gte=now)
        .order_by('scheduled_datetime')
        .first()
    )


def get_overdue_doses(user):
    now = timezone.now()
    return (
        DoseLog.objects
        .filter(user=user, status='pending', scheduled_datetime__lt=now)
        .order_by('scheduled_datetime')
    )


def get_doses_to_remind():
    now = timezone.now()
    soon = now + timedelta(minutes=15)

    return DoseLog.objects.filter(
        status='pending',
        scheduled_datetime__gte=now,
        scheduled_datetime__lte=soon,
        reminder_sent=False
    )


def get_overdue_to_alert():
    now = timezone.now()

    return DoseLog.objects.filter(
        status='pending',
        scheduled_datetime__lt=now,
        overdue_alert_sent=False
    )


def process_dose_alerts():
    reminder_doses = get_doses_to_remind()
    overdue_doses = get_overdue_to_alert()

    for dose in reminder_doses:
        if not dose.user.email:
            continue

        message = (
            f" Medication Reminder\n"
            f"{dose.medication.name} is due at "
            f"{dose.scheduled_datetime.strftime('%I:%M %p')}"
        )

        send_mail(
            subject="Medication Reminder",
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[dose.user.email],
            fail_silently=False,
        )

        print(f"REMINDER sent for dose ID {dose.I}")
        dose.reminder_sent = True
        dose.save()

    for dose in overdue_doses:
        if not dose.user.email:
            continue

        message = (f"Missed Dose Alert!\n"
                   f"{dose.medication.name} was schedule at"
                   f"{dose.scheduled_datetime.strftime('%I:%M %p')} and has not been taken."
                   )

        send_mail(
            subject="Medication Overdue Alert",
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[dose.user.email],
            fail_silently=False,
        )

        print(f"OVERDUE alert sent for dose ID {dose.id}")
        dose.overdue_alert_sent = True
        dose.save()


def send_test_sms(to_number, body):
    to_number = str(to_number).strip()

    to_number = to_number.replace("+", "")

    to_number = "+1" + to_number[-10:]

    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

    message = client.messages.create(
        body=body,
        from_=settings.TWILIO_PHONE_NUMBER,
        to=to_number
    )

    print(f"SMS sent with SID: {message.sid}")
