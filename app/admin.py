from django.contrib import admin
from .models import Profile, Attendance, Document, AuditLog



@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'cpf', 'phone')
    list_filter = ('role',)
    search_fields = ('user__username', 'cpf')


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'time', 'is_present')
    list_filter = ('date', 'is_present')
    search_fields = ('user__username',)


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'uploaded_at')
    list_filter = ('uploaded_at',)
    search_fields = ('title', 'user__username')


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'model_name', 'object_id', 'action', 'timestamp')
    list_filter = ('model_name', 'action', 'timestamp')
    search_fields = ('user__username', 'model_name')
