from django import forms
from .models import Resume, Education, Employment, Skill, Project, Certification
from accounts.models import SeekerProfile

class ResumeForm(forms.ModelForm):
    class Meta:
        model = Resume
        fields = [
            'image', 'profile_summary',
            'linkedin_profile', 'github_profile', 'portfolio_link','expected_salary', 'availability_to_join'
        ]
        widgets = {
            'availability_to_join': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }
    image = forms.ImageField(required=False, widget=forms.ClearableFileInput(attrs={'class': 'form-control'})) 
    
class PersonalDetailsForm(forms.ModelForm):
    class Meta:
        model = Resume
        fields = [
            'date_of_birth', 'gender', 'marital_status', 'languages',
            'permanent_address', 'area_pin_code', 'hometown', 'email', 'phone_number',
            'name','title'
        ]
class EducationForm(forms.ModelForm):
    class Meta:
        model = Education
        fields = ['degree', 'university', 'graduation_year', 'field_of_study']

class EmploymentForm(forms.ModelForm):
    class Meta:
        model = Employment
        fields = ['company_name', 'role', 'start_date', 'end_date', 'responsibilities']

class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = ['skill_name', 'last_used_year', 'experience_years']

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['project_name', 'project_description', 'role_in_project', 'start_date', 'end_date']

class CertificationForm(forms.ModelForm):
    class Meta:
        model = Certification
        fields = ['certification_name', 'issuing_organization', 'issue_date','certification_name_link']


class SeekerProfileForm(forms.ModelForm):
    class Meta:
        model = SeekerProfile
        fields = ['resume']
        widgets = {
            'resume': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }