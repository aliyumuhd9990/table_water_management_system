from django.db import models
from accounts.models import CustomUser, StaffGroup

class StaffReport(models.Model):
    REPORT_TYPE_CHOICES = (
        ('daily', 'Daily Report'),
        ('weekly', 'Weekly Report'),
        ('monthly', 'Monthly Report'),
    )

    staff = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="staff_reports")
    group = models.ForeignKey(StaffGroup, on_delete=models.SET_NULL, null=True, blank=True, related_name="group_reports")
    report_type = models.CharField(max_length=10, choices=REPORT_TYPE_CHOICES, default="daily")
    title = models.CharField(max_length=200)
    description = models.TextField(help_text="Write what you worked on today/this week/month")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.staff.full_name} ({self.group}) - {self.report_type} Report"
