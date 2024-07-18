import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lookify.settings')

print(f"DJANGO_SETTINGS_MODULE is set to: {os.environ.get('DJANGO_SETTINGS_MODULE')}")

try:
    django.setup()
    print("Django setup completed successfully.")
except Exception as e:
    print(f"Error during Django setup: {e}")
