from django.urls import path
from .views import CustomPasswordResetView, CustomPasswordResetDoneView, CustomPasswordResetConfirmView, CustomPasswordResetCompleteView, CustomPasswordChangeView, CustomPasswordChangeDoneView
from . import views

urlpatterns = [    

    path('login/', views.custom_login, name='custom_login'),
    path('logout/', views.custom_logout, name='custom_logout'),
    
    path('register/seeker/', views.register_seeker, name='register_seeker'),
    path('register/employer/', views.register_employer, name='register_employer'),
    path('register/manager/', views.register_manager, name='register_manager'),
    
    path('profile/view/', views.view_profile, name='view_profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),

    path('dashboard/seeker/', views.seeker_dashboard, name='seeker_dashboard'),

    path('dashboard/manager/', views.manager_dashboard, name='manager_dashboard'),
    

    path('employee/approve-managers/', views.approve_manager_list, name='approve_manager_list'),
    path('employee/approve-managers/<int:user_id>/', views.approve_manager, name='approve_manager'),
  
       
    path('register/', views.register, name='register'),
    
    #after registation pass reset, change system 
    
    # Password Reset URLs
    path('password_reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),

    # Custom Password Change URLs (For logged-in users)
    path('password_change/', CustomPasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', CustomPasswordChangeDoneView.as_view(), name='password_change_done'),
    
    
    
    
]

# <a href="{% url 'password_reset' %}">Forgot Password?</a>
# <a href="{% url 'password_change' %}">Change Password</a>

