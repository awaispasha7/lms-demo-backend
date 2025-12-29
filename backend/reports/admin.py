from django.contrib import admin
from .models import Report, ReportTemplate


@admin.register(ReportTemplate)
class ReportTemplateAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'report_type', 'is_active', 'created_at']
    list_filter = ['report_type', 'is_active']
    search_fields = ['name']


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'report_type', 'generated_by', 'generated_at']
    list_filter = ['report_type', 'generated_at']
    search_fields = ['title']

