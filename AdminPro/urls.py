from django.urls import path
from .views import superuser_dashboard, delete_profile, job_post_list, publish_job, reject_job, superuser_job_applicants, delete_job_application, show_all_seeker_profiles, show_all_employee_profiles, post_job ,category_page , add_employer, pending_job_post_list, blog_create, blog_update, blog_delete, blog_detail, blog_list


urlpatterns = [
    path('dashboard/', superuser_dashboard, name='superuser_dashboard'),
    path('delete-profile/<int:user_id>/', delete_profile, name='delete_profile'),
    path('jobs/', job_post_list, name='job_post_list'),
    path('jobs/approve/', pending_job_post_list, name='approve_job_post_list'),
    path('publish_job/<int:job_id>/', publish_job, name='publish_job'),
    path('reject_job/<int:job_id>/',  reject_job, name='reject_job'),
    path('job/<int:job_id>/applicants/superuser/', superuser_job_applicants, name='superuser_job_applicants'),
    path('delete_job_application/<int:application_id>/', delete_job_application, name='delete_job_application'),
    path('all-seeker-profiles/', show_all_seeker_profiles, name='all_seeker_profiles'),
    path('all-employee-profiles/', show_all_employee_profiles, name='all_employee_profiles'),
    
    path('post-job/', post_job, name='post_job'),
    
    path('categories/', category_page, name='category_page'),
    path('add/employer/', add_employer, name='add_employer'), 
    
    path('admin-blogs/', blog_list, name='blog_list'),
    path('admin-blogs/<int:post_id>/', blog_detail, name='blog_detail'),
    path('admin-blogs/create/', blog_create, name='blog_create'),
    path('admin-blogs/<int:post_id>/edit/', blog_update, name='blog_update'),
    path('admin-blogs/<int:post_id>/delete/', blog_delete, name='blog_delete')
    
]
