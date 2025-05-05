from django.contrib import admin
from .models import Department, Course

class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'theme_color')
    list_filter = ('theme_color',)
    search_fields = ('name', 'code')
    prepopulated_fields = {'code': ('name',)}

class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'department')
    list_filter = ('department',)
    search_fields = ('name', 'code')
    prepopulated_fields = {'code': ('name',)}

admin.site.register(Department, DepartmentAdmin)
admin.site.register(Course, CourseAdmin)