from django.contrib import admin
from .models import Thread, Message
from django.utils.html import format_html
# Add to the top of admin.py
from django.urls import reverse
from django.utils.safestring import mark_safe

# Then add this method to ThreadAdmin
def view_on_site(self, obj):
    url = reverse('thread_detail', kwargs={'thread_id': obj.id})
    return mark_safe(f'<a href="{url}">View in App</a>')
view_on_site.short_description = "View in App"

class MessageAdmin(admin.ModelAdmin):
    # ...
    list_select_related = ('sender', 'thread')
    raw_id_fields = ('sender',)
    show_full_result_count = False
    actions = ['mark_as_read', 'mark_as_unread']
    
    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)
    mark_as_read.short_description = "Mark selected messages as read"
    
    def mark_as_unread(self, request, queryset):
        queryset.update(is_read=False)
    mark_as_unread.short_description = "Mark selected messages as unread"
class MessageInline(admin.TabularInline):
    model = Message
    extra = 1
    readonly_fields = ('preview_attachment',)
    fields = ('sender', 'text', 'attachment', 'preview_attachment', 'created', 'is_read')
    
    def preview_attachment(self, obj):
        if obj.attachment:
            if obj.is_image():
                return format_html('<img src="{}" style="max-height: 100px; max-width: 100px;" />', obj.attachment.url)
            else:
                return format_html('<a href="{}">Download File</a>', obj.attachment.url)
        return "-"
    preview_attachment.short_description = "Preview"

@admin.register(Thread)
class ThreadAdmin(admin.ModelAdmin):
    list_display = ('id', 'created', 'updated', 'participants_list')
    list_filter = ('created', 'updated')
    search_fields = ('participants__username',)
    filter_horizontal = ('participants',)
    inlines = [MessageInline]
    
    def participants_list(self, obj):
        return ", ".join([user.username for user in obj.participants.all()])
    participants_list.short_description = "Participants"

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'thread', 'sender', 'short_text', 'attachment_preview', 'created', 'is_read')
    list_filter = ('is_read', 'created', 'sender')
    search_fields = ('text', 'sender__username')
    readonly_fields = ('preview_attachment',)
    fieldsets = (
        (None, {
            'fields': ('thread', 'sender', 'is_read')
        }),
        ('Content', {
            'fields': ('text', 'attachment', 'preview_attachment')
        }),
        ('Metadata', {
            'fields': ('created',),
            'classes': ('collapse',)
        })
    )
    
    def short_text(self, obj):
        return obj.text[:50] + "..." if len(obj.text) > 50 else obj.text
    short_text.short_description = "Text"
    
    def attachment_preview(self, obj):
        if obj.attachment:
            if obj.is_image():
                return format_html('<img src="{}" style="max-height: 50px; max-width: 50px;" />', obj.attachment.url)
            else:
                return format_html('<a href="{}">{}</a>', obj.attachment.url, obj.attachment.name.split('/')[-1])
        return "-"
    attachment_preview.short_description = "Attachment"
    
    def preview_attachment(self, obj):
        if obj.attachment:
            if obj.is_image():
                return format_html('<img src="{}" style="max-height: 200px; max-width: 200px;" />', obj.attachment.url)
            else:
                return format_html('<a href="{}" class="button">{}</a>', obj.attachment.url, obj.attachment.name.split('/')[-1])
        return "-"
    preview_attachment.short_description = "Detailed Preview"