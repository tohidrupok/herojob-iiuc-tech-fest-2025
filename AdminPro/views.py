from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from jobboard.models import JobApplication 
from jobboard.models import JobPost
from django.utils import timezone
from accounts.models import CustomUser
from django.contrib import messages
from accounts.models import SeekerProfile, EmployerProfile
from .forms import PostJobForm, JobCategoryForm
from accounts.forms import EmployerRegistrationForm
from jobboard.models import JobCategory 
from jobboard.models import BlogPost
from jobboard.forms import BlogPostForm 

# Function to check if user is superuser & staff
def is_superuser(user):
    return user.is_authenticated and user.is_staff and user.is_superuser

# Superuser Dashboard View
@login_required
@user_passes_test(is_superuser)
def superuser_dashboard(request): 
    
    job_posts = JobPost.objects.all()
    job_count = job_posts.count()  
    application_count = JobApplication.objects.all().count()
    recent_job_applications = JobApplication.objects.all().order_by('-applied_at')[:8]
    today_job_posts = JobPost.objects.filter(created_at__date=timezone.now().date()).count() 
    today_applications = JobApplication.objects.filter(applied_at__date=timezone.now().date()).count() 
    
    return render(request, 'panel/dashboard.html', {

        'job_count': job_count,
        'application_count': application_count,
        
        'today_job_posts': today_job_posts,
        'today_applications': today_applications,
        'recent_job_applications':recent_job_applications
    })


@login_required
@user_passes_test(is_superuser)  
def delete_profile(request, user_id):
    
    user = get_object_or_404(CustomUser, id=user_id) 
    if user.is_superuser:
        messages.error(request, "Admin accounts cannot be deleted.")
        return redirect('all_seeker_profiles')

    user.delete()
    messages.success(request, f"User {user.username} has been deleted successfully.")
    return redirect('all_seeker_profiles')  


@login_required
@user_passes_test(is_superuser)  
def job_post_list(request):
    job_posts = JobPost.objects.all()
    return render(request, 'panel/job_post_list.html', {'job_posts': job_posts})

@login_required
@user_passes_test(is_superuser)  
def pending_job_post_list(request):
    pending_job_posts = JobPost.objects.filter(status='pending')
    return render(request, 'panel/approve_job.html', {'job_posts': pending_job_posts})


@login_required
@user_passes_test(is_superuser) 
def publish_job(request, job_id):
    job = get_object_or_404(JobPost, id=job_id)
    job.status = 'published'  
    job.save()
    return redirect('approve_job_post_list') 

@login_required
@user_passes_test(is_superuser) 
def reject_job(request, job_id):
    job = get_object_or_404(JobPost, id=job_id)
    job.status = 'rejected' 
    job.save()
    return redirect('job_post_list') 


@login_required
@user_passes_test(is_superuser) 
def superuser_job_applicants(request, job_id):

    job = get_object_or_404(JobPost, id=job_id)
    applications = JobApplication.objects.filter(job=job)

    return render(request, 'panel/job_applicants_superuser.html', {
        'job': job,
        'applications': applications,
    }) 
    
    
def delete_job_application(request, application_id):
    application = get_object_or_404(JobApplication, id=application_id)
    
    if request.user != application.seeker.user and not request.user.is_superuser:
        messages.error(request, "You do not have permission to delete this application.")
        return redirect('home')  

    application.delete()
    messages.success(request, "Job application deleted successfully.")
    return redirect('job_post_list')  

@login_required
@user_passes_test(is_superuser)
def show_all_seeker_profiles(request):
    # Get all seeker profiles
    seeker_profiles = SeekerProfile.objects.all()

    context = {
        'resume': seeker_profiles
    }
    
    return render(request, 'panel/all-seeker.html', context)  

@login_required
@user_passes_test(is_superuser)
def show_all_employee_profiles(request):

    employer_profiles = EmployerProfile.objects.all()

    context = {
        'employee': employer_profiles
    }
    
    return render(request, 'panel/all-employee.html', context) 


@login_required
@user_passes_test(is_superuser)
def post_job(request):

    if request.method == "POST":
        form = PostJobForm(request.POST)
        print(form.errors)
        if form.is_valid():
            job = form.save(commit=False)  
            job.save()  
            messages.success(request, "Job posted successfully!")
            return redirect('job_post_list')  
        else:
            messages.error(request, "Please correct the errors below.")  

    else:
        form = PostJobForm()

    return render(request, 'panel/post_job.html', {'form': form})  


@login_required
@user_passes_test(is_superuser)
def category_page(request):
    categories = JobCategory.objects.all()
    form = JobCategoryForm()
    edit_category = None  

    if request.method == 'POST':
        # Add New Category
        if 'add_category' in request.POST:
            form = JobCategoryForm(request.POST)
            if form.is_valid():
                form.save()  
                return redirect('category_page')

        # Edit Existing Category
        elif 'edit_category' in request.POST:
            category_id = request.POST.get('category_id')
            category = get_object_or_404(JobCategory, id=category_id)
            form = JobCategoryForm(request.POST, instance=category)  
            if form.is_valid():
                form.save() 
                return redirect('category_page')

        # Delete Category
        elif 'delete_category' in request.POST:
            category_id = request.POST.get('category_id')
            category = get_object_or_404(JobCategory, id=category_id)
            category.delete()  
            return redirect('category_page')

    # Check if there's an edit action for an existing category
    if 'category_id' in request.GET:
        category_id = request.GET.get('category_id')
        edit_category = get_object_or_404(JobCategory, id=category_id)
        form = JobCategoryForm(instance=edit_category)  

    return render(request, 'panel/category_page.html', {
        'categories': categories,
        'form': form,
        'edit_category': edit_category
    })
    
    
@login_required
@user_passes_test(is_superuser)    
def add_employer(request):
    if request.method == 'POST':
        form = EmployerRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = 'employer'
            user.is_approved = True  
            user.save()
            return redirect('all_employee_profiles')
    else:
        form = EmployerRegistrationForm()
    return render(request, 'registration/register_employer.html', {'form': form}) 


@login_required
@user_passes_test(is_superuser)   
def blog_create(request):
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('blog_list')
    else:
        form = BlogPostForm()
    return render(request, 'panel/blog_form.html', {'form': form})

@login_required
@user_passes_test(is_superuser)   
def blog_update(request, post_id):
    post = get_object_or_404(BlogPost, id=post_id)
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            updated_post = form.save(commit=False)

            # Ei check ta just safety er jonno, normal case e lagbe na
            if not updated_post.created_at:
                updated_post.created_at = post.created_at  # Preserve the original

            updated_post.save()
            form.save_m2m()  # for categories
            return redirect('blog_detail', post_id=post.id)
    else:
        form = BlogPostForm(instance=post)
    return render(request, 'panel/blog_form.html', {'form': form})

@login_required
@user_passes_test(is_superuser)   
def blog_delete(request, post_id):
    post = get_object_or_404(BlogPost, id=post_id)
    if request.method == 'POST':
        post.delete()
        return redirect('blog_list')
    return render(request, 'panel/blog_confirm_delete.html', {'post': post}) 


@login_required
@user_passes_test(is_superuser)  
def blog_list(request):
    posts = BlogPost.objects.filter(published=True).order_by('-created_at')
    return render(request, 'panel/blog_list.html', {'posts': posts})


@login_required
@user_passes_test(is_superuser)  
def blog_detail(request, post_id):
    post = get_object_or_404(BlogPost, id=post_id, published=True)
    return render(request, 'panel/blog_detail.html', {'post': post})