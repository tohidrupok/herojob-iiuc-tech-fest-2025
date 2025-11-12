from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, JsonResponse
from .forms import SeekerRegistrationForm, EmployerRegistrationForm, CustomLoginForm, ManagerRegistrationForm, EmployerProfileForm
from .models import CustomUser, EmployerProfile, SeekerProfile



def register(request):
    seeker_form = SeekerRegistrationForm()
    employer_form = EmployerRegistrationForm()
    
    if request.method == 'POST':
        
        if 'seeker_submit' in request.POST:
            
            seeker_form = SeekerRegistrationForm(request.POST)
            if seeker_form.is_valid():
                print("seeker Form is valid") 
                user = seeker_form.save(commit=False)
                user.role = 'seeker'
                user.save()
                login(request, user)
                return redirect('seeker_dashboard')
            else:
                print("candidate Form is not valid so go raw candidate reg") 
    
                return render(request, 'registration/register_seeker.html', {'form': seeker_form})
                
        elif 'employer_submit' in request.POST:   
            employer_form = EmployerRegistrationForm(request.POST)
            if employer_form.is_valid():
                
                user = employer_form.save(commit=False)
                user.role = 'employer'
                user.is_approved = False
                user.save()
                return render(request, 'registration/pending_approval.html')
            else:
                print("employee Form is not valid so go raw employee reg") 
                return render(request, 'registration/register_employer.html', {'form': employer_form})
                         

    return redirect('home') 

   
def register_seeker(request):
    
    if request.method == 'POST':
        form = SeekerRegistrationForm(request.POST)
        if form.is_valid():
            print("Form is valid") 
            user = form.save(commit=False)
            user.role = 'seeker'
            user.save()
            login(request, user)  
            return redirect('seeker_dashboard')
    else:
        form = SeekerRegistrationForm()
    return render(request, 'registration/register_seeker.html', {'form': form})

def register_employer(request):
    if request.method == 'POST':
        form = EmployerRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = 'employer'
            user.is_approved = False  
            user.save()
            return render(request, 'registration/pending_approval.html')
    else:
        form = EmployerRegistrationForm()
    return render(request, 'registration/register_employer.html', {'form': form})

def register_manager(request):
    if request.method == 'POST':
        form = ManagerRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = 'manager'
            user.is_approved = False  
            user.save()
            return render(request, 'manager/pending_approval.html')
    else:
        form = ManagerRegistrationForm()
    return render(request, 'manager/register_manager.html', {'form': form}) 


def custom_login(request):
    if request.method == 'POST':
        form = CustomLoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                if user.is_manager and not user.is_approved:
                    return render(request, 'registration/pending_approval.html')
                if user.is_manager:
                    return redirect('superuser_dashboard')
                elif user.is_employer:
                    return redirect('manage-job')
                elif user.is_seeker:
                    return redirect('job_list')
    else:
        form = CustomLoginForm()
    return render(request, 'registration/login.html', {'form': form})

@login_required
def custom_logout(request):
    logout(request)
    return redirect('home')

# Dashboards
@login_required
def seeker_dashboard(request):
    if not request.user.is_seeker:  
        return HttpResponseForbidden("Access restricted to job seekers.")
    return render(request, 'seeker/dashboard.html')



@login_required
def manager_dashboard(request):
    if not request.user.is_manager:
        return HttpResponseForbidden("Access restricted to managers.")
    if not request.user.is_approved:
        return render(request, 'registration/pending_approval.html')
    return render(request, 'manager/dashboard.html')  







#####################
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test

def employee_required(view_func):
    @user_passes_test(lambda u: u.is_authenticated and u.is_manager)
    def wrapper(request, *args, **kwargs):
        return view_func(request, *args, **kwargs)
    return wrapper

@login_required
@employee_required
def approve_manager_list(request):
    """List all pending manager approval requests."""
    pending_managers = CustomUser.objects.filter(role='employer', is_approved=False)
    print(pending_managers)
    return render(request, 'manager/approve_manager_list.html', {'pending_managers': pending_managers})


from django.views.decorators.csrf import csrf_exempt
@csrf_exempt  
def approve_manager(request, user_id):
    if request.method == "POST":
        action = request.POST.get("action")
        try:
            user = CustomUser.objects.get(id=user_id)
            if action == "approve":
                user.is_approved = True
            else:
                user.is_approved = False
            user.save()
            return JsonResponse({"success": True})
        except user.DoesNotExist:
            return JsonResponse({"success": False, "error": "User not found"})
    return JsonResponse({"success": False, "error": "Invalid request"}, status=400)

@login_required
def view_profile(request):
    """View profile based on the user's role."""
    if request.user.is_employer:
        profile = get_object_or_404(EmployerProfile, user=request.user)
        template = 'view_profile.html'
    elif request.user.is_seeker:
        profile = get_object_or_404(SeekerProfile, user=request.user)
        template = 'view_profile.html'
    else:
        return redirect('home')
    
    return render(request, template, {'profile': profile})

@login_required
def edit_profile(request):
    """Edit profile based on the user's role."""
    if request.user.is_employer:
        profile = get_object_or_404(EmployerProfile, user=request.user)
        form_class = EmployerProfileForm
        template = 'edit_profile.html'
    # elif request.user.is_seeker:
    #     profile = get_object_or_404(SeekerProfile, user=request.user)
    #     form_class = SeekerProfileForm
    #     template = 'edit_profile.html'
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


#password reset and change password

from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView, PasswordChangeView, PasswordChangeDoneView
from django.urls import reverse_lazy

# Password Reset Views
class CustomPasswordResetView(PasswordResetView):
    template_name = 'custom_auth/password_reset_form.html'
    email_template_name = 'custom_auth/password_reset_email.html'
    success_url = reverse_lazy('password_reset_done')

class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'custom_auth/password_reset_done.html'

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'custom_auth/password_reset_confirm.html'
    success_url = reverse_lazy('password_reset_complete')

class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'custom_auth/password_reset_complete.html'

# Password Change Views (For logged-in users)
class CustomPasswordChangeView(PasswordChangeView):
    template_name = 'custom_auth/password_change_form.html'
    success_url = reverse_lazy('password_change_done')

class CustomPasswordChangeDoneView(PasswordChangeDoneView):
    template_name = 'custom_auth/password_change_done.html'
