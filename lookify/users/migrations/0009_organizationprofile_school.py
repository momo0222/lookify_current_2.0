# Generated by Django 4.2.3 on 2024-08-08 01:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_merge_0006_alter_profile_school_0007_fix_school_field'),
    ]

    operations = [
        migrations.AddField(
            model_name='organizationprofile',
            name='school',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.school'),
        ),
    ]
