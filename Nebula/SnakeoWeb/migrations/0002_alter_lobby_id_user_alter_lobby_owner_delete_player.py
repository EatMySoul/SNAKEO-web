# Generated by Django 4.2.2 on 2023-11-09 00:56

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('SnakeoWeb', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lobby',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('lobby', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='SnakeoWeb.lobby')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AlterField(
            model_name='lobby',
            name='owner',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='lobby_owner', to='SnakeoWeb.user'),
        ),
        migrations.DeleteModel(
            name='Player',
        ),
    ]
