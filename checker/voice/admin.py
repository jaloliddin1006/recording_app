from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Audio


@admin.register(Audio)
class AudioAdmin(admin.ModelAdmin):
    list_display = ( 'sentence', 'audio_tag', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('sentence', )
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')

    def audio_tag(self, obj):
        return mark_safe(f'<audio controls src="{obj.file_path.url}"></audio>')
    
    audio_tag.short_description = 'Audio'


    def delete_queryset(self, request, queryset):
        for q in queryset:
            q.file_path.delete()
        queryset.delete()
    
    def delete_model(self, request, obj):
        obj.file_path.delete()
        obj.delete()
    
