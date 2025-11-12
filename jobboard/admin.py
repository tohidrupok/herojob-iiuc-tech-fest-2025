from django.contrib import admin
from .models import JobPost, JobApplication, JobCategory, BlogPost, BlogCategory


admin.site.register(JobPost)
admin.site.register(JobApplication)
admin.site.register(JobCategory)
admin.site.register(BlogCategory)
admin.site.register(BlogPost)
