from celery import shared_task
import requests
import base64
import os
from django.conf import settings
from celery.exceptions import TimeLimitExceeded
from .models import GenerateImage

@shared_task(bind=True, max_retries=3, default_retry_delay=300)  
def generate_image(self, prompt, index):
    
    try:
        # Create the output directory if it doesn't exist
        output_dir = "./staticfiles/images"
        os.makedirs(output_dir, exist_ok=True)
        
        # Get API key and other settings
        api_key = settings.STABILITY_API_KEY
        api_host = "https://api.stability.ai"
        engine_id = "stable-diffusion-xl-1024-v1-0"

        if api_key is None:
            raise Exception("Missing Stability API key.")

        payload = {
            "text_prompts": [
                {"text": prompt}
            ],
            "cfg_scale": 7,
            "clip_guidance_preset": "FAST_BLUE",
            "height": 1024,
            "width": 1024,
            "samples": 1,
            "steps": 30,
        }

        # Send request to generate image
        response = requests.post(
            f"{api_host}/v1/generation/{engine_id}/text-to-image",
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json",
                "Authorization": f"Bearer {api_key}"
            },
            json=payload,
            timeout=60  # Timeout for the request
        )

        if response.status_code != 200:
            raise Exception(f"Non-200 response: {response.status_code} - {response.text}")
        
        data = response.json()

        if 'artifacts' not in data:
            raise Exception("Unexpected response format: 'artifacts' key missing")

        artifacts = data['artifacts']
        if not artifacts:
            raise Exception("No 'artifacts' found in the response")

        # Save images and create database entries
        for i, image in enumerate(artifacts):
            file_path = os.path.join(output_dir, f"generated_image_{index}_{i}.png")
            with open(file_path, "wb") as f:
                f.write(base64.b64decode(image["base64"]))

            GenerateImage.objects.create(
                prompt=prompt,
                index=index,
                file_path=file_path
            )
        return f"Task Completed for prompt {index}"
    except TimeLimitExceeded:
        return f"Task timed out for prompt {index}"
    except Exception as e:
        return f"Task failed for prompt {index}: {str(e)}"