from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('generate/', views.trigger_image_generation, name='generate_images'),
]
