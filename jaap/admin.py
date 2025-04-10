from django.contrib import admin
from .models import JaapSession, JaapCount

@admin.register(JaapSession)
class JaapSessionAdmin(admin.ModelAdmin):
    list_display = ('user', 'ram_count', 'timer_set', 'target_count', 'status', 'created_at', 'completed_at')
    list_filter = ('status', 'created_at', 'timer_set')
    search_fields = ('user__username', 'user__email')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('User Information', {
            'fields': ('user',)
        }),
        ('Jaap Details', {
            'fields': ('ram_count', 'timer_set', 'target_count', 'status')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'completed_at')
        }),
    )

@admin.register(JaapCount)
class JaapCountAdmin(admin.ModelAdmin):
    list_display = ('id', 'total_count', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')
    
    def has_add_permission(self, request):
        # Only allow one instance of JaapCount
        if self.model.objects.exists():
            return False
        return super().has_add_permission(request)
