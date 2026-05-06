from google import genai
from catches.models import *
from django.conf import settings

def ai_plan(temp, date, wind="lite", direction="north", sky="partly cloudy"):
    question = f"Lake water temp is {temp}, wind is {wind} from the {direction}, sky is {sky}, please suggest a fly to use for rainbow trout in a Northern Alberta lake on {date}"

    # The new SDK handles the base URL automatically
    client = genai.Client(api_key=settings.GEMINI_KEY)

    # Change from gemini-2.0-flash to gemini-1.5-flash
    response = client.models.generate_content(
        model="gemini-2.5-flash",  # Update this string
        config={
            "system_instruction": "You are an expert fly fishing guide."
        },
        contents=question
    )
    
    return response.text