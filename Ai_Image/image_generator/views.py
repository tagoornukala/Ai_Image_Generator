# myapp/views.py
from django.http import HttpResponse
from django.shortcuts import render
from .tasks import generate_image
from celery import group
from .models import GenerateImage

def trigger_image_generation(request):
    # Define prompts for image generation
    prompts = [
        "A red flying dog",
        "A piano ninja",
        "A footballer kid"
    ]

    # Create a group of image generation tasks with different prompts
    task_group = group(generate_image.s(prompt, index) for index, prompt in enumerate(prompts))
    
    # Run the tasks in parallel
    result = task_group.apply_async()
    print(result)
    
    # Return a response indicating tasks have been triggered
    return HttpResponse("Image generation tasks have been triggered in parallel.")
