from openai import OpenAI
from .models import *
from django.conf import settings

client = OpenAI(
    api_key=settings.GOOGLE_MAPS_API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/"
)

def get_answer (question):
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

    return (response.choices[0].message.content)

questions = [
    "If I provide you with some helpful details like a water temp of 5C, cloudy skys, can you help me pick a fly that will catch trout in Northern Alberta today?",
    "Lake water temp is 5C, wind is light from the north, sky is cloudy, please suggest a fly to use for rainbow trout in a Northern Alberta lake on November 9 in markdown format"
    ]

def build_question (temp, wind, direction, sky, date ):
    question = str(f"Lake water temp is {temp}, wind is {wind} from the {direction}, sky is {sky}, please suggest a fly to use for rainbow trout in a Northern Alberta lake on {date}")
    return question

def get_ai_plan (temp_pk, week_pk, wind = "lite", direction = "north", sky = "partly cloudy" ):
    week = Week.objects.get(pk = week_pk)
    plan_date = week.dates_in_week.start_date 
    temp = Temp.objects.get(pk=temp_pk)
    plan_temp = f'{temp.deg}C'

    question = build_question (plan_temp, wind, direction, sky, plan_date )
    answer = get_answer (question)
    return answer

if __name__ == '__main__':
    question = build_question ("5C", "light", "west", "cloudy", "November 9" )
    answer = get_answer (question)

    
    print (answer)
