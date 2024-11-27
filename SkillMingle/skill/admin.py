from django.contrib import admin
from .models import Category, CustomUser, Job

# Customize CategoryAdmin
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'job_count')  # Display name and job count in the admin list view
    search_fields = ('name',)  # Add a search bar for category name

    def job_count(self, obj):
        return obj.jobs.count()  # Display the number of jobs in this category
    job_count.short_description = 'Job Count'  # Optional: column header for job count

# Customize JobAdmin
class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'company_name', 'location', 'positions', 'employment_type', 'salary', 'category')
    search_fields = ('title', 'company_name', 'location')
    list_filter = ('employment_type', 'category')  # Filters for job type and category

# Register models with custom admin configurations
admin.site.register(Category, CategoryAdmin)
admin.site.register(Job, JobAdmin)

# Register CustomUserAdmin
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'usertype', 'is_approved')
    list_filter = ('usertype', 'is_approved')
    actions = ['approve_recruiters']

    def approve_recruiters(self, request, queryset):
        count = queryset.filter(usertype='recruiter').update(is_approved=True)
        self.message_user(request, f"{count} recruiters approved.")
    approve_recruiters.short_description = "Approve selected recruiters"

admin.site.register(CustomUser, CustomUserAdmin)
