# Generated by Django 4.2.3 on 2024-08-02 05:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('opportunity', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='opportunity',
            name='application_type',
            field=models.URLField(blank=True, null=True),
        ),
    ]
