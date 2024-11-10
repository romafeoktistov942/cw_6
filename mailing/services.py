import datetime
import smtplib

import pytz
from apscheduler.schedulers.background import BackgroundScheduler
from django.core.mail import send_mail

from config.settings import EMAIL_HOST_USER
from mailing.models import Attempt, Mailing


def get_mailings():
    """Функция для получения стека рассылок"""

    mailing_client_dict: dict = {}
    date_time = datetime.datetime.now(pytz.utc)
    print("Получаем текущую даты и время:", date_time)

    mailing_list = Mailing.objects.all()

    for mailing in mailing_list:
        attempt_date_mailing = (
            Attempt.objects.filter(mailing_id_id=mailing.id)
            .exclude(status="False")
            .order_by("date_last_attempt")
            .last()
        )

        if mailing.status == "W" and mailing.is_published:
            if attempt_date_mailing is None:
                if mailing.date_of_first_dispatch <= date_time:
                    mailing_client_dict[mailing] = mailing.client_list.all()
            else:
                if mailing.periodicity == "D":
                    periodicity_date = (
                        attempt_date_mailing.date_last_attempt
                        + datetime.timedelta(days=1)
                    )
                    if periodicity_date <= date_time:
                        mailing_client_dict[mailing] = mailing.client_list.all()
                elif mailing.periodicity == "W":
                    periodicity_date = (
                        attempt_date_mailing.date_last_attempt
                        + datetime.timedelta(days=7)
                    )
                    if periodicity_date <= date_time:
                        mailing_client_dict[mailing] = mailing.client_list.all()
                elif mailing.periodicity == "M":
                    periodicity_date = (
                        attempt_date_mailing.date_last_attempt
                        + datetime.timedelta(days=30)
                    )
                    if periodicity_date <= date_time:
                        mailing_client_dict[mailing] = mailing.client_list.all()

    do_send_mail(mailing_client_dict)


def do_send_mail(mailing_client_dict):
    """Футкция для рассылки"""
    print("Колличество рассылок:", len(mailing_client_dict))
    count = 0
    for mailing, client_list in mailing_client_dict.items():
        count += 1
        print(count)
        clients = [client.email for client in client_list]
        try:
            print(
                f"Рассылка: {mailing.message_id.title}\n"
                f"Сообщение: {mailing.message_id.message}\n"
                f"Получатели: {clients}"
            )
            server_response = send_mail(
                subject=mailing.message_id.title,
                message=mailing.message_id.message,
                from_email=EMAIL_HOST_USER,
                recipient_list=clients,
                fail_silently=False,
            )
            Attempt.objects.create(
                status=True,
                server_response=server_response,
                mailing_id=Mailing.objects.get(pk=mailing.id),
                owner=mailing.owner,
            )
        except smtplib.SMTPException as server_response:
            Attempt.objects.create(
                status=False,
                server_response=server_response,
                mailing_id=Mailing.objects.get(pk=mailing.id),
                owner=mailing.owner,
            )


def start():
    """Функция для реализации периодических задач"""
    scheduler = BackgroundScheduler()
    scheduler.add_job(get_mailings, "interval", seconds=10)
    scheduler.start()
