from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from taggit.forms import TagField
from .models import Profile, OrganizationProfile, Experience, Education,  ContactRequest, Exp, Edu
from django.forms import inlineformset_factory
from taggit.forms import TagWidget


User = get_user_model()
class RegisterForm(UserCreationForm):
    # fields we want to include and customize in our form
    user_type = forms.ChoiceField(choices=User.USER_TYPE_CHOICES, widget=forms.RadioSelect, required=True)

    first_name = forms.CharField(max_length=100,
                                 required=True,
                                 widget=forms.TextInput(attrs={'placeholder': 'First Name',
                                                               'class': 'form-control',
                                                               }))
    last_name = forms.CharField(max_length=100,
                                required=True,
                                widget=forms.TextInput(attrs={'placeholder': 'Last Name',
                                                              'class': 'form-control',
                                                              }))
    username = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput(attrs={'placeholder': 'Username',
                                                             'class': 'form-control',
                                                             }))
    email = forms.EmailField(required=True,
                             widget=forms.TextInput(attrs={'placeholder': 'Email',
                                                           'class': 'form-control',
                                                           }))
    password1 = forms.CharField(max_length=50,
                                required=True,
                                widget=forms.PasswordInput(attrs={'placeholder': 'Password',
                                                                  'class': 'form-control',
                                                                  'data-toggle': 'password',
                                                                  'id': 'password',
                                                                  }))
    password2 = forms.CharField(max_length=50,
                                required=True,
                                widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password',
                                                                  'class': 'form-control',
                                                                  'data-toggle': 'password',
                                                                  'id': 'password',
                                                                  }))


    class Meta:
        model = User
        fields = ['user_type', 'first_name', 'last_name', 'username', 'email', 'password1', 'password2']
    def save(self, commit=True):
        user = super().save(commit=False)
        # Exclude saving user_type to User model
        return user if not commit else super().save()

class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput(attrs={'placeholder': 'Username',
                                                             'class': 'form-control',
                                                             }))
    password = forms.CharField(max_length=50,
                               required=True,
                               widget=forms.PasswordInput(attrs={'placeholder': 'Password',
                                                                 'class': 'form-control',
                                                                 'data-toggle': 'password',
                                                                 'id': 'password',
                                                                 'name': 'password',
                                                                 }))
    remember_me = forms.BooleanField(required=False)

    class Meta:
        model = User
        fields = ['username', 'password', 'remember_me']


class UpdateUserForm(forms.ModelForm):
    username = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=True,
                             widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email']
#for individuals users
class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['background', 'avatar', 'phone', 'email', 'bio', 'grade', 'school', 'skills', 'has_applied']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            initial_skills = ', '.join([tag.name for tag in self.instance.skills.all()])
            self.fields['skills'].initial = initial_skills
        for field in self.fields.values():
            field.required = False
#for organization users


class UpdateOrgProfileForm(forms.ModelForm):
    class Meta:
        model = OrganizationProfile
        fields = ['organization_name', 'background', 'avatar', 'phone', 'email', 'about', 'website','full_address', 'domain', 'keywords']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            initial_keywords = ', '.join([tag.name for tag in self.instance.keywords.all()])
            self.fields['keywords'].initial = initial_keywords
        for field in self.fields.values():
            field.required = False

class ExperienceForm(forms.ModelForm):
    class Meta:
        model = Experience
        exclude = ['profile']

class EducationForm(forms.ModelForm):
    class Meta:
        model = Education
        exclude = ['profile']

ExperienceFormSet = inlineformset_factory(Profile, Experience,form=ExperienceForm,
                    extra=1, can_delete=True, can_delete_extra=True)
EducationFormSet = inlineformset_factory(Profile, Education,form=EducationForm,
                    extra=1, can_delete=True, can_delete_extra=True)


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactRequest
        fields = ['email', 'message']

    def __init__(self, *args, **kwargs):
        self.sender = kwargs.pop('sender', None)
        self.receiver = kwargs.pop('receiver', None)
        super(ContactForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super(ContactForm, self).save(commit=False)
        instance.sender = self.sender
        instance.receiver = self.receiver
        if commit:
            instance.save()
        return instance

class ExpForm(forms.ModelForm):
    class Meta:
        model = Exp
        fields = ['title', 'description', 'location','length']

class EduForm(forms.ModelForm):
    class Meta:
        model = Edu
        fields = ['title', 'description', 'location','length']