from django.contrib import admin
from .models import CustomUser, SeekerProfile, EmployerProfile

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role', 'is_approved')
    list_filter = ('role', 'is_approved')

    def approve_employers(self, request, queryset):
        queryset.update(is_approved=True)
    approve_employers.short_description = "Approve selected employers"

    actions = [approve_employers]

admin.site.register(SeekerProfile)
admin.site.register(EmployerProfile)