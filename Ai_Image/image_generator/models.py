from django.db import models

# Create your models here.

# Define the GenerateImage model to store image data.
class GenerateImage(models.Model):
    prompt = models.CharField(max_length=255)
    index = models.IntegerField()
    file_path = models.CharField(max_length=255)
    created_at = models.DateField(auto_now_add=True)

    # Define how the model is represented as a string.
    def __str__(self):
        return f"Image {self.index} for prompt : {self.prompt}"