from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit
import pycountry

# TODO: fix the hidden feilds for the platforms
class Image_Gathering(forms.Form): 
    """
    Adding to DataBase Form
    """
    CHOICES_PLATFORM = [('Reddit',' Reddit'),('Facebook',' Facebook'),('Twitter',' Twitter'),('4Chan',' 4Chan')]
    CHOICES_COUNTRIES = [(i.alpha_2, i.name) for i in list(pycountry.countries)]

    # input_ = forms.CharField(label = 'Input',max_length=100, required=True , widget=forms.TextInput(attrs={'placeholder': '#Trump'}))
    choice_platform = forms.MultipleChoiceField(
        label='Please choose platform:',
        required=True,
        widget=forms.RadioSelect,
        choices= CHOICES_PLATFORM,
    )
    startDate = forms.CharField(label = 'Start Date',max_length=10, required=True, widget=forms.TextInput(attrs={'placeholder': 'MM/DD/YYYY'}))
    endDate = forms.CharField(label = 'End Date',max_length=10, required=True, widget=forms.TextInput(attrs={'placeholder' : 'MM/DD/YYYY'}))
    
    # Reddit fields
    subReddit = forms.CharField(label = 'Reddit Subreddit',max_length=500, required=False, widget=forms.TextInput(attrs={'size':'80'}))

    # # 4Chan fields
    board = forms.CharField(label = '4Chan Board',max_length=500, required=False, widget=forms.TextInput(attrs={'size':'80'}))
    Country = forms.ChoiceField(
        label='4Chan Country',
        required=False,
        choices=CHOICES_COUNTRIES,
        initial='CA'
    )

    # # FaceBook fields
    access_token = forms.CharField(label = 'Facebook Dashboard Access Token',max_length=500, required=False, widget=forms.TextInput(attrs={'size':'80'}))

    # # Twitter Fields
    # hashTag = forms.CharField(label = 'Input',max_length=500, required=True, widget=forms.HiddenInput())


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Fieldset(
                '',
                'startDate',
                'endDate',
                'choice_platform',
                'subReddit',
                'access_token',
                'board',
                'Country',
            ),
            ButtonHolder(
                Submit('Submit', 'Scrape Data', css_class='button white')
            )
        )

class Image_Analysis(forms.Form):
    """
    Query from DataBase Form
    """
    
    Task_ids = forms.CharField(label = 'Task Ids',max_length=500, required=True, widget=forms.TextInput(attrs={'size':'80'}))
    Identical = forms.BooleanField(label = 'Identical', required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(

            Fieldset(
                '',
                'Task_ids',
                'Identical',
                # 'choice_filetype',
            ),
            ButtonHolder(
                Submit('Submit','Submit',css_class='button white'),
            ),
            
        )


class Image_Visualization(forms.Form): 
     
     def __init__(self, *args, **kwargs):
        pass