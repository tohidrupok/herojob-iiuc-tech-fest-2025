from django.db import models
from django.core.validators import EmailValidator
from accounts.models import CustomUser
from datetime import date
from jobboard.models import JobCategory


class Resume(models.Model):
    user = models.OneToOneField(
    'accounts.CustomUser', on_delete=models.CASCADE, related_name='resume_profile', blank=True, null=True
    )
    # Personal Details
    date_of_birth = models.DateField(blank=True, null=True)
    
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
    ]
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES, blank=True)
    
    MARITAL_STATUS_CHOICES = [
        ('Single', 'Single'),
        ('Married', 'Married'),
    ]
    marital_status = models.CharField(max_length=10, choices=MARITAL_STATUS_CHOICES, blank=True)    
    passport_number = models.CharField(max_length=20, blank=True, null=True)
    languages = models.CharField(max_length=255, blank=True)
    permanent_address = models.TextField( blank=True)
    area_pin_code = models.CharField(max_length=10, blank=True)
    hometown = models.CharField(max_length=255, blank=True)   
    email = models.EmailField( blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True)

    # Career Details
    desired_industry = models.ForeignKey(JobCategory, on_delete=models.CASCADE, related_name='job_posts', blank=True, null=True)
    desired_location = models.CharField(max_length=255, blank=True, null=True)
    functional_area = models.CharField(max_length=255, blank=True, null=True)
    
    JOB_TYPE_CHOICES = [
        ('Full Time', 'Full Time'), ('Part Time', 'Part Time'), ('Contractual', 'Contractual'), ('Internship', 'Internship')
    ]
    job_type = models.CharField(max_length=100, blank=True, choices=JOB_TYPE_CHOICES)
    
    expected_salary = models.DecimalField(max_digits=10, blank=True, decimal_places=2, default=0.0)
    availability_to_join = models.DateField( blank=True, null=True)

    # Profile Summary
    profile_summary = models.TextField(blank=True, null=True)
    

    # Links (Online Profiles)
    linkedin_profile = models.URLField(blank=True, null=True)
    github_profile = models.URLField(blank=True, null=True)
    portfolio_link = models.URLField(blank=True, null=True) 
    name = models.CharField(max_length=255, blank=True, null=True, verbose_name="Full Name")  
    title = models.CharField(max_length=255, blank=True, null=True, verbose_name="Professional Title") 
    image = models.ImageField(upload_to='media/seeker_image/', blank=True, null=True, verbose_name="Seeker Image", default='media/default/default_logo.png')
    

    def __str__(self):
        return f"Resume for {self.user}"

class Education(models.Model):
    resume = models.ForeignKey(
        'Resume', on_delete=models.CASCADE, related_name='educations'
    )
    degree = models.CharField(max_length=255, verbose_name="Degree")
    university = models.CharField(max_length=255, verbose_name="University")
    graduation_year = models.IntegerField(verbose_name="Graduation Year")
    field_of_study = models.CharField(max_length=255, blank=True, verbose_name="Field of Study")

    def __str__(self):
        return f"{self.degree} from {self.university} ({self.graduation_year})"

    class Meta:
        verbose_name = "Education"
        verbose_name_plural = "Educations" 

class Employment(models.Model):
    resume = models.ForeignKey(Resume, related_name='employments', on_delete=models.CASCADE)
    company_name = models.CharField(max_length=255)
    role = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    responsibilities = models.TextField()

    def __str__(self):
        return f"{self.role} at {self.company_name}"
    
    def duration(self):
        end = self.end_date if self.end_date else date.today()
        delta = end - self.start_date
        return delta.days // 365


class Skill(models.Model):
    resume = models.ForeignKey(Resume, related_name='skills', on_delete=models.CASCADE)
    skill_name = models.CharField(max_length=100)
    
    last_used_year = models.IntegerField()
    experience_years = models.FloatField()

    def __str__(self):
        return self.skill_name


class Project(models.Model):
    resume = models.ForeignKey(Resume, related_name='projects', on_delete=models.CASCADE)
    project_name = models.CharField(max_length=255)
    project_description = models.TextField()
    role_in_project = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.project_name


class Certification(models.Model):
    resume = models.ForeignKey(Resume, related_name='certifications', on_delete=models.CASCADE)
    certification_name = models.CharField(max_length=255)
    issuing_organization = models.CharField(max_length=255)
    issue_date = models.DateField()
    certification_name_link= models.URLField(max_length=200, blank=True, null=True)

    def __str__(self):
        return f"{self.certification_name} by {self.issuing_organization}"


