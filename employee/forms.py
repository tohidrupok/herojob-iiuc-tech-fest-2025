from django import forms
from accounts.models import EmployerProfile
from jobboard.models import JobPost

class EmployerProfileForm(forms.ModelForm):
    class Meta:
        model = EmployerProfile
        fields = [
            "company_name",
            "location",
            "company_website",
            "company_description",
            "phone",
            "email",
            "facebook_link",
            "twitter_link",
            "google_link",
            "linkedin_link",
            "founded_date",
            "logo",
        ]
        widgets = {
            # Use a date picker for the founded date field
            'founded_date': forms.DateInput(attrs={'type': 'date'}),
        } 
        
    logo = forms.ImageField(required=False, widget=forms.ClearableFileInput(attrs={'class': 'form-control'}))


class JobPostForm(forms.ModelForm):
    class Meta:
        model = JobPost
        exclude = ['employee', 'status']  
        
    widgets = {
            'application_deadline': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(JobPostForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'form-control', 
                'placeholder': f'Enter {field.label}'
            }) 
            
            