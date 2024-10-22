from django.db import models
from django.utils import timezone

class ScanResult(models.Model):
    url = models.URLField(max_length=200)
    ip_address = models.CharField(max_length=50, null=True, blank=True)
    grade = models.CharField(max_length=2)
    headers = models.TextField()
    scan_time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.url} - {self.grade} - {self.scan_time}"
