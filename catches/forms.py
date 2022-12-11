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

class New_Temp_Form (forms.ModelForm): 
    class Meta:
        model = Temp
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

class New_Lake_Form (forms.ModelForm):
    
    class Meta:
        model = Lake
        fields = '__all__'
    name = forms.CharField ( max_length = 100, required = True )  
    other_name = forms.CharField ( max_length = 100, required = False )      
    notes = forms.CharField ( max_length = 100, required = False )      
    ats = forms.CharField ( max_length = 100, required = False ) 
    lat = forms.DecimalField( max_digits = 20, decimal_places=10, required = False )  
    long = forms.DecimalField( max_digits = 20, decimal_places=10, required = False )  
    district = forms.CharField( max_length = 100, required = False )
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
                Column('name', css_class='form-group col-md-4 mb-0'),
                Column('other_name', css_class='form-group col-md-4 mb-0'),
                Column('favourite', css_class='form-group col-md-2 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('district', css_class='form-group col-md-3 mb-0'),
                Column('region', css_class='form-group col-md-3 mb-0 offset-md-2'),
                css_class='form-row'
            ),
            Row(
                Column('ats', css_class='form-group col-md-2 mb-0'),
                Column('lat', css_class='form-group col-md-2 mb-0'),
                Column('long', css_class='form-group col-md-2 mb-0'),
                Column('waterbody_id', css_class='form-group col-md-2 mb-0'),
                css_class='form-row'
            ),
            Row('notes'),
            Submit('submit', 'Save')
        )
        
class New_Log_Form (forms.ModelForm):
    
    class Meta:
        model = Log
        fields = '__all__'     

    catch_date = forms.DateField(
        widget=forms.widgets.DateInput(format="%m/%d/%Y") )
    notes = forms.CharField ( required = False )  
    image = forms.ImageField (required = False )

    lake = forms.ModelChoiceField(
        queryset=Lake.objects.all(),
        required = False )

    watertemp = forms.ModelChoiceField(
        queryset=Temp.objects.all(),
        required = False )

    fly = forms.ModelChoiceField(
        queryset=Fly.objects.all(),
        required = False )
    fly_size = forms.CharField ( required = False ) 
    fly_colour = forms.CharField ( required = False ) 

    fish = forms.ModelChoiceField(
        queryset=Fish.objects.all(),
        required = False )
    length = forms.CharField ( required = False ) 
    weight = forms.CharField ( required = False ) 
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('lake', css_class='form-group col-md-4 mb-0'),
                Column('watertemp', css_class='form-group col-md-4 mb-0'),
                Column('catch_date', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('fish', css_class='form-group col-md-4 mb-0'),
                Column('length', css_class='form-group col-md-4 mb-0'),
                Column('weight', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('fly', css_class='form-group col-md-4 mb-0'),
                Column('fly_size', css_class='form-group col-md-4 mb-0'),
                Column('fly_color', css_class='form-group col-md-4 mb-0'),
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
        
class New_Bug_site_Form (forms.ModelForm):
    
    class Meta:
        model = Bug_site
        fields = '__all__'     
    name = forms.CharField ( required = False )
    notes = forms.CharField ( required = False )  

    lake = forms.ModelChoiceField(
        queryset=Lake.objects.all(),
        required = False )

    watertemp = forms.ModelChoiceField(
        queryset=Temp.objects.all(),
        required = False )

    bug = forms.ModelChoiceField(
        queryset=Bug.objects.all(),
        required = False )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='form-group col-md-4 mb-0'),
                Column('', css_class='form-group col-md-8 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('bug', css_class='form-group col-md-4 mb-0'),
                Column('lake', css_class='form-group col-md-4 mb-0'),
                Column('watertemp', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('notes', css_class='form-group col-md-12 mb-0'),
                css_class='form-row'
            ),
            Submit('submit', 'Save')
        )

class New_Fly_Form (forms.ModelForm):
    
    class Meta:
        model = Fly
        fields = '__all__'
    name = forms.CharField ( required = True ) 
    description = forms.CharField ( required = False ) 
    size_range = forms.CharField ( required = False )
    author = forms.CharField ( required = False )
    youtube = forms.CharField ( required = False )
    image = forms.ImageField (required = False )

    bug = forms.ModelChoiceField(
        queryset=Bug.objects.all(),
        required = False )   

    fly_type = forms.ModelChoiceField(
        queryset=Fly_type.objects.all(),
        required = False )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='form-group col-md-4 mb-0'),
                Column('fly_type', css_class='form-group col-md-4 mb-0'),
                Column('bug', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('size_range', css_class='form-group col-md-6 mb-0'),
                Column('image', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            'description',
            Row(
                Column('author', css_class='form-group col-md-4 mb-0'),
                Column('youtube', css_class='form-group col-md-8 mb-0'),
                css_class='form-row'
            ),
            Submit('submit', 'Save')
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
                Column('length', css_class='form-group col-md-4 mb-0'),
                Column('number', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Submit('submit', 'Save')
        )
        


