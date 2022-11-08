# Generated by Django 4.1.3 on 2022-11-08 12:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Chatroom",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        help_text="Enter name of the chatroom", max_length=255
                    ),
                ),
                (
                    "summary",
                    models.TextField(
                        help_text="Enter summary of the chatroom", max_length=1000
                    ),
                ),
                (
                    "is_public",
                    models.BooleanField(
                        default=False,
                        help_text="Choose whether the chatroom should be public",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "created_by",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="chatroom_as_owner",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "user",
                    models.ManyToManyField(
                        related_name="chatroom_as_member", to=settings.AUTH_USER_MODEL
                    ),
                ),
            ],
            options={
                "ordering": ["-created_at", "name"],
            },
        ),
        migrations.CreateModel(
            name="Message",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "content",
                    models.TextField(
                        help_text="Enter message content", max_length=1000
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "chatroom",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="chatroom.chatroom",
                    ),
                ),
            ],
        ),
    ]
