from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Application

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'role', 'department', 'is_staff', 'is_active')
    list_filter = ('role', 'department', 'is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('email', 'profile_picture', 'phone_number')}),
        ('Academic info', {'fields': ('role', 'department', 'student_id')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'role', 'department'),
        }),
    )
    search_fields = ('username', 'email', 'student_id')
    ordering = ('username',)

class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'intended_department', 'application_date')
    list_filter = ('intended_department', 'application_date')
    search_fields = ('full_name', 'email')
    date_hierarchy = 'application_date'

admin.site.register(User, CustomUserAdmin)
admin.site.register(Application, ApplicationAdmin)