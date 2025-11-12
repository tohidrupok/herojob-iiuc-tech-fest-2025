from django import forms
from .models import JobApplication, JobPost, BlogPost

class JobPostForm(forms.ModelForm):
    class Meta:
        model = JobPost
        fields = '__all__'

class JobApplicationForm(forms.ModelForm):
    class Meta:
        model = JobApplication
        fields = ['resume', 'expected_Salary']

    def __init__(self, *args, seeker=None, **kwargs):
        super().__init__(*args, **kwargs)
        if seeker and seeker.resume:
            self.fields['resume'].initial = seeker.resume

    def clean_expected_Salary(self):
        expected_Salary = self.cleaned_data.get('expected_Salary')

        if expected_Salary is not None and expected_Salary < 1001:
            raise forms.ValidationError("If provided, expected salary must be greater than 1000.")

        return expected_Salary 
    
    
class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'writer_name', 'content', 'published', 'categories', 'image']