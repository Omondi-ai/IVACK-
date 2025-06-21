from django.contrib import admin
from .models import Post

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'target_type', 'department', 'course', 'professor', 'created_at')
    list_filter = ('target_type', 'department', 'created_at')
    search_fields = ('title', 'content', 'author__username')
    date_hierarchy = 'created_at'
    raw_id_fields = ('author', 'professor')

admin.site.register(Post, PostAdmin)