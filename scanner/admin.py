from django.contrib import admin
from .models import ScanResult

@admin.register(ScanResult)
class ScanResultAdmin(admin.ModelAdmin):
    list_display = ('url', 'ip_address', 'grade', 'scan_time')
