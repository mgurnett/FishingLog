from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column
from .models import Region

class New_Regions_Form (forms.ModelForm): #https://docs.djangoproject.com/en/4.1/ref/forms/fields/
    class Meta:
        model = Region
        fields = '__all__'
    name = forms.CharField ( required = True )       
    notes = forms.CharField ( required = False )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            'notes',
            Submit('submit', 'Save')
        )