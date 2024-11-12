from catches.models import *
from catches.ai_plan import *

def run():
        answer = ai_plan ("5C", "November 9")
        
        print (answer[0])