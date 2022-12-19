from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column
from .models import Fly

class New_Flys_Form (forms.ModelForm): 
    class Meta:
        model = Fly
        fields = '__all__'