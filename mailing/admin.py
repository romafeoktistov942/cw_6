from django.contrib import admin

from mailing.models import Message, Mailing, Client, Attempt


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "message",
        "created_at",
        "update_at",
        "owner",
    )
    list_filter = (
        "created_at",
        "update_at",
    )
    search_fields = (
        "title",
        "message",
    )


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "date_of_first_dispatch",
        "periodicity",
        "status",
        "created_at",
        "update_at",
        "message_id",
        "owner",
        Mailing.get_clients,
    )
    list_filter = ("message_id", "status")
    search_fields = ("periodicity",)


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "email",
        "name",
        "comment",
        "owner",
    )
    list_filter = (
        "name",
        "email",
    )
    search_fields = (
        "name",
        "email",
        "comment",
    )


@admin.register(Attempt)
class AttemptAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "date_last_attempt",
        "status",
        "server_response",
        "mailing_id",
        "owner",
    )
    list_filter = ("status",)
    search_fields = (
        "date_last_attempt",
        "server_response",
    )
