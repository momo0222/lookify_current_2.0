from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.contrib.auth.decorators import login_required
from .forms import OrgSearchForm
from users.models import OrganizationProfile

User = get_user_model()

@login_required
def org_home(request):
    form = OrgSearchForm(request.GET or None)
    search = request.GET.get('search', '')
    school = request.GET.get('school', '')

    orgs = User.objects.filter(
        Q(user_type='organization') &
        (Q(organizationprofile__domain__icontains=search) |
         Q(organizationprofile__about__icontains=search))
    )

    if school:
        orgs = orgs.filter(organizationprofile__school_id=school)

    orgs = orgs.annotate(
        opportunity_count=Count('opportunity')  # Use the related_name if specified in the ForeignKey
    ).order_by('-opportunity_count')




    page = Paginator(orgs, 9)
    page_number = request.GET.get('page', 1)

    page_obj = page.get_page(page_number)

    context = {
        'form':form,
        'orgs': orgs,
        'page_number': page_obj,
    }
    return render(request, 'orgs/orgs-home.html', context)


