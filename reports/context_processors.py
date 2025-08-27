from .models import StaffReport

def report_counters(request):
    """
    Provides total report count and counts by report type
    for templates (if user is authenticated and is staff).
    """
    if request.user.is_authenticated and request.user.role == "staff":
        total_reports = StaffReport.objects.filter(staff=request.user).count()
        daily_count = StaffReport.objects.filter(staff=request.user, report_type="daily").count()
        weekly_count = StaffReport.objects.filter(staff=request.user, report_type="weekly").count()
        monthly_count = StaffReport.objects.filter(staff=request.user, report_type="monthly").count()
    else:
        total_reports = daily_count = weekly_count = monthly_count = 0

    return {
        "report_total_count": total_reports,
        "report_daily_count": daily_count,
        "report_weekly_count": weekly_count,
        "report_monthly_count": monthly_count,
    }
