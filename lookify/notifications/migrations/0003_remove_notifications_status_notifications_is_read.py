# Generated by Django 4.2.5 on 2024-07-16 05:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0002_notifications_created_at'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notifications',
            name='status',
        ),
        migrations.AddField(
            model_name='notifications',
            name='is_read',
            field=models.BooleanField(default=False),
        ),
    ]
