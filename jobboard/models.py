from django.db import models
from accounts.models import EmployerProfile, SeekerProfile
from django.urls import reverse

#Job Post
class JobCategory(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name 
    
class JobPost(models.Model):
    employee = models.ForeignKey(EmployerProfile, on_delete=models.CASCADE, related_name='job_posts')
    title = models.CharField(max_length=255)
    job_category = models.ForeignKey(JobCategory, on_delete=models.SET_NULL, null= True, blank= True, related_name='job_posts_category')
    company_industry_type = models.CharField(max_length=255, null= True, blank= True)
    no_of_vacancy = models.PositiveIntegerField(null= True, blank= True)
    application_deadline = models.DateField( null= True, blank= True)
    age_range = models.CharField(max_length=255, null= True, blank= True)
    gender = models.CharField(max_length=50, choices=[('Male', 'Male'), ('Female', 'Female'), ('Both', 'Both')], null= True, blank= True)
    contact_person = models.CharField(max_length=255, null= True, blank= True)
    experience_required = models.CharField(max_length=150, null= True, blank= True )
    cv_receive_method = models.CharField(max_length=255, null= True, blank= True, choices=[
        ('Online CV/Resume', 'Online CV/Resume'),   
        ('Email Attachment', 'Email Attachment'),
        ('Walk-in Interview', 'Walk-in Interview'),
        ('Hard Copy CV', 'Hard Copy CV'),
    ])
    job_type = models.CharField(max_length=50, null= True, blank= True, choices=[('Full Time', 'Full Time'), ('Part Time', 'Part Time'), ('Contractual', 'Contractual'), ('Internship', 'Internship')])
    job_level = models.CharField(max_length=50, null= True, blank= True, choices=[('Entry Level', 'Entry Level'), ('Mid Level', 'Mid Level'), ('Top Level', 'Top Level')])
    applicant_photo_required = models.BooleanField(default=False, null= True, blank= True)
    educational_qualification = models.TextField(null= True, blank= True)  #remove kore dibo
    others_qualification = models.TextField(null= True, blank= True)
    
    job_description = models.TextField(null= True, blank= True)
    job_responsibilities = models.TextField(null= True, blank= True)
    job_requirements = models.TextField( null= True, blank= True)
    other_benefits = models.TextField(blank=True, null=True)
    
    job_location = models.CharField(max_length=200, null= True, blank= True)
    exclusive_job = models.BooleanField(default=False, null= True, blank= True)
    created_at = models.DateTimeField(auto_now_add=True)
    salary_range = models.CharField(max_length=200, null= True, blank= True, default='Negotiable')
    STATUS_CHOICES = [
           ('pending', 'Pending'),
            ('published', 'Published'),  
            ('rejected', 'Rejected'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('job_detail', args=[str(self.id)]) 
    
    
    
#job Apply 

class JobApplication(models.Model):
    job = models.ForeignKey(JobPost, on_delete=models.CASCADE, related_name='applications')
    seeker = models.ForeignKey(SeekerProfile, on_delete=models.CASCADE, related_name='applications')
    resume = models.FileField(upload_to='media/apply/resumes/', blank=True, verbose_name="Resume")  
    applied_at = models.DateTimeField(auto_now_add=True)
    expected_Salary = models.IntegerField(null=True, blank=True)

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    def save(self, *args, **kwargs):
        # If no resume is uploaded, use the seeker's profile resume
        if not self.resume and self.seeker.resume:
            self.resume = self.seeker.resume
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.seeker.user.username} applied for {self.job.title}"  
    
 
    
# class JobPost(models.Model):
#     title = models.CharField(max_length=255, db_index=True)  # Index for fast search
#     job_description = models.TextField()
#     job_requirements = models.TextField()
#     job_category = models.ForeignKey(JobCategory, on_delete=models.SET_NULL, null=True, db_index=True)
#     created_at = models.DateTimeField(auto_now_add=True, db_index=True)  # Index for sorting



class BlogCategory(models.Model): 
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name

class BlogPost(models.Model): 
    title = models.CharField(max_length=200)
    writer_name = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateField(auto_now_add=True)
    published = models.BooleanField(default=False)
    categories = models.ManyToManyField(BlogCategory, blank=True)
    image = models.ImageField(upload_to='media/blog_images/', blank=True, null=True , default='media/default/blog.jpg')

    def __str__(self): 
        return self.title   
    
    @classmethod
    def get_recent(cls, count=5):
        return cls.objects.filter(published=True).order_by('-created_at')[:count]
