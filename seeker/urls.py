from django.urls import path
from . import views

urlpatterns = [
    path('resumes/', views.all_resumes, name='view_resume'),
    path('my-resume/', views.my_resume, name='my_resume'),
    path('resume/<int:resume_id>/', views.resume_detail, name='resume_detail'),
    # path('application/', views.application, name = "application"
    # path('application/list', views.application_list, name = "appliapplication_listcation"
    # path('profile/edit/', views.seeker_profile, name='seeker_profile_edit'),
    
    path('edit/resume/', views.edit_resume, name='edit_resume'),
    path('edit/education/<int:pk>/', views.edit_education, name='edit_education'),
    path('education/delete/<int:pk>/', views.delete_education, name='delete_education'),
    path('edit/employment/<int:pk>/', views.edit_employment, name='edit_employment'),
    path('employment/delete/<int:pk>/', views.delete_employment, name='delete_employment'),
    path('edit/skill/<int:pk>/', views.edit_skill, name='edit_skill'),
    path('skill/delete/<int:pk>/', views.delete_skill, name='delete_skill'),
    path('edit/project/<int:pk>/', views.edit_project, name='edit_project'),
    path('project/delete/<int:pk>/', views.delete_project, name='delete_project'),
    path('edit/certification/<int:pk>/', views.edit_certification, name='edit_certification'), 
    path('certification/delete/<int:pk>/', views.delete_certification, name='delete_certification'),
    
    
    path('add/education/', views.add_education, name='add_education'), 
    path('add/employment/', views.add_employment, name='add_employment'),
    path('add/skill/', views.add_skill, name='add_skill'),
    path('add/project/', views.add_project, name='add_project'),
    path('add/certification/', views.add_certification, name='add_certification'), 
    path('upload-resume/', views.upload_resume, name='upload_resume'),
    

    
    path('profile/view/', views.view_profile, name='view_profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    
    
    path('resume/edit/<int:resume_id>/', views.edit_personal_details, name='edit_personal_details'),
    path('resume/update/<int:resume_id>/', views.update_personal_details, name='update_personal_details'),
    
    path('dashboard/', views.dashboard, name='dashboard'),
    path('recommendations/', views.job_recommendations, name='recommendations'),
    
]



