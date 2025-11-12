from django.urls import path
from . import views

urlpatterns = [
    
    path('profile/', views.view_employer_profile, name='employer_profile'), 
    path('employer/profile/<int:user_id>/', views.view_employer_profile, name='employer_profile_with_id'),
    
    # path('dashboard/', views.employer_dashboard, name='employer_dashboard'),
    path('core/profile/edit/', views.employer_profile, name='employer_profile_edit'),
    path('create-job/', views.create_job, name='create_job'),
    path('manage-job/', views.manage_job, name='manage-job'),
    path('delete-job/<int:job_id>/', views.delete_job, name='delete_job'),
    path('job/<int:job_id>/applicants/', views.job_applicants, name='job_applicants'),
    path('candidate/profile/<int:user_id>/', views.view_profile, name='view_profile_public'),
    
]



