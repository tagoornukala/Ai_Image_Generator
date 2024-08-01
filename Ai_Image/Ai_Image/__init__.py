# Import the Celery app instance from the 'celery_app' module.
# This ensures that the Celery app is loaded when Django starts.
from .celery_app import app as celery_app

# Specify which objects are available for import from this module.
# Here, we're making the 'celery_app' object available to other modules.
__all__ = ('celery_app',)