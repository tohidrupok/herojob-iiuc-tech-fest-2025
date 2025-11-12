from django.shortcuts import render, redirect, get_object_or_404
from .models import Resume, Education, Employment, Skill, Project, Certification
from .forms import ResumeForm, EducationForm, EmploymentForm, SkillForm, ProjectForm, CertificationForm, SeekerProfileForm, PersonalDetailsForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required 
from accounts.models import SeekerProfile
from datetime import date
from django.http import JsonResponse, HttpResponseForbidden
from jobboard.models import JobApplication, JobPost
from django.utils import timezone


@login_required
def resume_detail(request, resume_id):

    resume = get_object_or_404(Resume, id=resume_id)
    
    # Fetch related data
    educations = resume.educations.all()
    employments = resume.employments.all()
    skills = resume.skills.all()
    projects = resume.projects.all()
    certifications = resume.certifications.all()

    context = {
        'resume': resume,
        'educations': educations,
        'employments': employments,
        'skills': skills,
        'projects': projects,
        'certifications': certifications,
    }
    return render(request, 'resume_detail.html', context) 


@login_required
def my_resume(request):
    
    if not request.user.is_seeker:  
        return HttpResponseForbidden("Access restricted.")
    
    resume = get_object_or_404(Resume, user=request.user)
    
    if request.method == "POST" and request.FILES.get("logo"):
        resume.image = request.FILES["logo"]
        resume.save()
        return JsonResponse({"success": True, "logo_url": resume.image.url}) 
    
    if request.method == "POST":
        form = ResumeForm(request.POST, request.FILES, instance=resume)
        if form.is_valid():
            form.save()
            return redirect('my_resume')  
    else:
        form = ResumeForm(instance=resume) 
            
    # Fetch related data
    educations = resume.educations.all().order_by('-id')
    employments = resume.employments.all().order_by('-id')
    skills = resume.skills.all().order_by('-id')
    projects = resume.projects.all().order_by('-id')
    certifications = resume.certifications.all().order_by('-id')
    

    context = {
        'form': form,
        'resume': resume,
        'educations': educations,
        'employments': employments,
        'skills': skills,
        'projects': projects,
        'certifications': certifications,
        
        
    }
    return render(request, 'resume_detail.html', context) 

# @login_required
# def seeker_profile(request):
   
#     resume = get_object_or_404(Resume, user=request.user)
    
#     if request.method == "POST" and request.FILES.get("logo"):
#         resume.image = request.FILES["logo"]
#         resume.save()
#         return JsonResponse({"success": True, "logo_url": resume.image.url}) 
    
#     if request.method == "POST":
#         form = ResumeForm(request.POST, request.FILES, instance=resume)
#         if form.is_valid():
#             form.save()
#             return redirect('employer_profile')  
#     else:
#         form = ResumeForm(instance=resume)
    
#     return render(request, 'resume_detail.html', {'form': form, 'resume': resume}) 

@login_required
def all_resumes(request):
    resumes = Resume.objects.all()
    return render(request, 'all_resume.html', {'resumes': resumes}) 


@login_required
def edit_resume(request):
    if not request.user.is_seeker:  
        return HttpResponseForbidden("Access restricted.")
    
    resume = get_object_or_404(Resume, user=request.user)
    if request.method == 'POST':
        form = ResumeForm(request.POST, instance=resume)
        if form.is_valid():
            form.save()
            return redirect('my_resume')
    else:
        form = ResumeForm(instance=resume)
    return render(request, 'edit.html', {'form': form,'resume': resume })

@login_required
def edit_education(request, pk):
    if not request.user.is_seeker:  
        return HttpResponseForbidden("Access restricted.")
    
    education = get_object_or_404(Education, pk=pk)
    if request.method == 'POST':
        form = EducationForm(request.POST, instance=education)
        if form.is_valid():
            form.save()
            return redirect('my_resume')
    else:
        form = EducationForm(instance=education)
    resume = get_object_or_404(Resume, user=request.user)
    return render(request, 'edit.html', {'form': form,'resume': resume })

@login_required
def delete_education(request, pk):
    
    if not request.user.is_seeker:  
        return HttpResponseForbidden("Access restricted.")
    
    education = get_object_or_404(Education, pk=pk)

    if request.method == 'POST':
        education.delete()
        return redirect('my_resume')  

    return redirect('my_resume') 

@login_required
def delete_employment(request, pk):
    
    if not request.user.is_seeker:  
        return HttpResponseForbidden("Access restricted.")
    
    employment = get_object_or_404(Employment, pk=pk)

    if request.method == 'POST':
        employment.delete()
        return redirect('my_resume')  

    return redirect('my_resume')

@login_required
def delete_project(request, pk):
    
    if not request.user.is_seeker:  
        return HttpResponseForbidden("Access restricted.")
    
    
    project = get_object_or_404(Project, pk=pk)

    if request.method == 'POST':
        project.delete()
        return redirect('my_resume')  

    return redirect('my_resume')

@login_required
def delete_certification(request, pk):
    
    if not request.user.is_seeker:  
        return HttpResponseForbidden("Access restricted.")
    
    
    certification = get_object_or_404(Certification, pk=pk)

    if request.method == 'POST':
        certification.delete()
        return redirect('my_resume')  

    return redirect('my_resume')

@login_required
def delete_skill(request, pk):
    if not request.user.is_seeker:  
        return HttpResponseForbidden("Access restricted.")
    
    skill = get_object_or_404(Skill, pk=pk)

    if request.method == 'POST':
        skill.delete()
        return redirect('my_resume')  

    return redirect('my_resume')

@login_required
def edit_employment(request, pk):
    if not request.user.is_seeker:  
        return HttpResponseForbidden("Access restricted.")
    
    employment = get_object_or_404(Employment, pk=pk)
    resume = get_object_or_404(Resume, user=request.user)
    
    if request.method == 'POST':
        form = EmploymentForm(request.POST, instance=employment)
        if form.is_valid():
            form.save()
            return redirect('my_resume')
    else:
        form = EmploymentForm(instance=employment)
        
    return render(request, 'edit.html', {'form': form,'resume': resume })

@login_required
def edit_skill(request, pk):
    if not request.user.is_seeker:  
        return HttpResponseForbidden("Access restricted.")
    
    skill = get_object_or_404(Skill, pk=pk)
    resume = get_object_or_404(Resume, user=request.user)
    if request.method == 'POST':
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():
            form.save()
            return redirect('my_resume')
    else:
        form = SkillForm(instance=skill)
        
    return render(request, 'edit.html', {'form': form,'resume': resume })

@login_required
def edit_project(request, pk):
    if not request.user.is_seeker:  
        return HttpResponseForbidden("Access restricted.")
    
    project = get_object_or_404(Project, pk=pk)
    resume = get_object_or_404(Resume, user=request.user) 
    
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect('my_resume')
    else:
        form = ProjectForm(instance=project)
    return render(request, 'edit.html', {'form': form,'resume': resume })

@login_required
def edit_certification(request, pk):
    if not request.user.is_seeker:  
        return HttpResponseForbidden("Access restricted.")
    
    certification = get_object_or_404(Certification, pk=pk)
    resume = get_object_or_404(Resume, user=request.user)
    
    if request.method == 'POST':
        form = CertificationForm(request.POST, instance=certification)
        if form.is_valid():
            form.save()
            return redirect('my_resume')
    else:
        form = CertificationForm(instance=certification)
    return render(request, 'edit.html', {'form': form,'resume': resume })

#ADD New Object
@login_required
def add_education(request):
    if not request.user.is_seeker:  
        return HttpResponseForbidden("Access restricted.")
    
    resume = Resume.objects.get(user=request.user)  
    if request.method == 'POST':
        form = EducationForm(request.POST)
        if form.is_valid():
            education = form.save(commit=False)
            education.resume = resume  
            education.save()
            return redirect('my_resume')  
    else:
        form = EducationForm()
    return render(request, 'edit.html', {'form': form}) 

@login_required
def add_employment(request):
    if not request.user.is_seeker:  
        return HttpResponseForbidden("Access restricted.")
    
    resume = Resume.objects.get(user=request.user)
    if request.method == 'POST':
        form = EmploymentForm(request.POST)
        if form.is_valid():
            employment = form.save(commit=False)
            employment.resume = resume
            employment.save()
            return redirect('my_resume')
    else:
        form = EmploymentForm()
    return render(request, 'edit.html', {'form': form}) 

@login_required
def add_skill(request):
    if not request.user.is_seeker:  
        return HttpResponseForbidden("Access restricted.")
    
    resume = Resume.objects.get(user=request.user)
    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.resume = resume
            skill.save()
            return redirect('my_resume')
    else:
        form = SkillForm()
    return render(request, 'edit.html', {'form': form}) 


@login_required
def add_project(request):
    if not request.user.is_seeker:  
        return HttpResponseForbidden("Access restricted.")
    
    resume = Resume.objects.get(user=request.user)
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.resume = resume
            project.save()
            return redirect('my_resume')
    else:
        form = ProjectForm()
    return render(request, 'edit.html', {'form': form}) 


@login_required
def add_certification(request):
    if not request.user.is_seeker:  
        return HttpResponseForbidden("Access restricted.")
    
    resume = Resume.objects.get(user=request.user)
    if request.method == 'POST':
        form = CertificationForm(request.POST)
        if form.is_valid():
            certification = form.save(commit=False)
            certification.resume = resume
            certification.save()
            return redirect('my_resume')
    else:
        form = CertificationForm()
    return render(request, 'edit.html', {'form': form})  


#upload resume
@login_required
def upload_resume(request):
    if not request.user.is_seeker:  
        return HttpResponseForbidden("Access restricted.")
    
    resume = get_object_or_404(Resume, user=request.user)
    profile = SeekerProfile.objects.get(user=request.user)
    
    if request.method == "POST":
        form = SeekerProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('view_profile') 

    else:
        form = SeekerProfileForm(instance=profile)

    return render(request, 'upload_resume.html', {'form': form, 'resume': resume })





@login_required
def view_profile(request):
    if not request.user.is_seeker:  
        return HttpResponseForbidden("Access restricted.")
    
    
    if request.user.is_seeker:
        profile = get_object_or_404(SeekerProfile, user=request.user)
        resume = get_object_or_404(Resume, user=request.user)
        age = None
        if resume.date_of_birth:
            today = date.today()
            age = today.year - resume.date_of_birth.year - (
                (today.month, today.day) < (resume.date_of_birth.month, resume.date_of_birth.day)
            )

        # Fetch related data
        educations = resume.educations.all().order_by('-id')
        employments = resume.employments.all().order_by('-id')
        skills = resume.skills.all().order_by('-id')
        projects = resume.projects.all().order_by('-id')
        certifications = resume.certifications.all().order_by('-id')
        total_years_of_experience = sum([employment.duration() for employment in employments])

        
        
        template = 'seeker-detail.html'
    else:
        return redirect('home')
    
    context = {
            'profile': profile,
            'resume': resume,
            'educations': educations,
            'employments': employments,
            'skills': skills,
            'projects': projects,
            'certifications': certifications,
            'age': age,
            'total_years_of_experience': total_years_of_experience,
        }
    
    return render(request, template, context)


@login_required
def edit_profile(request):
    """Edit profile based on the user's role."""

    if request.user.is_seeker:
        profile = get_object_or_404(SeekerProfile, user=request.user)
        form_class = SeekerProfileForm
        template = 'edit_profile.html'
    else:
        return redirect('home')
    
    if request.method == 'POST':
        form = form_class(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('view_profile')
    else:
        form = form_class(instance=profile)
    
    return render(request, template, {'form': form}) 


#Personal data's views


def edit_personal_details(request, resume_id):
    resume = get_object_or_404(Resume, id=resume_id)
    data = {
        "name": resume.name,
        "title": resume.title,
        "date_of_birth": resume.date_of_birth.strftime('%Y-%m-%d') if resume.date_of_birth else "",
        "permanent_address": resume.permanent_address,
        "gender": resume.gender,
        "email": resume.email,
        "phone_number": resume.phone_number,
        
        "area_pin_code": resume.area_pin_code,
        "marital_status": resume.marital_status,
        "hometown": resume.hometown,
        "languages": resume.languages,
    }
    return JsonResponse(data) 

def update_personal_details(request, resume_id):
    resume = get_object_or_404(Resume, id=resume_id)

    if request.method == "POST":
        form = PersonalDetailsForm(request.POST, instance=resume)
        if form.is_valid():
            form.save()
            messages.success(request, "Personal details updated successfully!")  # Success message
            return redirect("my_resume")  # Redirect to 'my_resume' page
        else:
            messages.error(request, "Error updating details. Please check your inputs.")  # Error message

    return redirect("my_resume") 


@login_required
def dashboard(request):
    if not request.user.is_seeker:  
        return HttpResponseForbidden("Access restricted.")
    
    resume = get_object_or_404(Resume, user=request.user)
    profile = SeekerProfile.objects.get(user=request.user)
    applications = JobApplication.objects.filter(seeker=profile).order_by('-applied_at')
    total_applications = applications.count()
    total_jobs = JobPost.objects.count()
    
    one_month_ago = timezone.now() - timezone.timedelta(days=30)
    last_month_applications = applications.filter(applied_at__gte=one_month_ago).count()
    last_month_jobs = JobPost.objects.filter(created_at__gte=one_month_ago).count()
    
    

    return render(request, 'dashboard.html', {
        'resume': resume,
        'profile': profile,
        'applications': applications, 
        'total_applications': total_applications,
        'total_jobs': total_jobs,
        'last_month_applications': last_month_applications,
        'last_month_jobs': last_month_jobs
    }) 
    
    
    
    
import openai  
from django.shortcuts import render
from .models import Resume, Skill
from jobboard.models import JobPost
from django.contrib.auth.decorators import login_required

@login_required
def job_recommendations(request):
    user_resume = Resume.objects.filter(user=request.user).prefetch_related('skills', 'educations', 'employments').first()

    if not user_resume:
        return render(request, 'jobs/recommendations.html', {'message': 'Please complete your resume first.'})

    # Extracting user skills
    user_skills = set(user_resume.skills.values_list('skill_name', flat=True))
    # Extracting user's experience in years
    total_experience = sum(emp.duration() for emp in user_resume.employments.all()) 
    # Fetching all jobs
    all_jobs = JobPost.objects.filter(status='published').prefetch_related('job_category')
    
    # Scoring jobs based on skills, experience, and job type match
    job_scores = []
    for job in all_jobs:
        
        # Handle job requirements gracefully
        job_requirements = set(job.job_requirements.split(',')) if job.job_requirements else set()
        skill_match_score = len(user_skills.intersection(job_requirements))

        # Handle experience parsing gracefully
        experience_match = 0
        if job.experience_required:  # Check if experience_required is not None or empty
            try:
                required_experience = int(job.experience_required.split()[0])  # Extract the first number if present
                experience_match = 1 if required_experience <= total_experience else 0
            except (ValueError, IndexError):
                experience_match = 0  # If parsing fails, consider it a match
        else:
            experience_match = 0  # Match if no experience is specified

        # Handling NoneType for job_type and user_resume.job_type
        user_job_type = user_resume.desired_industry.name.lower() if user_resume.desired_industry else ""
        
        job_type_match = 1 if user_job_type and user_job_type in (job.job_category.name.lower() if job.job_category and job.job_category.name else "") else 0
        
        # Calculating final score
        total_score = skill_match_score * 3 + experience_match * 2 + job_type_match * 2
        job_scores.append((job, total_score))

    # Sorting jobs by highest score
    sorted_jobs = sorted(job_scores, key=lambda x: x[1], reverse=True)

    # Sending data to template with top 5 job recommendations
    return render(request, 'recommendations.html', {'jobs': [job[0] for job in sorted_jobs[:5]]})
