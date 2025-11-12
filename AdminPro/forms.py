from django import forms
from accounts.models import EmployerProfile
from jobboard.models import JobPost , JobCategory


class PostJobForm(forms.ModelForm):
    class Meta:
        model = JobPost
        fields = '__all__'
        
    widgets = {
            'application_deadline': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(PostJobForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'form-control', 
                'placeholder': f'Enter {field.label}'
            }) 
            

class JobCategoryForm(forms.ModelForm):
    class Meta:
        model = JobCategory
        fields = ['name', 'description']