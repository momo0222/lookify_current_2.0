from django import forms
from django_select2 import forms as s2forms
from users.models import School

class SchoolWidget(s2forms.ModelSelect2Widget):
    search_fields = [
        "name__icontains",
        "zip_code__icontains",
    ]
   
    def get_url(self):
        return '/ajax/school-search/'
class OrgSearchForm(forms.Form):
    search = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'placeholder': 'Organization Name or Keyword',
        'class': 'form-control'
    }))
    school = forms.ModelChoiceField(
        queryset=School.objects.all(),
        widget=SchoolWidget,
        label="Search School by Name or Zip Code"
    )
