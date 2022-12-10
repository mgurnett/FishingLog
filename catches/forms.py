from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column
from .models import *

class New_Regions_Form (forms.ModelForm): 
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

class New_Fly_type_Form (forms.ModelForm):
    class Meta:
        model = Fly_type
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

class New_Fish_Form (forms.ModelForm):
    
    class Meta:
        model = Fish
        fields = '__all__'
    name = forms.CharField ( required = True )       
    notes = forms.CharField ( required = False )      
    abbreviation = forms.CharField ( required = False )
    image = forms.ImageField (required = False )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='form-group col-md-4 mb-0'),
                Column('abbreviation', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('notes', css_class='form-group col-md-12 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('image', css_class='form-group col-md-12 mb-0'),
                css_class='form-row'
            ),
            Submit('submit', 'Save')
        )
    class Meta:
        model = Fly_type
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

class New_Bug_Form (forms.ModelForm):
    
    class Meta:
        model = Bug
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
            Row(
                Column('notes', css_class='form-group col-md-12 mb-0'),
                css_class='form-row'
            ),
            Submit('submit', 'Save')
        )