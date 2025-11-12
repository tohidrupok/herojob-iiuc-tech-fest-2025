from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('seeker', 'Job Seeker'),
        ('employer', 'Employer'),
        ('manager', 'Manager'),
        
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='seeker')
    is_verified = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)

    #related_name 
    groups = models.ManyToManyField(
        Group,
        related_name="customuser_set",
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="customuser_permissions", 
        blank=True,
    ) 
    
    @property
    def is_seeker(self):
        return self.role == 'seeker'

    @property
    def is_employer(self):
        return self.role == 'employer'
    
    @property
    def is_manager(self):
        return self.role == 'manager' 


class SeekerProfile(models.Model):
    user = models.OneToOneField(
        'CustomUser', on_delete=models.CASCADE, related_name='seeker_profile'
    )
    bio = models.TextField(blank=True, verbose_name="Biography")
    resume = models.FileField(upload_to='media/resumes/', blank=True, verbose_name="Resume")
    skills = models.TextField(blank=True, verbose_name="Skills")
    
    # Personal Info 
    name = models.CharField(max_length=255, blank=True, verbose_name="Full Name")  
    professional_title = models.CharField(max_length=255, blank=True, verbose_name="Professional Title")  
    
    # Salary Information
    current_salary = models.DecimalField(
        max_digits=10, decimal_places=2, default=0, blank=True, verbose_name="Current Salary"
    )
    expected_salary = models.DecimalField(
        max_digits=10, decimal_places=2, default=0, blank=True, verbose_name="Expected Salary"
    )
    
    # Contact Info
    phone = models.CharField(
        max_length=15, blank=True, verbose_name="Phone Number", help_text="Include country code (e.g., +88)"
    )  
    email_address = models.EmailField(blank=True, verbose_name="Email Address")  

    location = models.CharField(max_length=255, blank=True, verbose_name="Location")  
    image = models.ImageField(upload_to='media/seeker_logos/', blank=True, null=True, verbose_name="seeker image")
    my_resume = models.OneToOneField('seeker.Resume', on_delete=models.CASCADE, blank=True, null=True, verbose_name="Resume")
    
    def __str__(self):
        return f"{self.user.username}'s Profile"

    class Meta:
        verbose_name = "Seeker Profile"
        verbose_name_plural = "Seeker Profiles"


class EmployerProfile(models.Model):
    user = models.OneToOneField(
        'CustomUser', on_delete=models.CASCADE, related_name='employer_profile'
    )
    
    company_name = models.CharField(max_length=255, verbose_name="Company Name")
    
    # Combined location fields into a single 'location' field
    location = models.CharField(max_length=255, blank=True, verbose_name="Company Location")
    
    company_website = models.URLField(blank=True, verbose_name="Company Website")
    company_description = models.TextField(blank=True, verbose_name="Company Description")
    
    # Contact Information
    phone = models.CharField(max_length=15, blank=True, verbose_name="Phone Number", help_text="Include country code (e.g., +880)")
    email = models.EmailField(blank=True, verbose_name="Company Email")
    
    # Social Media Links (still kept separate for clarity)
    facebook_link = models.URLField(blank=True, verbose_name="Facebook Link")
    twitter_link = models.URLField(blank=True, verbose_name="Twitter Link")
    google_link = models.URLField(blank=True, verbose_name="Google Link")
    linkedin_link = models.URLField(blank=True, verbose_name="LinkedIn Link")
    
    # Company Details
    founded_date = models.DateField(null=True, blank=True, verbose_name="Founded Date")
    logo = models.ImageField(upload_to='media/company_logos/', blank=True, null=True, verbose_name="Company Logo", default='media/default/default_logo.png')
    
    
    
    def __str__(self):
        return f"{self.user.username}'s Profile"

    class Meta:
        verbose_name = "Employer Profile"
        verbose_name_plural = "Employer Profiles"
        
    def get_embed_url(self):
        """Convert YouTube URL to embed URL."""
        if self.twitter_link:
            if "watch?v=" in self.twitter_link:
                return self.twitter_link.replace("watch?v=", "embed/")
            elif "youtu.be/" in self.twitter_link:
                return self.twitter_link.replace("youtu.be/", "youtube.com/embed/")
        return None  
