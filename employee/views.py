from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from accounts.models import EmployerProfile, CustomUser
from .forms import EmployerProfileForm, JobPostForm
from django.http import JsonResponse, HttpResponseForbidden
from django.utils import timezone
from jobboard.models import JobApplication 
from jobboard.models import JobPost


# Create your views here.    
# @login_required
# def employer_dashboard(request):
#     if not request.user.is_employer:  
#         return HttpResponseForbidden("Access restricted to employers.")
#     if not request.user.is_approved:
#         return render(request, 'registration/pending_approval.html')
    
#     profile = get_object_or_404(EmployerProfile, user=request.user) 
#     job_posts = profile.job_posts.all()  
#     job_count = job_posts.count()  
#     application_count = JobApplication.objects.filter(job__in=job_posts).count()

#     return render(request, 'core/dashboard.html', {
#         'profile': profile,
#         'job_posts': job_posts,
#         'job_count': job_count,
#         'application_count': application_count
#     })


@login_required
def view_employer_profile(request, user_id=None):
    # If user_id is provided in URL, fetch that user's profile
    if user_id:
        profile_user = get_object_or_404(CustomUser, id=user_id)
        profile = get_object_or_404(EmployerProfile, user=profile_user)
    else:
        # Only employers can view their own profile
        if not request.user.is_employer:
            return HttpResponseForbidden("Access restricted to employers.")
        if not request.user.is_approved:
            return render(request, 'registration/pending_approval.html') 
        profile = get_object_or_404(EmployerProfile, user=request.user)

    jobs = JobPost.objects.filter(employee=profile).order_by('-created_at')

    total_experience = None
    if profile.founded_date:
        total_experience = timezone.now().year - profile.founded_date.year

    return render(request, 'employer-detail-v2.html', {
        'profile': profile,
        'total_experience': total_experience,
        'jobs': jobs,
    })


# @login_required
# def edit_employer_profile(request):
#     if not request.user.is_employer:
#         return HttpResponseForbidden("Access restricted to employers.")
    
    
#     profile = get_object_or_404(EmployerProfile, user=request.user)
    
#     if request.method == "POST" and request.FILES.get("logo"):
#         profile.logo = request.FILES["logo"]
#         profile.save()
#         return JsonResponse({"success": True, "logo_url": profile.logo.url}) 
    
#     if request.method == "POST":
#         form = EmployerProfileForm(request.POST, request.FILES, instance=profile)
#         if form.is_valid():
#             form.save()
#             return redirect('employer_profile')  # Redirect to the profile page after saving
#     else:
#         form = EmployerProfileForm(instance=profile)
    
#     return render(request, 'employer-profile.html', {'form': form, 'profile': profile}) 


@login_required
def employer_profile(request):
    if not request.user.is_employer:
        return HttpResponseForbidden("Access restricted to employers.")
    if not request.user.is_approved:
        return render(request, 'registration/pending_approval.html')
    
    
    profile = get_object_or_404(EmployerProfile, user=request.user)
    
    if request.method == "POST" and request.FILES.get("logo"):
        profile.logo = request.FILES["logo"]
        profile.save()
        return JsonResponse({"success": True, "logo_url": profile.logo.url}) 
    
    if request.method == "POST":
        form = EmployerProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('employer_profile')  
    else:
        form = EmployerProfileForm(instance=profile)
    
    return render(request, 'core/dash-company-profile.html', {'form': form, 'profile': profile}) 


from django.contrib import messages 

@login_required
def create_job(request):
    if not request.user.is_employer:
        return HttpResponseForbidden("Access restricted to employers.") 
    if not request.user.is_approved:
        return render(request, 'registration/pending_approval.html')
    
    employer = get_object_or_404(EmployerProfile, user=request.user)  

    if request.method == "POST":
        form = JobPostForm(request.POST)
        print(form.errors)
        if form.is_valid():
            job = form.save(commit=False)  
            job.employee = employer  
            job.save()  
            messages.success(request, "Job posted successfully!")
            return redirect('manage-job')  
        else:
            messages.error(request, "Please correct the errors below.")  

    else:
        form = JobPostForm()

    return render(request, 'job/create_job.html', {'form': form, 'profile': employer}) 

@login_required
def manage_job(request):
    if not request.user.is_employer:
        return HttpResponseForbidden("Access restricted to employers.") 
    if not request.user.is_approved:
        return render(request, 'registration/pending_approval.html')
    
    profile = get_object_or_404(EmployerProfile, user=request.user)  
    job_posts = profile.job_posts.all().order_by('-created_at')
    

    return render(request, 'job/manage_job.html', {'job_posts':job_posts, 'profile': profile}) 

@login_required
def delete_job(request, job_id):
    job = get_object_or_404(JobPost, id=job_id)
    
    if not request.user.is_superuser:
        employer_profile = get_object_or_404(EmployerProfile, user=request.user)
        if job.employee != employer_profile:
            return HttpResponseForbidden("You do not have permission to delete this job.")
        else:
            job.delete()
            messages.success(request, "Job deleted successfully.")
            return redirect('manage-job')

    job.delete()
    messages.success(request, "Job deleted successfully.")
    return redirect('job_post_list')



@login_required
def job_applicants(request, job_id):
    if not request.user.is_employer:
        return HttpResponseForbidden("Access restricted to employers.") 
    if not request.user.is_approved:
        return render(request, 'registration/pending_approval.html')
    
    profile = get_object_or_404(EmployerProfile, user=request.user) 
    job = get_object_or_404(JobPost, id=job_id)

    employer_profile = get_object_or_404(EmployerProfile, user=request.user)
    if job.employee != employer_profile:
        return HttpResponseForbidden("You do not have permission to view applicants for this job.")

    applications = JobApplication.objects.filter(job=job) 

    return render(request, 'job/job_applicants.html', {'job': job, 'applications': applications, 'profile': profile}) 



from django.shortcuts import get_object_or_404, render
from django.http import Http404
from datetime import date
from accounts.models import SeekerProfile 

def view_profile(request, user_id=None):
    # If no user_id is provided, use the logged-in user (if available)
    if user_id:
        profile_user = get_object_or_404(SeekerProfile, user__id=user_id).user
    else:
        raise Http404("User not found.")

    # Fetch user profile and resume
    profile = get_object_or_404(SeekerProfile, user=profile_user)
    
    print(profile)

    # Calculate age if date_of_birth exists
    age = None
    if profile.my_resume.date_of_birth:
        today = date.today()
        age = today.year - profile.my_resume.date_of_birth.year - (
            (today.month, today.day) < (profile.my_resume.date_of_birth.month, profile.my_resume.date_of_birth.day)
        )

    # Fetch related data
    educations = profile.my_resume.educations.all().order_by('-id')
    employments = profile.my_resume.employments.all().order_by('-id')
    skills = profile.my_resume.skills.all().order_by('-id')
    projects = profile.my_resume.projects.all().order_by('-id')
    certifications = profile.my_resume.certifications.all().order_by('-id')
    total_years_of_experience = sum([employment.duration() for employment in employments])

    # Template for rendering
    template = 'job/seeker-profile.html'

    context = {
        'profile': profile,
        'resume': profile.my_resume,
        'educations': educations,
        'employments': employments,
        'skills': skills,
        'projects': projects,
        'certifications': certifications,
        'age': age,
        'total_years_of_experience': total_years_of_experience,
    }

    return render(request, template, context) 
