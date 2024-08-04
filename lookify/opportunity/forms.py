from django import forms
from .models import Opportunity, Experience, Application


class OpportunityForm(forms.ModelForm):
    class Meta:
        model = Opportunity
        fields = ['title', 'description', 'location', 'category', 'background', 'tags','application_type', 'responsibilities', 'grade',
                  'length']


class FilterForm(forms.Form):
    search = forms.CharField(required=False)


class ApplicationForm(forms.Form):
    application_text = forms.CharField(label='', widget=forms.Textarea)
    application_contact = forms.CharField(label='', widget=forms.Textarea(attrs={'style': 'max-height: 2.6em; overflow: hidden;'}))


class AppForm(forms.ModelForm):
    experience1 = forms.TextInput()
    experience2 = forms.TextInput()

    class Meta:
        model = Experience
        fields = ['experience1', 'experience2']


