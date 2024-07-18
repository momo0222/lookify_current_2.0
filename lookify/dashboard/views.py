from django.shortcuts import render, redirect
from opportunity.models import Opportunity, Application
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from users.models import ContactRequest, Exp, Edu
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import HttpResponseForbidden  # Import your Exp model here
from django.contrib.auth import get_user_model
from users.forms import ExpForm, EduForm
from notifications.models import Notifications
# Create your views here.

User = get_user_model()
@login_required
def dash(request):
    user = request.user
    posts_data = Opportunity.objects.filter(user = user)
    print(user.user_type)
    context = {
        "user": user,
        "posts" : posts_data,
    }
    if user.user_type == 'individual':
        return render(request, 'dashboard/indv-dashboard.html', context)
    else:
        return render(request, 'dashboard/org-dashboard.html', context)


def dash_exp(request):
    user = request.user
    posts_data = Exp.objects.filter(user=user)

    context = {
        "user": user,
        "posts": posts_data,
    }
    return render(request, 'dashboard/dashboard.html', context)

@login_required
def opportunity_manager(request):
    opps = Opportunity.objects.filter(user=request.user)
    count = opps.count()
    
    page_number = request.GET.get('page', 1)


    page = Paginator(opps, 10)
    page_obj = page.get_page(page_number)
    context = {
        'posts': opps,
        "count": count,
        'page_number': page_obj
    }
    if request.user.user_type == 'individual':
        return render(request, 'dashboard/dashboard-manage-looks.html', context)
    else:
        return render(request, 'dashboard/org-dashboard-manage-looks.html', context)


@login_required
def application_manager(request):
    user = request.user
    applications = Application.objects.filter(sender=user)
    opps = Opportunity.objects.filter(application__in=applications).distinct().order_by('-pub_date')
    count = opps.count()

    page_number = request.GET.get('page', 1)
    paginator = Paginator(opps, 10)
    page_obj = paginator.get_page(page_number)

    # Create a list of dictionaries containing both the opportunity and its corresponding application
    opportunities_with_applications = []
    for opp in page_obj.object_list:
        app = applications.filter(opportunity=opp).first()
        if app:
            opportunities_with_applications.append({
                'opportunity': opp,
                'application': app
            })

    context = {
        'opportunities_with_applications': opportunities_with_applications,
        'count': count,
        'page_number': page_number,
        'page_obj': page_obj
    }
    return render(request, 'dashboard/dashboard-manage-apply.html', context)

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
            return redirect(to="exp-manager")
    else:
        forms = ExpForm()
    return render(request, 'dashboard/dashboard-manage-exp.html', {'forms': forms})



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
    return render(request, 'dashboard/dashboard-manage-exp.html', context)

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
            messages.success(request, 'Your education entry was created.')
            return redirect('edu_manager')
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
        return redirect('edu-manager')
    else:
        return HttpResponseForbidden("You don't have permission to delete this experience.")



@login_required
def application_list(request, pk):
    opp = Opportunity.objects.get(pk=pk)
    applications = Application.objects.filter(opportunity=opp)
    
    context = {
        'apps': applications,
        'opp': opp
    }
    if request.user.user_type == 'individual':
        return render(request, 'dashboard/dashboard-applications.html', context)
    else:
        return render(request, 'dashboard/org-dashboard-applications.html', context)

@login_required
def application_approve(request, pk):
    app = Application.objects.get(pk=pk)
    postpk = app.opportunity.pk
    app.status = "Accepted"
    app.save()
    Notifications.objects.create(user_sender=request.user, user_revoker=app.sender, type_of_notification="result")
    return redirect(to="manage-application-list", pk=postpk)

@login_required
def application_reject(request, pk):
    app = Application.objects.get(pk=pk)
    postpk = app.opportunity.pk
    app.status = "Rejected"
    app.save()
    Notifications.objects.create(user_sender=request.user, user_revoker=app.sender, type_of_notification="result")
    return redirect(to="manage-application-list", pk=postpk)

@login_required
def inbox(request):
    requests = ContactRequest.objects.filter(receiver=request.user)

    context = {
        "messages": requests
    }
    if request.user.user_type == 'individual':
        return render(request, 'dashboard/dashboard-inbox.html', context)
    else:
        return render(request, 'dashboard/org-dashboard-inbox.html', context)