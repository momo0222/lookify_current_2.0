# Generated by Django 4.2.3 on 2024-06-21 23:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organizationprofile',
            name='website',
            field=models.URLField(blank=True),
        ),
    ]
