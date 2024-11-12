from openai import OpenAI
from .models import *
from django.conf import settings

def ai_plan (temp, date, wind = "lite", direction = "north", sky = "partly cloudy" ):

    question = str(f"Lake water temp is {temp}, wind is {wind} from the {direction}, sky is {sky}, please suggest a fly to use for rainbow trout in a Northern Alberta lake on {date}")
    # print (question)

    client = OpenAI(
        api_key = settings.GEMINI_KEY,
        base_url="https://generativelanguage.googleapis.com/v1beta/"
    )

    response = client.chat.completions.create(
        model="gemini-1.5-flash",
        n=1,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {
                "role": "user",
                "content": question
            }
        ]
    )
    print (response.choices[0].message.content)
    return (response.choices[0].message.content)
