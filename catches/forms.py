from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, HTML
from crispy_forms.bootstrap import FormActions
from ckeditor.widgets import CKEditorWidget
from .models import *


class DateInput(forms.DateInput):
    input_type = 'date'

 
class New_Regions_Form (forms.ModelForm): 
    class Meta:
        model = Region
        fields = '__all__'
    name = forms.CharField(required=True)       
    notes = forms.CharField(required=False)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            'notes',
            Submit('submit', 'Save'),
        )
        self.helper.layout.append(
            FormActions(
                HTML('<a class="btn btn-primary" onclick="window.history.back()">Cancel</a>')
            )
        )

class New_Temp_Form (forms.ModelForm): 
    class Meta:
        model = Temp
        fields = '__all__'
    name = forms.CharField ( required = True )       
    notes = forms.CharField ( required = False )
    search_keys = forms.CharField ( required = True )     
    
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
            Row(
                Column('search_keys', css_class='form-group col-md-12 mb-0'),
                css_class='form-row'
            ),
            Submit('submit', 'Save')
        )

# class New_Fly_type_Form (forms.ModelForm):
#     class Meta:
#         model = Fly_type
#         fields = '__all__'
#     name = forms.CharField ( required = True )       
#     notes = forms.CharField ( required = False )
#     image = forms.ImageField (required = False )  
    
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.helper = FormHelper()
#         self.helper.layout = Layout(
#             Row(
#                 Column('name', css_class='form-group col-md-4 mb-0'),
#                 css_class='form-row'
#             ),
#             'notes',
#             Row(
#                 Column('image', css_class='form-group col-md-6 mb-0'),
#                 css_class='form-row'
#             ),
#             Submit('submit', 'Save')
#         )

# class New_Fish_Form (forms.ModelForm):
    
#     class Meta:
#         model = Fish
#         fields = '__all__'
#     name = forms.CharField ( required = True )       
#     notes = forms.CharField ( required = False )      
#     abbreviation = forms.CharField ( required = False )
#     image = forms.ImageField (required = False )
#     static_tag = forms.CharField ( required = False )
    
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.helper = FormHelper()
#         self.helper.layout = Layout(
#             Row(
#                 Column('name', css_class='form-group col-md-4 mb-0'),
#                 Column('abbreviation', css_class='form-group col-md-4 mb-0'),
#                 css_class='form-row'
#             ),
#             Row(
#                 Column('notes', css_class='form-group col-md-12 mb-0'),
#                 css_class='form-row'
#             ),
#             Row(
#                 Column('image', css_class='form-group col-md-8 mb-0'),
#                 Column('static_tag', css_class='form-group col-md-4 mb-0'),
#                 css_class='form-row'
#             ),
#             Submit('submit', 'Save')
#         )

# class New_Bug_Form (forms.ModelForm):
    
#     class Meta:
#         model = Bug
#         fields = '__all__'
#     name = forms.CharField ( required = True )       
#     notes = forms.CharField ( required = False )  
#     image = forms.ImageField (required = False )
#     static_tag = forms.CharField ( required = False )
    
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.helper = FormHelper()
#         self.helper.layout = Layout(
#             Row(
#                 Column('name', css_class='form-group col-md-4 mb-0'),
#                 Column('static_tag', css_class='form-group col-md-4 mb-0'),
#                 css_class='form-row'
#             ),
#             Row(
#                 Column('notes', css_class='form-group col-md-12 mb-0'),
#                 css_class='form-row'
#             ),
#             Row(
#                 Column('image', css_class='form-group col-md-6 mb-0'),
#                 css_class='form-row'
#             ),
#             Submit('submit', 'Save')
#         )

class New_Lake_Form (forms.ModelForm):
    
    class Meta:
        model = Lake
        fields = ['name', 'other_name', 'notes', 'ats', 'lat', 'long', 
        'district', 'waterbody_id', 'favourite', 'region', 'static_tag', 'gps_url']

    name = forms.CharField ( max_length = 100, required = True )  
    other_name = forms.CharField ( max_length = 100, required = False )      
    notes = forms.CharField ( widget = CKEditorWidget(), max_length = 100, required = False )      
    ats = forms.CharField ( max_length = 100, required = False ) 
    lat = forms.DecimalField( max_digits = 25, decimal_places=20, required = True )  
    long = forms.DecimalField( max_digits = 25, decimal_places=20, required = True)  
    district = forms.ChoiceField( required = False, choices=DISTRICTS, initial='', widget=forms.Select())
    static_tag = forms.CharField( max_length = 100, required = True )
    gps_url = forms.CharField( max_length = 100, required = False )
    waterbody_id = forms.IntegerField( required = False )
    favourite = forms.BooleanField( required = False )
    region = forms.ModelChoiceField(
        queryset=Region.objects.all(),
        required = False )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('name',          css_class='form-group col-md-5 mb-0'),
                Column('other_name',    css_class='form-group col-md-4 mb-0'),
                Column('favourite',     css_class='form-group col-md-2 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('district',      css_class='form-group col-md-3 mb-0'),
                Column('static_tag',    css_class='form-group col-md-4 mb-0'),
                Column('region',        css_class='form-group col-md-3 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('ats',           css_class='form-group col-md-2 mb-0'),
                Column('lat',           css_class='form-group col-md-3 mb-0'),
                Column('long',          css_class='form-group col-md-3 mb-0'),
                Column('waterbody_id',  css_class='form-group col-md-2 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('notes',         css_class='form-group col-md-10 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('gps_url',       css_class='form-group col-md-10 mb-0'),
                css_class='form-row'
            ),
            Submit('submit', 'Save')
        )
              
class New_Hatch_Form (forms.ModelForm):
    
    class Meta:
        model = Hatch
        fields = '__all__'     
    notes = forms.CharField ( widget = CKEditorWidget(), required = False )  
    static_tag = forms.CharField ( required = False )
    sight_date = forms.DateField(
        initial=timezone.now,
        widget=DateInput )

    lake = forms.ModelChoiceField(
        queryset=Lake.objects.all(),
        required = False )

    bug = forms.ModelChoiceField(
        queryset=Bug.objects.all(),
        required = False )

    week = forms.ModelChoiceField(
        queryset=Week.objects.all(),
        required = False )

    temp = forms.ModelChoiceField(
        queryset=Temp.objects.all(),
        required = False )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('', css_class='form-group col-md-2 mb-0'),
                Column('bug', css_class='form-group col-md-3 mb-0'),
                Column('lake', css_class='form-group col-md-3 mb-0'),
                Column('sight_date', css_class='form-group col-md-3 mb-0'),
                Column('', css_class='form-group col-md-2 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('', css_class='form-group col-md-2 mb-0'),
                Column('week', css_class='form-group col-md-3 mb-0'),
                Column('temp', css_class='form-group col-md-3 mb-0'),
                Column('static_tag', css_class='form-group col-md-3 mb-0'),
                Column('', css_class='form-group col-md-2 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('', css_class='form-group col-md-2 mb-0'),
                Column('notes', css_class='form-group col-md-8 mb-0'),
                Column('', css_class='form-group col-md-2 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('', css_class='form-group col-md-8 mb-0'),
                Submit('submit', 'Save'),
                css_class='form-row'
            ),
        )

class New_Stock_Form (forms.ModelForm):
    
    class Meta:
        model = Stock
        fields = '__all__'     

    date_stocked = forms.DateField(
        widget=forms.widgets.DateInput(format="%m/%d/%Y") )
    number = forms.IntegerField ( required = True )
    length = forms.DecimalField ( required = True )
    strain = forms.ChoiceField(choices = STRAIN, initial='', widget=forms.Select(), required=False)
    gentotype = forms.ChoiceField(choices = GENTOTYPE, initial='', widget=forms.Select(), required=False)

    lake = forms.ModelChoiceField(
        queryset=Lake.objects.all() )

    fish = forms.ModelChoiceField(
        queryset=Fish.objects.all() )
 
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('date_stocked', css_class='form-group col-md-4 mb-0'),
                Column('lake', css_class='form-group col-md-8 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('fish', css_class='form-group col-md-4 mb-0'),
                Column('gentotype', css_class='form-group col-md-4 mb-0'),
                Column('strain', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('number', css_class='form-group col-md-4 mb-0'),
                Column('length', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Submit('submit', 'Save')
        )
        
class New_Log_Form (forms.ModelForm): 
    
    class Meta:
        model = Log
        # fields = '__all__' 
        fields = ['catch_date', 'notes', 'lake', 'location', 
        'temp', 'fly', 'fly_size', 'fly_colour', 'fish', 'length', 'weight', 'fish_swami', 'num_landed', 'private']  
    catch_date = forms.DateField(
        initial=timezone.now,
        widget=DateInput )
    notes = forms.CharField ( widget = CKEditorWidget(), required = False )
    lake = forms.ModelChoiceField(
        queryset=Lake.objects.all())
    location = forms.CharField ( required = False ) 
    temp = forms.ModelChoiceField(
        label='Water Temperature',
        queryset=Temp.objects.all(),
        required = False )
    fly = forms.ModelChoiceField(
        queryset=Fly.objects.all(),
        required = False )
    fly_size = forms.CharField ( required = False ) 
    fly_colour = forms.CharField ( required = False ) 
    fish = forms.ModelChoiceField(
        queryset=Fish.objects.all(), required = False )
    length = forms.CharField ( required = False, initial=0.0 ) 
    weight = forms.CharField ( required = False, initial=0.0 ) 
    fish_swami = forms.IntegerField ( required = False, initial=0 ) 
    num_landed = forms.IntegerField ( required = False, initial=0 ) 
    private = forms.BooleanField( required = False, initial=False )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('lake',          css_class='form-group col-md-3 mb-0'),
                Column('location',      css_class='form-group col-md-3 mb-0'),
                Column('temp',          css_class='form-group col-md-2 mb-0'),
                Column('catch_date',    css_class='form-group col-md-2 mb-0'),
                Column('fish_swami',    css_class='form-group col-md-2 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('fish',          css_class='form-group col-md-4 mb-0'),
                Column('length',        css_class='form-group col-md-2 mb-0'),
                Column('weight',        css_class='form-group col-md-2 mb-0'),
                Column('num_landed',    css_class='form-group col-md-2 mb-0'),
                Column('private',       css_class='form-group col-md-2 mt-8'),
                css_class='form-row'
            ),
            Row(
                Column('fly',           css_class='form-group col-md-4 mb-0'),
                Column('fly_size',      css_class='form-group col-md-4 mb-0'),
                Column('fly_colour',    css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('notes',         css_class='form-group col-md-12 mb-0'),
                css_class='form-row'
            ),
            Submit('submit', 'Save')
        )
        
class Plan_form (forms.ModelForm):
    class Meta:
        model = Week
        fields = ['number']
        
    number = forms.ModelChoiceField( queryset=Week.objects.all(), label="Week number:" )

    def __init__ (self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column(''),
                css_class='form-row'
            )
        )