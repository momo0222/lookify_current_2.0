# Generated by Django 4.2.3 on 2024-08-07 21:56

from django.db import migrations

def fix_invalid_school_values(apps, schema_editor):
    Profile = apps.get_model('users', 'Profile')
    School = apps.get_model('users', 'School')
    default = School.objects.get(name__icontains="Dougherty Valley High")
    if default:
        Profile.objects.update(school=default.id)
    else:
        raise ValueError('School not foun')
    

    # Set all "N/A" values in the school field to NULL
    
class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_school'),
    ]

    operations = [
        migrations.RunPython(fix_invalid_school_values),
    ]