from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser, SeekerProfile, EmployerProfile
from seeker.models import Resume

@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:  # Only run this code when a new user is created
        if instance.role == 'seeker':
            resume = Resume.objects.create(user=instance)
            SeekerProfile.objects.create(user=instance , my_resume=resume)
            
        elif instance.role == 'employer':
            EmployerProfile.objects.create(user=instance)
 
