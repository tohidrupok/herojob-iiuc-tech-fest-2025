from django.urls import path
from .views import (
    job_list, job_detail, apply_job, employee_applications, about_us, contact_us, home, blog_list, blog_detail, learing_list, learning_tip_detail
)

urlpatterns = [
    path('', home, name='home'),
    path('all-jobs/', job_list, name='job_list'),
    path('jobs/<int:job_id>/', job_detail, name='job_detail'),
    
    path('jobs/<int:job_id>/apply/', apply_job, name='apply_job'),
    path('applications/', employee_applications, name='employee_applications'),
    path('jobs/<int:job_id>/apply/', apply_job, name='apply_job'),
    
    
    path('about/',  about_us, name='about_us'),
    path('contact/', contact_us, name='contact_us'), 
    
    path('blogs/', blog_list, name='home_blog_list'),
    path('blogs/<int:post_id>/', blog_detail, name='home_blog_detail'),

    path('learning/tips/', learing_list, name='learning_list'),
    path('learning/tips/<int:id>/', learning_tip_detail, name='learning_tip_detail'),

    
]
