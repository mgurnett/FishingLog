from django import forms
from django.forms import ModelForm, DateInput
#https://docs.djangoproject.com/en/4.2/topics/forms/modelforms/#topics-forms-modelforms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, Button, Row, Column, HTML
from crispy_forms.bootstrap import FormActions
# from ckeditor.widgets import CKEditorWidget
from django_ckeditor_5.widgets import CKEditor5Widget
from .models import *

class DateInput(DateInput):
    input_type = 'date'

class New_Bug_Form (forms.ModelForm):
    class Meta:
        model = Bug
        fields = '__all__'
        widgets = {
            "notes": CKEditor5Widget(
                attrs={"class": "django_ckeditor_5"}, config_name="notes"
            )
        }

    name = forms.CharField ( required = True )       
    notes = forms.CharField ( max_length = 100, required = False ) 
    image = forms.ImageField ( required = True )
    static_tag = forms.CharField ( required = False )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper() 
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='form-group col-md-4 mb-0'),
                Column('static_tag', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('notes'),
                css_class='form-row'
            ),
            Row(
                Column('image', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column(css_class='form-group col-md-7 text-end'),
                Column(Submit('submit', 'Submit', css_class='btn btn-primary col-md-5')),
                Column(FormActions(
                    HTML('<a class="btn btn-primary col-md-3" onclick="window.history.back()">Cancel</a>')
                ),  css_class='btn-primary col-md-3'),
                css_class='form-row'
            ),
        )

# class New_Regions_Form (forms.ModelForm): 
#     class Meta:
#         model = Region
#         fields = '__all__'
#         # fields = ['name', 'notes']
#         widgets = {
#             "notes": CKEditor5Widget(
#                 attrs={"class": "django_ckeditor_5"}, config_name="notes"
#             )
#         }
        
#     name = forms.CharField(required=True)       
#     notes = forms.CharField(required=False)
    
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.helper = FormHelper()
#         self.helper.layout = Layout(
#             Row(
#                 Column('name', css_class='form-group col-md-4 mb-0'),
#                 css_class='form-row'
#             ),
#             Row(
#                 Column('notes', css_class='form-group col-md-12 mb-0'),
#                 css_class='form-row'
#             ),
#             Row(
#                 Column(css_class='form-group col-md-7 text-end'),
#                 Column(Submit('submit', 'Submit', css_class='btn btn-primary col-md-5')),
#                 Column(FormActions(
#                     HTML('<a class="btn btn-primary col-md-3" onclick="window.history.back()">Cancel</a>')
#                 ),  css_class='btn-primary col-md-3'),
#                 css_class='form-row'
#             ),
#         )

class New_Temp_Form (forms.ModelForm): 
    class Meta:
        model = Temp
        fields = ['name', 'notes', 'search_keys']
        widgets = {
            "notes": CKEditor5Widget(
                attrs={"class": "django_ckeditor_5"}, config_name="notes"
            )
        }
        
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
            Row(
                Column(css_class='form-group col-md-7 text-end'),
                Column(Submit('submit', 'Submit', css_class='btn btn-primary col-md-5')),
                Column(FormActions(
                    HTML('<a class="btn btn-primary col-md-3" onclick="window.history.back()">Cancel</a>')
                ),  css_class='btn-primary col-md-3'),
                css_class='form-row'
            ),
        )

class Lake_to_Region_form(forms.ModelForm):
    class Meta:
        model = Lake  # Corrected model
        fields = ['lake']

    lake = forms.ModelChoiceField(queryset=Lake.objects.all(), label="Lake to add:")
              
class New_Hatch_Form (forms.ModelForm):
    
    class Meta:
        model = Hatch
        fields = '__all__'     
        widgets = {
            "notes": CKEditor5Widget(
                attrs={"class": "django_ckeditor_5"}, config_name="notes"
            )
        }
        
    notes = forms.CharField ( required = False )  
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
                Column(css_class='form-group col-md-7 text-end'),
                Column(Submit('submit', 'Submit', css_class='btn btn-primary col-md-5')),
                Column(FormActions(
                    HTML('<a class="btn btn-primary col-md-3" onclick="window.history.back()">Cancel</a>')
                ),  css_class='btn-primary col-md-3'),
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
            Row(
                Column(css_class='form-group col-md-7 text-end'),
                Column(Submit('submit', 'Submit', css_class='btn btn-primary col-md-5')),
                Column(FormActions(
                    HTML('<a class="btn btn-primary col-md-3" onclick="window.history.back()">Cancel</a>')
                ),  css_class='btn-primary col-md-3'),
                css_class='form-row'
            ),
        )
        
class New_Log_Form (forms.ModelForm): 
    
    class Meta:
        model = Log
        # fields = '__all__' 
        fields = ['catch_date', 'notes', 'lake', 'location', 
        'temp', 'fly', 'fly_size', 'fly_colour', 'fish', 'length', 'weight', 'fish_swami', 'num_landed', 'private']  
        widgets = {
            "notes": CKEditor5Widget(
                attrs={"class": "django_ckeditor_5"}, config_name="notes"
            )
        }
        
    catch_date = forms.DateField(
        initial=timezone.now,
        widget=DateInput )
    notes = forms.CharField ( required = False )
    lake = forms.ModelChoiceField(
        queryset=Lake.objects.all())
    location = forms.CharField ( required = False ) 
    temp = forms.ModelChoiceField(
        label='Water Temperature',
        queryset=Temp.objects.all(),
        initial=1,
        required = True )
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
                Column('private',       css_class='form-group col-md-2 mt-12'),
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
            Row(
                Column(css_class='form-group col-md-7 text-end'),
                Column(Submit('submit', 'Submit', css_class='btn btn-primary col-md-5')),
                Column(FormActions(
                    HTML('<a class="btn btn-primary col-md-3" onclick="window.history.back()">Cancel</a>')
                ),  css_class='btn-primary col-md-3'),
                css_class='form-row'
            ),
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

class New_Fly_type_Form (forms.ModelForm):
    class Meta:
        model = Fly_type
        fields = '__all__'
        widgets = {
            "notes": CKEditor5Widget(
                attrs={"class": "django_ckeditor_5"}, config_name="notes"
            )
        }
        
    name = forms.CharField ( required = True )       
    notes = forms.CharField ( required = False )
    image = forms.ImageField (required = False )  
    
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
                Column('image', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column(css_class='form-group col-md-7 text-end'),
                Column(Submit('submit', 'Submit', css_class='btn btn-primary col-md-5')),
                Column(FormActions(
                    HTML('<a class="btn btn-primary col-md-3" onclick="window.history.back()">Cancel</a>')
                ),  css_class='btn-primary col-md-3'),
                css_class='form-row'
            ),
        )

class New_Fish_Form (forms.ModelForm):
    class Meta:
        model = Fish
        fields = '__all__'
        widgets = {
            "notes": CKEditor5Widget(
                attrs={"class": "django_ckeditor_5"}, config_name="notes"
            )
        }

    name = forms.CharField ( required = True )       
    notes = forms.CharField ( required = False )             
    # notes = forms.CharField(widget = CKEditor5Widget())
    abbreviation = forms.CharField ( required = False )
    image = forms.ImageField (required = False )
    static_tag = forms.CharField ( required = False )
    
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
                Column('image', css_class='form-group col-md-8 mb-0'),
                Column('static_tag', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column(css_class='form-group col-md-7 text-end'),
                Column(Submit('submit', 'Submit', css_class='btn btn-primary col-md-5')),
                Column(FormActions(
                    HTML('<a class="btn btn-primary col-md-3" onclick="window.history.back()">Cancel</a>')
                ),  css_class='btn-primary col-md-3'),
                css_class='form-row'
            ),
        )


class New_Lake_Form (forms.ModelForm):
    
    class Meta:
        model = Lake
        fields = [
            'name', 'other_name', 'ats', 'lat', 'long', 'district', 
            'waterbody_id', 'favourite', 'static_tag', 'gps_url', 'reg_location', 'notes'
        ]
        
        widgets = {
            "notes": CKEditor5Widget(
                attrs={"class": "django_ckeditor_5"}, config_name="notes"
            )
        }
        
    name = forms.CharField ( max_length = 100, required = True )  
    other_name = forms.CharField ( max_length = 100, required = False )   
    notes = forms.CharField ( required = False )       
    ats = forms.CharField ( max_length = 100, required = False ) 
    lat = forms.DecimalField( max_digits = 25, decimal_places=20, required = True )  
    long = forms.DecimalField( max_digits = 25, decimal_places=20, required = True)  
    district = forms.ChoiceField( required = False, choices=DISTRICTS, initial='', widget=forms.Select())
    static_tag = forms.CharField( max_length = 100, required = False )
    gps_url = forms.CharField( max_length = 100, required = False )
    reg_location = forms.CharField( max_length = 10, required = False )
    waterbody_id = forms.IntegerField( required = False )
    favourite = forms.BooleanField( required = False )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('name',          css_class='form-group col-md-5 mb-0'),
                Column('other_name',    css_class='form-group col-md-4 mb-0'),
                Column('favourite',     css_class='form-group col-md-2 mt-4'),
                css_class='form-row'
            ),
            Row(
                Column('district',      css_class='form-group col-md-3 mb-0'),
                Column('static_tag',    css_class='form-group col-md-4 mb-0'),
                Column('reg_location',  css_class='form-group col-md-3 mb-0'),
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
                Column('gps_url',       css_class='form-group col-md-7 mb-0'),
                Column(Submit('submit', 'Submit', css_class='btn-primary col-md-5 mb-0')),
                Column(FormActions(
                    HTML('<a class="btn btn-primary col-md-3" onclick="window.history.back()">Cancel</a>')
                ), 
                css_class='btn-primary col-md-3 mb-0')
            ),
        )


# class New_Regions_Form (forms.Form):

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.helper = FormHelper()
#         self.helper.layout = Layout(
#             Fieldset(
#                 'first arg is the legend of the fieldset',
#                 'name',
#                 'notes'
#             ),
#             Submit('submit', 'Submit', css_class='button white'),
#         )

class New_Regions_For (forms.ModelForm):
      """Form for comments to the article."""

      def __init__(self, *args, **kwargs):
          super().__init__(*args, **kwargs)
          self.fields["notes"].required = False

      class Meta:
          model = Region
          fields = ("name", "notes")
          widgets = {
              "notes": CKEditor5Widget(
                  attrs={"class": "django_ckeditor_5"}, config_name="notes"
              )
          }