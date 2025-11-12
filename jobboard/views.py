from django.shortcuts import render, get_object_or_404, redirect
from .models import JobPost, JobApplication, JobCategory, BlogPost, BlogCategory
from accounts.models import EmployerProfile, CustomUser
from .forms import JobApplicationForm, JobPostForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.core.cache import cache
from django.db.models import Q
from django.utils.timezone import now, timedelta
from django.db.models import Count, Sum
from django.utils import timezone




def home(request):
    top_categories = JobCategory.objects.annotate(
        job_count=Count('job_posts_category', filter=Q(job_posts_category__status='published'))
    ).order_by('-job_count')[:10] 
    
    companies = EmployerProfile.objects.all()

    company_data = []

    for company in companies:
        published_jobs = JobPost.objects.filter(employee=company, status='published')
        company_data.append({
            'company': company,
            'published_jobs': published_jobs
        })
    total_users = CustomUser.objects.count()
    total_job_posts = JobPost.objects.count() 
    total_vacancies = JobPost.objects.aggregate(total_vacancies=Sum('no_of_vacancy'))['total_vacancies'] or 0 
    recentblog = BlogPost.objects.filter(published=True).order_by('-created_at')[:3]
    
    today = timezone.now().date()
    expired_jobs = JobPost.objects.filter(application_deadline=today)
    jobs_today_deadline_count= expired_jobs.count()
   
    context = {
        'top_categories': top_categories,
        'company_data': company_data,
        'total_job_posts': total_job_posts,
        'total_vacancies': total_vacancies,
        'total_users': total_users,
        'job': expired_jobs,
        'jobs_today_deadline_count': jobs_today_deadline_count,
        'recentblog': recentblog,
    }
    return render(request, 'home.html', context)   


def job_list(request):
    sort_by = request.GET.get('sort_by', 'most_recent')
    show_count = request.GET.get('show_count', 10)
    category_id = request.GET.get('category')
    keyword = request.GET.get('keyword', '').strip()
    location = request.GET.get('location', '').strip()
    date_filter = request.GET.get('date_filter', '')  
    
    # Check if user clicked "Remove" on a filter
    if 'remove_category' in request.GET:
        category_id = ''
    if 'remove_keyword' in request.GET:
        keyword = ''
    if 'remove_location' in request.GET:
        location = ''
    if 'remove_date' in request.GET:
        date_filter = ''

    # Check if "Clear All" was clicked
    if 'clear_all' in request.GET:
        category_id = keyword = location = date_filter = ''
        

    try:
        show_count = int(show_count)
    except ValueError:
        show_count = 10

 
    filters = Q()
    if category_id:
        filters &= Q(job_category_id=category_id)


    if keyword:
        filters &= Q(title__icontains=keyword) | Q(job_description__icontains=keyword) | Q(job_requirements__icontains=keyword)


    if location:
        filters &= Q(job_location__icontains=location)

    today = now().date()
    if date_filter:
        if date_filter == "today":
            filters &= Q(application_deadline=today)
        elif date_filter == "last_hour":
            filters &= Q(created_at__gte=now() - timedelta(hours=1))
        elif date_filter == "last_24_hours":
            filters &= Q(created_at__gte=now() - timedelta(days=1))
        elif date_filter == "last_7_days":
            filters &= Q(created_at__gte=now() - timedelta(days=7))
        elif date_filter == "last_14_days":
            filters &= Q(created_at__gte=now() - timedelta(days=14))
        elif date_filter == "last_30_days":
            filters &= Q(created_at__gte=now() - timedelta(days=30))

    job_type_map = {
        "full_time": "Full Time",
        "internship": "Internship",
        "part_time": "Part Time",
        "temporary": "Temporary",
        "contractual": "Contractual"
    }
    if sort_by in job_type_map:
        filters &= Q(job_type=job_type_map[sort_by])

    jobs = JobPost.objects.filter(filters, status='published').order_by('-created_at').only(
    "id", "title", "job_category_id", "job_type", "job_location", "created_at"
    )

    total_jobs = jobs.count()
    query_params = request.GET.copy()

    # Paginate 
    paginator = Paginator(jobs, show_count)
    page_number = request.GET.get('page')
    page_jobs = paginator.get_page(page_number)

    #Cached Categories
    categories = cache.get('job_categories')
    if not categories:
        categories = list(JobCategory.objects.values('id', 'name'))
        cache.set('job_categories', categories, timeout=3600)

    date_filter_options = {
        "today": "Today Deadline",
        "last_hour": "Last hour",
        "last_24_hours": "Last 24 hours",
        "last_7_days": "Last 7 days",
        "last_14_days": "Last 14 days",
        "last_30_days": "Last 30 days",
        "all jobs": "All"
    }
    selected_category_name = ''
    if category_id:
        selected_cat_obj = JobCategory.objects.filter(id=category_id).first()
        if selected_cat_obj:
            selected_category_name = selected_cat_obj.name 
        
    return render(request, 'jobs/job_list.html', {
        'jobs': page_jobs,
        'total_jobs': total_jobs,
        'sort_by': sort_by,
        'show_count': show_count,
        'category': categories,
        'selected_category': category_id,
        'keyword': keyword,
        'location': location,
        'date_filter_options': date_filter_options,  
        'selected_date_filter': date_filter ,
        'query_params': query_params,
        'selected_category_name': selected_category_name,
    })


def job_detail(request, job_id):
    job = get_object_or_404(JobPost, id=job_id)
    seeker = request.user.seeker_profile if request.user.is_authenticated and hasattr(request.user, 'seeker_profile') else None
    related_jobs = JobPost.objects.filter(job_category=job.job_category).exclude(id=job.id).order_by('-created_at')[:9]
    has_applied = JobApplication.objects.filter(job=job, seeker=seeker).exists() if seeker else False

    return render(request, 'jobs/job_detail.html', {
        'job': job,
        'seeker': seeker,
        'related_jobs': related_jobs,
        'has_applied': has_applied
    })
    
# def job_detail(request, job_id):
#     # Fetch the job along with its related category in one query
#     job = get_object_or_404(JobPost.objects.select_related('job_category'), id=job_id)

#     # Fetch seeker profile efficiently
#     seeker = getattr(request.user, 'seeker_profile', None) if request.user.is_authenticated else None

#     # Use prefetch_related to optimize related jobs query
#     related_jobs = JobPost.objects.filter(job_category=job.job_category)\
#         .exclude(id=job.id)\
#         .select_related('job_category')\
#         .only('id', 'title', 'created_at', 'job_category')\
#         .order_by('-created_at')[:9]

#     # Optimize has_applied check by using .only() to fetch minimal data
#     has_applied = JobApplication.objects.filter(job=job, seeker=seeker).only('id').exists() if seeker else False

#     return render(request, 'jobs/job_detail.html', {
#         'job': job,
#         'seeker': seeker,
#         'related_jobs': related_jobs,
#         'has_applied': has_applied
#     })
       

@login_required
def create_job(request):
    if request.method == "POST":
        form = JobPostForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.poster = request.user  
            job.save()
            return redirect('job_list')
    else:
        form = JobPostForm()
    
    return render(request, 'jobs/create_job.html', {'form': form})


from django.http import JsonResponse
@login_required
def apply_job(request, job_id):
    job = get_object_or_404(JobPost, id=job_id)
    seeker = request.user.seeker_profile
    
    if JobApplication.objects.filter(job=job, seeker=seeker).exists():
        return JsonResponse({"success": False, "error": "You have already applied for this job."})
 
 
    if request.method == "POST":
        form = JobApplicationForm(request.POST, request.FILES, seeker=seeker)
        if form.is_valid():
            application = form.save(commit=False)
            application.job = job
            application.seeker = seeker
            application.save()
            return JsonResponse({"success": True})
        else:
            return JsonResponse({"success": False, "error": "Invalid form submission."})

    return JsonResponse({"success": False, "error": "Invalid request."})


@login_required
def employee_applications(request):
    applications = JobApplication.objects.filter(job__poster=request.user)
    return render(request, 'jobs/employee_applications.html', {'applications': applications})


def about_us(request):
    return render(request, 'about_us.html')

def contact_us(request):
    return render(request, 'contact_us.html') 



def blog_list(request):
    posts = BlogPost.objects.filter(published=True).order_by('-created_at')
    recentjob = BlogPost.get_recent() 
    
    blogCategory = BlogCategory.objects.annotate(post_count=Count('blogpost'))
    paginator = Paginator(posts, 10)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'blog/blog_list.html', {'page_obj': page_obj, 'blogCategory': blogCategory, 'recentjob': recentjob})


def blog_detail(request, post_id):
    post = get_object_or_404(BlogPost, id=post_id, published=True)
    return render(request, 'blog/blog_detail.html', {'post': post})
 
 