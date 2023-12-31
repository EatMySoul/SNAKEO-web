# Generated by Django 4.2.2 on 2023-11-09 19:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('SnakeoWeb', '0003_lobbyuser_alter_lobby_owner_delete_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lobby',
            name='owner',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='lobby_owner', to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='LobbyUser',
        ),
    ]
