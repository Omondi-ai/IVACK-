from django.contrib import admin
from .models import Assessment, Result

class ResultInline(admin.TabularInline):
    model = Result
    extra = 1
    raw_id_fields = ('student',)

class AssessmentAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'assessment_type', 'date_given', 'max_score')
    list_filter = ('assessment_type', 'course__department', 'date_given')
    search_fields = ('title', 'course__name')
    inlines = [ResultInline]
    date_hierarchy = 'date_given'

class ResultAdmin(admin.ModelAdmin):
    list_display = ('student', 'assessment', 'score', 'grade')
    list_filter = ('assessment__course', 'assessment__assessment_type')
    search_fields = ('student__username', 'assessment__title')
    raw_id_fields = ('student', 'assessment')

admin.site.register(Assessment, AssessmentAdmin)
admin.site.register(Result, ResultAdmin)