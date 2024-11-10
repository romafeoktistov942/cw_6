import json
from datetime import datetime
from pathlib import Path
from django.db import connection
from django.core.management import BaseCommand

from mailing.models import Mailing, Client, Message, Attempt


class Command(BaseCommand):
    def load_data(self) -> list[dict]:
        """Метод для загрузки данных из json"""
        ROOT_PATH = Path(__file__).parent.parent.parent.parent
        DATA_PATH = ROOT_PATH.joinpath("mailing.json")
        with open(DATA_PATH, "rt", encoding="UTF-8") as file:
            mailing = json.load(file)
        return mailing

    def get_message(self, message) -> list:
        """Метод для получения списка экземпляров Класса Message для заполнения базы данных"""
        message_for_create = []
        for item in message:
            data = item["fields"]
            if item["model"] == "mailing.message":
                message_for_create.append(
                    Message(
                        pk=item["pk"],
                        title=data["title"],
                        message=data["message"],
                        image=data.get("image", None),
                        created_at=data["created_at"],
                        update_at=data.get("update_at", datetime.now()),
                    )
                )
        return message_for_create

    def get_client(self, client):
        """Метод для получения списка экземпляров Класса Client для заполнения базы данных"""
        client_for_create = []
        for item in client:
            data = item["fields"]
            if item["model"] == "mailing.client":
                client_for_create.append(
                    Client(
                        email=data["email"],
                        name=data.get("name", None),
                        comment=data.get("comment", None),
                        pk=item["pk"],
                    )
                )
        return client_for_create

    def get_mailing(self, mailing) -> list:
        """Метод для получения списка экземпляров Класса Mailing для заполнения базы данных"""
        mailing_for_create = []
        for item in mailing:
            data = item["fields"]
            if item["model"] == "mailing.mailing":
                mailing = Mailing.objects.create(
                    pk=item["pk"],
                    date_of_first_dispatch=data.get("date_of_first_dispatch", None),
                    periodicity=data.get("periodicity", None),
                    status=data.get("status", None),
                    datetime_to_start=data.get("datetime_to_start", None),
                    created_at=data.get("created_at", None),
                    update_at=data.get("update_at", None),
                    message_id=Message.objects.get(pk=data.get("message_id")),
                )
                clients = Client.objects.filter(pk__in=data.get("client_list", []))
                mailing.client_list.set(clients)

                mailing_for_create.append(mailing)
        return mailing_for_create

    def get_attempt(self, attempt) -> list:
        """Метод для получения списка экземпляров Класса Attempt для заполнения базы данных"""
        attempt_for_create = []
        for item in attempt:
            data = item["fields"]
            if item["model"] == "mailing.attempt":
                attempt_for_create.append(
                    Attempt(
                        date_first_attempt=data.get("date_first_attempt", None),
                        date_last_attempt=data.get("date_last_attempt", None),
                        status=data.get("status", None),
                        server_response=data.get("server_response", None),
                        mailing_id=Mailing.objects.get(pk=data["mailing_id"]),
                        pk=item["pk"],
                    )
                )
        return attempt_for_create

    def handle(self, *args, **options) -> None:
        """Метод автоматически срабатывает при обращении к коменде fill"""

        print("Загрузка данных")
        mailing = self.load_data()

        print("Очистка Базы данных")
        Message.objects.all().delete()
        Client.objects.all().delete()
        Mailing.objects.all().delete()
        Attempt.objects.all().delete()

        with connection.cursor() as cursor:
            cursor.execute(f"TRUNCATE TABLE mailing_message RESTART IDENTITY CASCADE;")
        with connection.cursor() as cursor:
            cursor.execute(f"TRUNCATE TABLE mailing_client RESTART IDENTITY CASCADE;")
        with connection.cursor() as cursor:
            cursor.execute(f"TRUNCATE TABLE mailing_mailing RESTART IDENTITY CASCADE;")
        with connection.cursor() as cursor:
            cursor.execute(f"TRUNCATE TABLE mailing_attempt RESTART IDENTITY CASCADE;")
        with connection.cursor() as cursor:
            cursor.execute(
                f"TRUNCATE TABLE mailing_mailing_client_list RESTART IDENTITY CASCADE;"
            )

        print("Создание Сообщений")
        message_for_create = self.get_message(mailing)
        Message.objects.bulk_create(message_for_create)

        print("Создание Клиентов")
        client_for_create = self.get_client(mailing)
        Client.objects.bulk_create(client_for_create)

        print("Создание Рассылок")
        mailing_for_create = self.get_mailing(mailing)
        print("Рассылки созданы уже ранее")
        # Mailing.objects.bulk_create(mailing_for_create)

        print("Создание Попыток")
        attempt_for_create = self.get_attempt(mailing)
        Attempt.objects.bulk_create(attempt_for_create)


