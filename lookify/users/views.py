import os
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.template.defaultfilters import slugify
from django.urls import reverse, reverse_lazy
from django.contrib.auth import get_user_model, login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.views import View
from django.views.generic.edit import UpdateView, FormView
from django.db.models import Count

from .forms import (
    RegisterForm,
    LoginForm,
    UpdateUserForm,
    UpdateProfileForm,
    UpdateOrgProfileForm,
    ExperienceFormSet,
    EducationFormSet,
    ContactForm,
    ExpForm,
    EduForm
)
from .models import Profile, Education, Experience, Exp, Edu, ContactRequest, OrganizationProfile
from opportunity.models import Opportunity, Application

User = get_user_model()

def home(request):
    numLooks =  Opportunity.objects.count()
    featured_looks = Opportunity.objects.order_by("-visits")[:6]
    orgs = OrganizationProfile.objects.filter(
    user__user_type='organization'
).annotate(
    opportunity_count=Count('user__opportunity')  # Annotate based on related opportunities count
).order_by('-opportunity_count')[:6]
    context = {
        "num": numLooks,
        "featured": featured_looks,
        'orgs': orgs
    }
    return render(request, 'users/home.html', context)



class RegisterView(View):
    form_class = RegisterForm
    initial = {'key': 'value'}
    template_name = 'users/register.html'
    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f" {error}")
        return super().form_invalid(form)

    def dispatch(self, request, *args, **kwargs):
        # will redirect to the home page if a user tries to access the register page while logged in
        if request.user.is_authenticated:
            return redirect(to='/')

        # else process dispatch as it otherwise normally would
        return super(RegisterView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            user = form.save()

            username = form.cleaned_data.get('username')

            if user.user_type == 'individual':
                Profile.objects.create(user=user)

            elif user.user_type == 'organization':
                OrganizationProfile.objects.create(user=user)

            user = authenticate(username=form.cleaned_data.get('username'), password=form.cleaned_data.get('password1'))
            if user is not None:
                login(request, user)

                messages.success(request, f'Account created for {username}, please update your profile')

                if user.user_type == 'individual':
                    return redirect("update_profile")

                elif user.user_type == 'organization':
                    return redirect("update-org-profile")

        else:
            print(form.errors)
        return render(request, self.template_name, {'form': form})


# Class based view that extends from the built in login view to add a remember me functionality
class CustomLoginView(LoginView):
    form_class = LoginForm

    def form_invalid(self, form):
        # Add form errors to messages
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f" {error}")
        return super().form_invalid(form)

    def form_valid(self, form):
        remember_me = form.cleaned_data.get('remember_me')

        if not remember_me:
            # set session expiry to 0 seconds. So it will automatically close the session after the browser is closed.
            self.request.session.set_expiry(0)

            # Set session as modified to force data updates/cookie to be saved.
            self.request.session.modified = True

        # else browser session will be as long as the session cookie time "SESSION_COOKIE_AGE" defined in settings.py
        messages.success(self.request, "Logged in successfully")
        return super(CustomLoginView, self).form_valid(form)

class ModalSignInView(LoginView):
    template = "users/modal_signin.html"
    form_class = LoginForm

    def form_valid(self, form):
        self.user = form.get_user()
        login(self.request, self.user)
        remember_me = form.cleaned_data.get('remember_me')

        if not remember_me:
            # set session expiry to 0 seconds. So it will automatically close the session after the browser is closed.
            self.request.session.set_expiry(0)

            # Set session as modified to force data updates/cookie to be saved.
            self.request.session.modified = True

        # else browser session will be as long as the session cookie time "SESSION_COOKIE_AGE" defined in settings.py
        return super(ModalSignInView, self).form_valid(form)

@login_required
def profile_view(request, username):
    # Get the user object for the user whose profile is being viewed
    viewed_user = get_object_or_404(User, username=username)


    # Fetch other relevant data for the profile view
    if viewed_user.user_type == 'individual':
        user_profile = Profile.objects.get(user=viewed_user)
        # Filter experiences based on the user whose profile is being viewed
        exps = Exp.objects.filter(user=viewed_user)
        edus = Edu.objects.filter(user=viewed_user)
        context = {
        'user': viewed_user,
        'user_profile': user_profile,
        'exps': exps,
        'edus': edus,
        }
        return render(request, 'users/indv_profile_view.html', context)
    elif viewed_user.user_type == 'organization':
        user_profile = OrganizationProfile.objects.get(user=viewed_user)
        opps = Opportunity.objects.filter(user=viewed_user)
        context = {
        'org': user_profile,
        'posts': opps
        }
        return render(request, 'users/org_profile_view.html', context)

@login_required
def submitContact(request, receiver):

    if request.method == 'POST':
        receiver = User.objects.get(username=receiver)
        message = ContactForm(request.POST, sender=request.user, receiver=receiver)

        if message.is_valid():
            message.save()
            messages.success(request, "Your message has been sent successfully")
            return redirect(to="profile-view", username=receiver)


@login_required
def user_search(request):
    key = request.GET.get('user_search')
    return render(request, 'users/user_searchresults.html')



@login_required
def expo(request):
    if request.method == 'POST':
        forms = ExpForm(request.POST, request.FILES)

        if forms.is_valid():
            eform = forms.save(commit=False)
            eform.user = request.user
            eform.slug = slugify(eform.title)

            # Ensure slug uniqueness
            slug_suffix = 1
            while True:
                try:
                    eform.save()
                    break
                except IntegrityError:
                    # If slug already exists, append a suffix and try again
                    eform.slug = f"{slugify(eform.title)}-{slug_suffix}"
                    slug_suffix += 1

            forms.save_m2m()
            messages.success(request, 'Your experience was created.')
            # Redirect to the profile view of the current user
            return redirect(to="exp-manager")
    else:
        forms = ExpForm()
    return render(request, 'dashboard/dashboard-new-exp.html', {'forms': forms})

@login_required
def exp_manager(request):
    exps = Exp.objects.filter(user=request.user)

    page_number = request.GET.get('page', 1)

    page = Paginator(exps, 10)
    page_obj = page.get_page(page_number)
    context = {
        'posts': exps,
        'page_number': page_obj
    }
    return render(request, 'dashboard/dashboard-edit-profile.html', context)

@login_required
def delete_exp(request, pk):
    exp = get_object_or_404(Exp, pk=pk)

    # Check if the logged-in user is the owner of the experience
    if exp.user == request.user:
        exp.delete()
        messages.success(request, 'Your experience was deleted successfully.')
        return redirect('exp-manager')
    else:
        return HttpResponseForbidden("You don't have permission to delete this experience.")


@login_required
def edu(request):
    if request.method == 'POST':
        forms = EduForm(request.POST, request.FILES)

        if forms.is_valid():
            eform = forms.save(commit=False)
            eform.user = request.user
            eform.slug = slugify(eform.title)

            # Ensure slug uniqueness
            slug_suffix = 1
            while True:
                try:
                    eform.save()
                    break
                except IntegrityError:
                    # If slug already exists, append a suffix and try again
                    eform.slug = f"{slugify(eform.title)}-{slug_suffix}"
                    slug_suffix += 1

            forms.save_m2m()
            return redirect(to="edu-manager")
    else:
        forms = EduForm()
    return render(request, 'dashboard/dashboard-manage-edu.html', {'forms': forms})


@login_required
def edu_manager(request):
    edus = Edu.objects.filter(user=request.user)

    page_number = request.GET.get('page', 1)

    page = Paginator(edus, 10)
    page_obj = page.get_page(page_number)
    context = {
        'posts': edus,
        'page_number': page_obj
    }
    return render(request, 'dashboard/dashboard-manage-edu.html', context)

@login_required
def delete_edu(request, pk):
    eduu = get_object_or_404(Edu, pk=pk)

    # Check if the logged-in user is the owner of the experience
    if eduu.user == request.user:
        eduu.delete()
        messages.success(request, 'Your experience was deleted successfully.')
        return redirect('dashboard/edu-manager')
    else:
        return HttpResponseForbidden("You don't have permission to delete this experience.")


class OrgProfileUpdate(FormView):
    form_class = UpdateOrgProfileForm
    template_name = "dashboard/org-dashboard-edit-profile.html"

    def get_success_url(self):
        # Get the username of the updated profile
        username = self.request.user.username
        # Construct the success URL using the username
        return reverse('profile-view', kwargs={'username': username})

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        # Pass the instance of OrganizationProfile associated with the current user to the form
        try:
            organization_profile = OrganizationProfile.objects.get(user=self.request.user)
        except OrganizationProfile.DoesNotExist:
            organization_profile = None
        kwargs['instance'] = organization_profile
        return kwargs

    def form_valid(self, form):
        # Set the user for the organization profile before saving
        profile = form.save(commit=False)
        profile.user = self.request.user
        profile = form.save(commit=False)
        if 'avatar' in self.request.FILES:
            profile.avatar = self.request.FILES['avatar']
        if 'background' in self.request.FILES:
            profile.background = self.request.FILES['background']
        profile.save()
        return super().form_valid(form)

        return super().form_valid(form)


class ProfileInline(FormView):
    form_class = UpdateProfileForm
    template_name = "dashboard/dashboard-edit-profile.html"

    def form_valid(self, form):
        profile = form.save(commit=False)
        if 'avatar' in self.request.FILES:
            profile.avatar = self.request.FILES['avatar']
        if 'background' in self.request.FILES:
            profile.background = self.request.FILES['background']
        profile.save()

        named_formsets = self.get_named_formsets()

        # Check if the main form and all formsets are valid
        if form.is_valid() and all((x.is_valid() for x in named_formsets.values())):
            # Save the main form
            form.save_m2m()

            # Save each formset
            for name, formset in named_formsets.items():
                formset_save_func = getattr(self, 'formset_{0}_valid'.format(name), None)
                if formset_save_func is not None:
                    formset_save_func(formset)
                else:
                    formset.save()

            # Redirect to the appropriate URL after successful form submission
            return redirect('user-dash')
        else:
            # If the form or any formset is not valid, render the form again with errors
            return self.render_to_response(self.get_context_data(form=form))

    def formset_experience_valid(self, formset):
        """
        Hook for custom formset saving.. useful if you have multiple formsets
        """
        experiences = formset.save(commit=False)  # self.save_formset(formset, contact)
        # add this, if you have can_delete=True parameter set in inlineformset_factory func
        for obj in formset.deleted_objects:
            obj.delete()
        for experience in experiences:
            experience.profile = self.object
            experience.save()

    def formset_education_valid(self, formset):
        """
        Hook for custom formset saving.. useful if you have multiple formsets
        """
        educations = formset.save(commit=False)  # self.save_formset(formset, contact)
        # add this, if you have can_delete=True parameter set in inlineformset_factory func
        for obj in formset.deleted_objects:
            obj.delete()
        for education in educations:
            education.profile = self.object
            education.save()

class ProfileUpdate(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = UpdateProfileForm
    template_name = "dashboard/dashboard-edit-profile.html"

    def get_success_url(self):
        # Get the username of the updated profile
        username = self.object.user.username
        # Construct the success URL using the username
        return reverse('profile-view', kwargs={'username': username})

    def get_context_data(self, **kwargs):
        ctx = super(ProfileUpdate, self).get_context_data(**kwargs)
        ctx['named_formsets'] = self.get_named_formsets()
        return ctx

    def get_named_formsets(self):
        return {
            'experiences': ExperienceFormSet(self.request.POST or None, instance=self.object, prefix='experiences'),
            'educations': EducationFormSet(self.request.POST or None, instance=self.object, prefix='educations'),
        }

    def get_object(self, queryset=None):
        # Override get_object to fetch the profile of the logged-in user
        return self.request.user.profile

    def form_valid(self, form):
        response = super().form_valid(form)

        avatar_file = self.request.FILES.get('avatar')
        background_file = self.request.FILES.get('background')

        if avatar_file:
            avatar_path = os.path.join('profile_images', avatar_file.name)
            default_storage.save(avatar_path, avatar_file)
            self.object.avatar = avatar_path

        if background_file:
            background_path = os.path.join('profile_background', background_file.name)
            default_storage.save(background_path, background_file)
            self.object.background = background_path

        self.object.save()

        skills_data = form.cleaned_data['skills']
        if isinstance(skills_data, str):
            # Split the string into a list of tags
            new_skills = set(skills_data.split(','))
        else:
            new_skills = set()

        # Clear existing skills and add new ones

        for skill in new_skills:
            self.object.skills.add(skill.strip())


        self.object = form.save()
        for formset in self.get_named_formsets().values():
            if formset.is_valid():
                formset.save()
            else:
                # Handle formset errors here if needed
                pass
        return redirect("profile-view", self.object.user.username)


    def form_invalid(self, form):
        messages.error(self.request, "Profile update failed. Please check the form.")
        return super().form_invalid(form)

# Handle form submission
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            messages.success(request, "Profile updated successfully")
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

def delete_education(request, pk):
    try:
        education = Education.objects.get(id=pk)
    except Education.DoesNotExist:
        messages.success(
            request, 'Object Does not exit'
            )
        return redirect('update_profile')

    education.delete()
    messages.success(
            request, 'Education deleted successfully'
            )
    return redirect('update_profile')

def delete_experience(request, pk):
    try:
        experience = Experience.objects.get(id=pk)
    except Experience.DoesNotExist:
        messages.success(
            request, 'Object Does not exit'
            )
        return redirect('update_profile')

    experience.delete()
    messages.success(
            request, 'Variant deleted successfully'
            )
    return redirect('update_profile')

from django.contrib.auth import get_user_model
from django.http import HttpResponse
#checks if username exsits, for register page
def check_username(request):

    username = request.GET.get('username')
    if username =="":
        return HttpResponse("")
    if get_user_model().objects.filter(username=username).exists():
        return HttpResponse('<div style="color: red">This username is already exists</div>')

    else:
        return HttpResponse('<div style="color: green">This username is available</div>')
def check_email(request):

    email = request.GET.get('email')
    if email =="":
        return HttpResponse("")
    if get_user_model().objects.filter(email=email).exists():
        return HttpResponse('<div style="color: red">This email is already exists</div>')
    else:
        return HttpResponse('<div style="color: green">This email is available</div>')