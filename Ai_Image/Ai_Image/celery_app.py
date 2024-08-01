import os
from celery import Celery

# Set the environment variable for Django settings.
# This tells Celery where to find the Django configuration.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Ai_Image.settings')

# Create a Celery application named 'Ai_Image'.
app = Celery('Ai_Image')

# Load Celery settings from Django settings.
# Look for settings starting with 'CELERY_'.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Find and register Celery tasks from all installed Django apps.
app.autodiscover_tasks()
