from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import OpportunityForm, FilterForm, AppForm, ApplicationForm
from .models import Opportunity, Experience, Application
from django.template.loader import render_to_string
from django.http import JsonResponse, HttpResponseForbidden
from django.template.defaultfilters import slugify
from django.core.paginator import Paginator
from easyaudit.models import RequestEvent
# Create your views here.
from taggit.models import Tag
from django.db.models import Q
from django.http import HttpResponse


# views.py

CATEGORY_MAPPING = {
    '':'',
    "All categories": "",
    "Academic Enrichment": "academic_enrichment",
    "Extracurricular Activities": "extracurricular_activities",
    "STEM": "stem",
    "Internships and Work Experience": "internships_work_experience",
    "Leadership Development": "leadership_development",
    "College and Career Readiness": "college_career_readiness",
    "Personal Development": "personal_development",
    "Cultural and Global Awareness": "cultural_global_awareness",
    "Health and Wellness": "health_wellness",
    "The Arts and Creativity": "arts_creativity",
}

@login_required
def opportunity(request):
    if request.method == 'POST':
        form = OpportunityForm(request.POST, request.FILES)

        if form.is_valid():
            newform = form.save(commit=False)
            newform.user = request.user
            newform.slug = slugify(newform.title)
            newform.save()
            form.save_m2m()
            messages.success(request, 'Your look was created successfully.')
            return redirect(to="opportunity-home")
    else:
        form = OpportunityForm()
    if(request.user.user_type=='individual'):
        return render(request, 'dashboard/dashboard-new-look.html', {'form': form})
    else:
         return render(request, 'dashboard/org-dashboard-new-look.html', {'form': form})


def tagged(request, slug):
    tag = get_object_or_404(Tag, slug=slug)

    opps = Opportunity.objects.filter(tags=tag)

@login_required
def opportunity_home(request):
    keyword = request.GET.get('search', '')
    location = request.GET.get('location', '')
    category = request.GET.get('category', '')
    
    time = request.GET.get('time', '')
    location = request.GET.get('location', '')
    page_number = request.GET.get('page', 1)
    
    matching_tags = Tag.objects.filter(name__icontains=keyword)
    posts = Opportunity.objects.filter(tags__in=matching_tags).distinct()
    posts = posts.filter(location__icontains=location)
    posts = posts.filter(category__icontains=CATEGORY_MAPPING[category])
    print(posts)
    if time == '2':
            posts = posts.order_by('pub_date')
    elif time == '1':
            posts = posts.order_by('-pub_date')
    else:
            posts = posts.order_by('-visits')
    
    page = Paginator(posts, 10)
    page_obj = page.get_page(page_number)
    

    context = {
        "all_posts": posts,
        "posts": page_obj,
        "time": time
    }
    templates = 'opportunity/opportunity_home.html'
    
    return render(request, templates, context)

@login_required
def post_detail(request, pk):
    post = get_object_or_404(Opportunity, pk=pk)
    url = reverse('post-detail', args=[pk])
    visit = RequestEvent.objects.filter(url=url, method="GET").count()
    raw_responsibilities = post.responsibilities
    responsibilities_list = [responsibility.strip() for responsibility in raw_responsibilities.split('#') if responsibility.strip()]
    form = ApplicationForm()
    post.visits += 1
    post.save()
    success_message = None
    if request.POST:
        form = ApplicationForm(request.POST)
        if form.is_valid():
            message = form.cleaned_data['application_text']
            user = request.user
            new_app = Application.objects.create(
                opportunity=post,
                sender=user,
                text=message
            )
            post.num_applications += 1
            new_app.save()
            post.save()
            new_app.save()
    context = {
        'opportunity': post,
        'visits': visit,
        'form': form,
        'resps': responsibilities_list,
    }
    return render(request, 'opportunity/post_detail.html', context)

@login_required
def data(request):
    return render(request, 'opportunity/data.html')



@login_required
def delete_opportunity(request, pk):
    post = get_object_or_404(Opportunity, pk=pk)

    if(post.user == request.user):
        post.delete()
        messages.success(request, 'Your look was deleted successfully.')
        return redirect(to="users-home")
    return HttpResponseForbidden("You don't have permission to delete this opportunity.")

@login_required
def like_opportunity(request, pk):
    opportunity = get_object_or_404(Opportunity, pk=pk)

    # Toggle the 'like' field
    opportunity.like = not opportunity.like
    opportunity.save()

    # Redirect back to the same page or wherever you want
    return redirect(request.META.get('HTTP_REFERER', "{% url 'opportunity-home' %}"))

@login_required
def apply_opportunity(request, pk):
    opp = Opportunity.objects.get(pk=pk)

    if request.user.profile.has_applied:
            messages.error(request, "You've already applied to this position")
            return redirect("post-detail", pk=pk)
    else:
        if request.method == 'POST':
            form = ApplicationForm(request.POST)
            
            
            if form.is_valid():
                message = form.cleaned_data['application_text']
                info = form.cleaned_data['application_contact']
                user = request.user
                new_app = Application.objects.create(
                    opportunity=opp,
                    sender=user,
                    text=message,
                    contact=info,
                )
                opp.num_applications += 1
                opp.save()
                new_app.save()

                profile = request.user.profile
                profile.has_applied = True
                print(request.user.profile.has_applied)
                profile.save()
                
                messages.success(request, "Application sent!")
                return redirect(to='post-detail', pk=pk)
            
        else:
            form = ApplicationForm()
    
        return render(request, 'opportunity/wittleapply.html', {'form': form, 'opp': opp})
   