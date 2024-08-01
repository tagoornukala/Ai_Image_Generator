from django.contrib import admin
from .models import GenerateImage

# Customize the admin interface for the GenerateImage model.
class GenerateImage_Admin(admin.ModelAdmin):
    # Show these fields in the list view on the admin page.
    list_display = ['prompt','index','file_path','created_at']

# Register the GenerateImage model with the custom admin interface.
admin.site.register(GenerateImage,GenerateImage_Admin)