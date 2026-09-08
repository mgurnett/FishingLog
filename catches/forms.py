import datetime
from django import forms
from django.forms import ModelForm, DateInput
from django.utils import timezone
#https://docs.djangoproject.com/en/4.2/topics/forms/modelforms/#topics-forms-modelforms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Field, Submit, Button, Row, Column, HTML
from crispy_forms.bootstrap import FormActions
# from ckeditor.widgets import CKEditorWidget
from django_ckeditor_5.widgets import CKEditor5Widget
from .models import *
from catches.helpers.fish_data import *

class CustomDateInput(forms.DateInput):
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
    notes = forms.CharField(
        widget=CKEditor5Widget(attrs={"class": "django_ckeditor_5"}, config_name="notes"),
        required=False
    )
    image = forms.ImageField ( required = False )
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
        widget=CustomDateInput # <-- Use the renamed class here
    )

    lake = forms.ModelChoiceField(
        queryset=Lake.objects.all(),
        required = True )

    bug = forms.ModelChoiceField(
        queryset=Bug.objects.all(),
        required = True )

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
                Column('bug', css_class='form-group col-md-4 mb-3'),
                Column('lake', css_class='form-group col-md-4 mb-3'),
                Column('sight_date', css_class='form-group col-md-4 mb-3'),
                css_class='form-row'
            ),
            Row(
                Column('week', css_class='form-group col-md-4 mb-3'),
                Column('temp', css_class='form-group col-md-4 mb-3'),
                Column('static_tag', css_class='form-group col-md-4 mb-3'),
                css_class='form-row'
            ),
            Row(
                Column('notes', css_class='form-group col-md-12 mb-3'),
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
        
class New_Log_Form(forms.ModelForm): 
    
    class Meta:
        model = Log
        fields = [
            'catch_date', 'catch_time', 'notes', 'lake', 'location', 
            'temp', 'fly', 'fly_size', 'fly_colour', 'fish', 'length', 
            'weight', 'fish_swami', 'num_landed', 'private', 
            'strategy', 'setup',
            'lake_depth', 'gps_lat', 'gps_long', 'catch_depth', 'live'
        ]
        
    catch_date = forms.DateField(
        initial=datetime.date.today,
        input_formats=['%Y-%m-%d', '%m/%d/%Y'],
        widget=forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date', 'class': 'form-control'})
    )
        
    catch_time = forms.TimeField(
        required=False, 
        input_formats=['%H:%M', '%H:%M:%S'],
        widget=forms.TimeInput(format='%H:%M', attrs={'type': 'time', 'class': 'form-control'})
    )
            
    notes = forms.CharField(
        required=False,
        widget=CKEditor5Widget(attrs={"class": "django_ckeditor_5"}, config_name="notes")
    )
    
    lake = forms.ModelChoiceField(queryset=Lake.objects.all())
    location = forms.CharField(required=False) 
    temp = forms.ModelChoiceField(
        label='Water Temperature',
        queryset=Temp.objects.all(),
        required=False,
        empty_label="-- Select Water Temp (Optional) --"
    )
    fly = forms.ModelChoiceField(queryset=Fly.objects.all(), required=False)
    fly_size = forms.CharField(required=False) 
    fly_colour = forms.CharField(required=False) 
    fish = forms.ModelChoiceField(queryset=Fish.objects.all(), required=False)
    
    strategy = forms.ModelChoiceField(
        queryset=Strategy.objects.all(),
        required=False,
        label="Fishing Strategy"
    )
    setup = forms.ModelChoiceField(
        queryset=Setup.objects.all(),
        required=False,
        label="Line Setup / Rig"
    )
    
    live = forms.BooleanField(required=False, initial=False, label="Live Catch")
    
    lake_depth = forms.FloatField(required=False, label="Lake Depth (ft)")
    catch_depth = forms.FloatField(required=False, label="Catch Depth (ft)")
    
    gps_lat = forms.FloatField(required=False, widget=forms.TextInput(attrs={'readonly': 'readonly', 'placeholder': 'Check Live to fetch...'}))
    gps_long = forms.FloatField(required=False, widget=forms.TextInput(attrs={'readonly': 'readonly', 'placeholder': 'Check Live to fetch...'}))
    
    length = forms.CharField(required=False, initial=0.0)
    length_unit = forms.ChoiceField(
        choices=[('cm', 'cm'), ('in', 'inches')],
        widget=forms.RadioSelect,
        initial='cm',
        label="Unit"
    )
    
    weight = forms.CharField(required=False, initial=0.0)
    weight_unit = forms.ChoiceField(
        choices=[('kg', 'kg'), ('lbs', 'lbs')],
        widget=forms.RadioSelect,
        initial='kg',
        label="Unit"
    )
    
    fish_swami = forms.IntegerField(required=False, initial=0) 
    num_landed = forms.IntegerField(required=False, initial=0) 
    private = forms.BooleanField(required=False, initial=False)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['strategy'].queryset = Strategy.objects.all().order_by('name')
        self.fields['strategy'].empty_label = "-- Select Strategy (Optional) --"
        self.fields['setup'].queryset = Setup.objects.all().order_by('name')
        self.fields['setup'].empty_label = "-- Select Setup / Rig (Optional) --"

        # Safely localize formatting for UpdateViews without altering data types globally
        if self.instance and self.instance.pk:
            if self.instance.catch_date and hasattr(self.instance.catch_date, 'strftime'):
                self.initial['catch_date'] = self.instance.catch_date.strftime('%Y-%m-%d')
            if self.instance.catch_time and hasattr(self.instance.catch_time, 'strftime'):
                self.initial['catch_time'] = self.instance.catch_time.strftime('%H:%M')

        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('lake',          css_class='form-group col-md-3 mb-0'),
                Column('location',      css_class='form-group col-md-3 mb-0'),
                Column('temp',          css_class='form-group col-md-2 mb-0'),
                Column('catch_date',    css_class='form-group col-md-2 mb-0'),
                Column('catch_time',    css_class='form-group col-md-2 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('fish',          css_class='form-group col-md-3 mb-0'),
                Column('length',        css_class='form-group col-md-2 mb-0'),
                Column('length_unit',   css_class='form-group col-md-1 mb-0 custom-inline-radios'),
                Column('weight',        css_class='form-group col-md-2 mb-0'),
                Column('weight_unit',   css_class='form-group col-md-1 mb-0 custom-inline-radios'),
                Column('num_landed',    css_class='form-group col-md-2 mb-0'),
                Column('private',       css_class='form-group col-md-1 mb-0 pt-4'),
                css_class='form-row'
            ),
            Row(
                Column('strategy',      css_class='form-group col-md-6 mb-0'),
                Column('setup',         css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('fly',           css_class='form-group col-md-4 mb-0'),
                Column('fly_size',      css_class='form-group col-md-3 mb-0'),
                Column('fly_colour',    css_class='form-group col-md-3 mb-0'),
                Column('fish_swami',    css_class='form-group col-md-2 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column(Field('live', id='id_live'), css_class='form-group col-md-1 mb-0 pt-4'),
                Column('lake_depth',    css_class='form-group col-md-2 mb-0'),
                Column('catch_depth',   css_class='form-group col-md-3 mb-0'),
                Column('gps_lat',       css_class='form-group col-md-3 mb-0'),
                Column('gps_long',      css_class='form-group col-md-3 mb-0'),
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

    def clean(self):
        cleaned_data = super().clean()

        # 1. LENGTH CONVERSION & VALIDATION
        length_val = cleaned_data.get('length')
        l_unit = cleaned_data.get('length_unit')
        if length_val not in (None, ''):
            try:
                float_length = float(length_val)
                if l_unit == 'in':
                    float_length = float_length * 2.54
                cleaned_data['length'] = round(float_length, 2)
            except (ValueError, TypeError):
                self.add_error('length', 'Please enter a valid number for length.')
        else:
            cleaned_data['length'] = 0.0

        # 2. WEIGHT CONVERSION & VALIDATION
        weight_val = cleaned_data.get('weight')
        w_unit = cleaned_data.get('weight_unit')
        if weight_val not in (None, ''):
            try:
                float_weight = float(weight_val)
                if w_unit == 'lbs':
                    float_weight = float_weight * 0.45359237
                cleaned_data['weight'] = round(float_weight, 2)
            except (ValueError, TypeError):
                self.add_error('weight', 'Please enter a valid number for weight.')
        else:
            cleaned_data['weight'] = 0.0

        # 3. FISH_SWAMI & NUM_LANDED DEFAULTS
        if cleaned_data.get('fish_swami') is None:
            cleaned_data['fish_swami'] = 0
        if cleaned_data.get('num_landed') is None:
            cleaned_data['num_landed'] = 0

        return cleaned_data
        
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
    notes = forms.CharField(
        widget=CKEditor5Widget(attrs={"class": "django_ckeditor_5"}, config_name="notes"),
        required=False
    )
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
    # notes = forms.CharField ( required = False )             
    notes = forms.CharField(widget=CKEditor5Widget(), required=False)
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
        # fields = '__all__'
        fields = [
            'name', 'other_name', 'district', 'static_tag', 'reg_location', 
            'ats', 'lat', 'long', 'waterbody_id', 'notes', 'gps_url', 'size'
        ]
        widgets = {
            "notes": CKEditor5Widget(
                attrs={"class": "django_ckeditor_5"}, config_name="notes"
            )
        }
        
    name = forms.CharField ( max_length = 20, required = True )  
    other_name = forms.CharField ( max_length = 100, required = False )
    district = forms.ChoiceField( required = True, choices=DISTRICTS, initial='', widget=forms.Select())
    static_tag = forms.CharField( max_length = 100, required = False )      
    reg_location = forms.CharField( max_length = 10, required = False )
    ats = forms.CharField ( max_length = 100, required = False ) 
    lat = forms.DecimalField( max_digits = 25, decimal_places=20, required = True )  
    long = forms.DecimalField( max_digits = 25, decimal_places=20, required = True)  
    waterbody_id = forms.IntegerField( required = False )        
    # notes = forms.CharField (widget=forms.Textarea, required = False ) 
    notes = forms.CharField(widget=CKEditor5Widget(), required=False)
    gps_url = forms.CharField( max_length = 100, required = False )
    size = forms.DecimalField( max_digits = 5, decimal_places=1, required = False ) 
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('name',          css_class='form-group col-md-3 mb-0'),
                Column('other_name',    css_class='form-group col-md-3 mb-0'),
                Column('district',          css_class='form-group col-md-2 mb-0'),
                Column('static_tag',    css_class='form-group col-md-2 mb-0'),
                Column('reg_location',    css_class='form-group col-md-2 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('ats', css_class='form-group col-md-2 mb-0'),
                Column('lat', css_class='form-group col-md-3 mb-0'),
                Column('long', css_class='form-group col-md-3 mb-0'),
                Column('waterbody_id', css_class='form-group col-md-2 mb-0'),
                Column('size', css_class='form-group col-md-2 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('notes', css_class='form-group col-md-12 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('gps_url', css_class='form-group col-md-5 mb-0'),
                css_class='gps_url'
            ),
            Row(
                Column(Submit('submit', 'Submit', css_class='btn btn-primary col-md-5')),
                Column(FormActions(
                    HTML('<a class="btn btn-primary col-md-3" onclick="window.history.back()">Cancel</a>')
                ),  css_class='btn-primary col-md-3'),
                css_class='form-row'
            ),
        )


class New_Regions_Form (forms.ModelForm):

    class Meta:
        model = Region
        fields = ("name", "notes", "address", "city", "prov")
        widgets = {
            "notes": CKEditor5Widget(
                attrs={"class": "django_ckeditor_5"}, config_name="notes"
            )
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["notes"].required = False

        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('name',          css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('notes'),
                css_class='form-row'
            ),
            Row(
                Column('address', css_class='form-group col-md-6 mb-0'),
                Column('city', css_class='form-group col-md-4 mb-0'),
                Column('prov', css_class='form-group col-md-2 mb-0'),
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

class New_Knot_Form (forms.ModelForm):
    class Meta:
        model = Knot
        fields = '__all__'
        widgets = {
            "notes": CKEditor5Widget(
                attrs={"class": "django_ckeditor_5"}, config_name="notes"
            )
        }

    name = forms.CharField ( required = True )                
    notes = forms.CharField(widget=CKEditor5Widget(), required=False)
    image = forms.ImageField (required = False )
    static_tag = forms.CharField ( required = False )
    
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

class New_Locker_Form (forms.ModelForm):
    class Meta:
        model = Locker
        exclude = ['owner', 'pictures', 'videos', 'articles']

    name = forms.CharField ( required = True )
    purchase_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=False
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('category', css_class='form-group col-md-3 mb-0'),
                Column('name', css_class='form-group col-md-3 mb-0'),
                Column('brand', css_class='form-group col-md-3 mb-0'),
                Column('model', css_class='form-group col-md-3 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('purchase_date', css_class='form-group col-md-2 mb-0'),
                Column('purchase_price', css_class='form-group col-md-2 mb-0'),
                Column('characteristics', css_class='form-group col-md-8 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('manufacture_link', css_class='form-group col-md-6 mb-0'),
                Column('retailer_link', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('image', css_class='form-group col-md-8 mb-0'),
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


class New_Video_Form(forms.ModelForm):
    existing_video = forms.ModelChoiceField(
        queryset=Video.objects.all().order_by('name'),
        required=False,
        empty_label="-- Or select existing video from library --",
        label="Select Existing Video"
    )
    name = forms.CharField(max_length=100, required=False, label="Video Title")
    url = forms.URLField(max_length=200, required=False, label="External Video URL (YouTube, Vimeo, etc.)")
    author = forms.CharField(max_length=100, required=False)
    snippet = forms.CharField(max_length=255, required=False)
    notes = forms.CharField(
        widget=CKEditor5Widget(attrs={"class": "django_ckeditor_5"}, config_name="notes"),
        required=False
    )
    tags = forms.CharField(max_length=255, required=False, help_text="Comma-separated tags")

    class Meta:
        model = Video
        fields = ['existing_video', 'name', 'url', 'author', 'snippet', 'notes', 'tags']

    def clean(self):
        cleaned_data = super().clean()
        existing_video = cleaned_data.get('existing_video')
        name = cleaned_data.get('name')
        url = cleaned_data.get('url')

        if not existing_video:
            if not name:
                self.add_error('name', 'Please provide a video title or select an existing video.')
            if not url:
                self.add_error('url', 'Please provide a video URL or select an existing video.')
        return cleaned_data


class New_Picture_Form(forms.ModelForm):
    existing_picture = forms.ModelChoiceField(
        queryset=Picture.objects.all().order_by('name'),
        required=False,
        empty_label="-- Or select existing picture from library --",
        label="Select Existing Picture"
    )
    name = forms.CharField(max_length=100, required=False, label="Picture Title")
    image_url = forms.URLField(
        required=False,
        label="External Picture URL",
        help_text="Provide an image URL to download into /public/downloads/picture/"
    )
    image = forms.ImageField(required=False, label="Or upload image file")
    snippet = forms.CharField(max_length=255, required=False)
    notes = forms.CharField(
        widget=CKEditor5Widget(attrs={"class": "django_ckeditor_5"}, config_name="notes"),
        required=False
    )
    tags = forms.CharField(max_length=255, required=False, help_text="Comma-separated tags")

    class Meta:
        model = Picture
        fields = ['existing_picture', 'name', 'image_url', 'image', 'snippet', 'notes', 'tags']

    def clean(self):
        cleaned_data = super().clean()
        existing_picture = cleaned_data.get('existing_picture')
        name = cleaned_data.get('name')
        image_url = cleaned_data.get('image_url')
        image = cleaned_data.get('image')

        if not existing_picture:
            if not name:
                self.add_error('name', 'Please provide a picture title or select an existing picture.')
            if not image_url and not image:
                self.add_error('image_url', 'Please provide either an external image URL or upload an image file.')
        return cleaned_data


class New_Article_Form(forms.ModelForm):
    existing_article = forms.ModelChoiceField(
        queryset=Article.objects.all().order_by('name'),
        required=False,
        empty_label="-- Or select existing article from library --",
        label="Select Existing Article"
    )
    name = forms.CharField(max_length=100, required=False, label="Article Title")
    article_url = forms.URLField(
        required=False,
        label="External Article URL",
        help_text="Provide an article/document link to download into /public/downloads/article/"
    )
    file = forms.FileField(required=False, label="Or upload article file (PDF, Doc, etc.)")
    author = forms.CharField(max_length=100, required=False)
    snippet = forms.CharField(max_length=255, required=False)
    notes = forms.CharField(
        widget=CKEditor5Widget(attrs={"class": "django_ckeditor_5"}, config_name="notes"),
        required=False
    )
    tags = forms.CharField(max_length=255, required=False, help_text="Comma-separated tags")

    class Meta:
        model = Article
        fields = ['existing_article', 'name', 'article_url', 'file', 'author', 'snippet', 'notes', 'tags']

    def clean(self):
        cleaned_data = super().clean()
        existing_article = cleaned_data.get('existing_article')
        name = cleaned_data.get('name')
        article_url = cleaned_data.get('article_url')
        file = cleaned_data.get('file')
        notes = cleaned_data.get('notes')

        if not existing_article:
            if not name:
                self.add_error('name', 'Please provide an article title or select an existing article.')
            if not article_url and not file and not notes:
                self.add_error('article_url', 'Please provide an external article URL, upload a file, or write notes.')
        return cleaned_data


class New_Setup_Form(forms.ModelForm):
    class Meta:
        model = Setup
        fields = [
            'name', 'rod', 'reel', 'fly_line', 'line_to_leader_knot',
            'leader', 'leader_length', 'strike_indicator',
            'indicator_distance_from_fly_end', 'is_private', 'notes'
        ]
        widgets = {
            'notes': CKEditor5Widget(attrs={"class": "django_ckeditor_5"}, config_name="notes"),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Euro Nymphing Rig, 9ft 5wt Indicator Setup, Streamer Sinking Rig'}),
            'rod': forms.Select(attrs={'class': 'form-select'}),
            'reel': forms.Select(attrs={'class': 'form-select'}),
            'fly_line': forms.Select(attrs={'class': 'form-select'}),
            'line_to_leader_knot': forms.Select(attrs={'class': 'form-select'}),
            'leader': forms.Select(attrs={'class': 'form-select'}),
            'leader_length': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 9ft, 7.5ft, 12ft'}),
            'strike_indicator': forms.Select(attrs={'class': 'form-select'}),
            'indicator_distance_from_fly_end': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 18in, 3ft, 4.5ft'}),
            'is_private': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            if user.is_superuser:
                self.fields['rod'].queryset = Locker.objects.filter(category__name='Rod').order_by('name')
                self.fields['reel'].queryset = Locker.objects.filter(category__name='Reel').order_by('name')
                self.fields['fly_line'].queryset = Locker.objects.filter(category__name='Fly line').order_by('name')
                self.fields['leader'].queryset = Locker.objects.filter(category__name='Leader').order_by('name')
                self.fields['strike_indicator'].queryset = Locker.objects.filter(category__name='Hardware').order_by('name')
            else:
                self.fields['rod'].queryset = Locker.objects.filter(owner=user, category__name='Rod').order_by('name')
                self.fields['reel'].queryset = Locker.objects.filter(owner=user, category__name='Reel').order_by('name')
                self.fields['fly_line'].queryset = Locker.objects.filter(owner=user, category__name='Fly line').order_by('name')
                self.fields['leader'].queryset = Locker.objects.filter(owner=user, category__name='Leader').order_by('name')
                self.fields['strike_indicator'].queryset = Locker.objects.filter(owner=user, category__name='Hardware').order_by('name')
        else:
            self.fields['rod'].queryset = Locker.objects.filter(category__name='Rod').order_by('name')
            self.fields['reel'].queryset = Locker.objects.filter(category__name='Reel').order_by('name')
            self.fields['fly_line'].queryset = Locker.objects.filter(category__name='Fly line').order_by('name')
            self.fields['leader'].queryset = Locker.objects.filter(category__name='Leader').order_by('name')
            self.fields['strike_indicator'].queryset = Locker.objects.filter(category__name='Hardware').order_by('name')

        self.fields['line_to_leader_knot'].queryset = Knot.objects.all().order_by('name')
        self.fields['rod'].empty_label = "-- Select Rod --"
        self.fields['reel'].empty_label = "-- Select Reel --"
        self.fields['fly_line'].empty_label = "-- Select Fly Line --"
        self.fields['line_to_leader_knot'].empty_label = "-- Select Connection Knot --"
        self.fields['leader'].empty_label = "-- Select Leader --"
        self.fields['strike_indicator'].empty_label = "-- Select Indicator (Optional) --"


class SetupSectionForm(forms.ModelForm):
    class Meta:
        model = SetupSection
        fields = ['order', 'configuration', 'connection_knot', 'hardware', 'tippet_material', 'length', 'notes']
        widgets = {
            'order': forms.NumberInput(attrs={'class': 'form-control form-control-sm section-order-input', 'style': 'width: 70px;', 'min': 1}),
            'configuration': forms.Select(attrs={'class': 'form-select form-select-sm section-config-select'}),
            'connection_knot': forms.Select(attrs={'class': 'form-select form-select-sm knot-select'}),
            'hardware': forms.Select(attrs={'class': 'form-select form-select-sm hardware-select'}),
            'tippet_material': forms.Select(attrs={'class': 'form-select form-select-sm tippet-select'}),
            'length': forms.TextInput(attrs={'class': 'form-control form-control-sm', 'placeholder': 'e.g., 4ft, 18in, 6in'}),
            'notes': forms.TextInput(attrs={'class': 'form-control form-control-sm', 'placeholder': 'e.g., Point fly, Top dropper, Trailing nymph'}),
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            if user.is_superuser:
                self.fields['hardware'].queryset = Locker.objects.filter(category__name='Hardware').order_by('name')
                self.fields['tippet_material'].queryset = Locker.objects.filter(category__name__in=['Tippet', 'Leader']).order_by('name')
            else:
                self.fields['hardware'].queryset = Locker.objects.filter(owner=user, category__name='Hardware').order_by('name')
                self.fields['tippet_material'].queryset = Locker.objects.filter(owner=user, category__name__in=['Tippet', 'Leader']).order_by('name')
        else:
            self.fields['hardware'].queryset = Locker.objects.filter(category__name='Hardware').order_by('name')
            self.fields['tippet_material'].queryset = Locker.objects.filter(category__name__in=['Tippet', 'Leader']).order_by('name')

        self.fields['connection_knot'].queryset = Knot.objects.all().order_by('name')
        self.fields['connection_knot'].empty_label = "-- Knot --"
        self.fields['hardware'].empty_label = "-- Hardware --"
        self.fields['tippet_material'].empty_label = "-- Tippet / Material --"


SetupSectionFormSet = forms.inlineformset_factory(
    Setup,
    SetupSection,
    form=SetupSectionForm,
    extra=1,
    can_delete=True
)


class New_Strategy_Form(forms.ModelForm):
    class Meta:
        model = Strategy
        fields = ['name', 'setup', 'is_private', 'notes']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Deep Chironomid Wind Drift, Streamer Strip along Drop-offs'}),
            'setup': forms.Select(attrs={'class': 'form-select'}),
            'is_private': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'notes': CKEditor5Widget(attrs={"class": "django_ckeditor_5"}, config_name="notes"),
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            if user.is_superuser:
                self.fields['setup'].queryset = Setup.objects.all().order_by('name')
            else:
                self.fields['setup'].queryset = Setup.objects.filter(models.Q(is_private=False) | models.Q(owner=user)).order_by('name')
        else:
            self.fields['setup'].queryset = Setup.objects.filter(is_private=False).order_by('name')
        self.fields['setup'].empty_label = "-- Select Line Setup / Rig (Optional) --"


class New_Post_Form(forms.ModelForm):
    title = forms.CharField(max_length=100, required=True, label="Post Title")
    content = forms.CharField(
        widget=CKEditor5Widget(attrs={"class": "django_ckeditor_5"}, config_name="notes"),
        required=False,
        label="Post Content"
    )
    tags = forms.CharField(max_length=255, required=False, help_text="Comma-separated tags (e.g., fishing, trout, dryfly)")

    class Meta:
        model = Post
        fields = ['title', 'content', 'tags']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            if hasattr(self.instance, 'tags'):
                self.initial['tags'] = ", ".join(t.name for t in self.instance.tags.all())
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('title', css_class='form-group col-md-12 mb-3'),
                css_class='form-row'
            ),
            Row(
                Column('content', css_class='form-group col-md-12 mb-3'),
                css_class='form-row'
            ),
            Row(
                Column('tags', css_class='form-group col-md-12 mb-3'),
                css_class='form-row'
            ),
            Row(
                Column(Submit('submit', 'Post', css_class='btn btn-primary me-2'), css_class='col-auto'),
                Column(FormActions(
                    HTML('<a class="btn btn-secondary" onclick="window.history.back()">Cancel</a>')
                ), css_class='col-auto'),
                css_class='form-row mt-3'
            ),
        )

    def save(self, commit=True):
        instance = super().save(commit=commit)
        tag_str = self.cleaned_data.get('tags', '')
        if commit:
            if tag_str:
                tag_names = [t.strip() for t in tag_str.split(',') if t.strip()]
                instance.tags.set(tag_names)
            else:
                instance.tags.clear()
        return instance



