from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import StaffReport
from django.contrib import messages

@login_required
def staff_reports(request):
    if request.user.role != "staff":
        return redirect("index")  # only staff can see this

    reports = StaffReport.objects.filter(staff=request.user)
    context = {
        "header_name": 'My Reports',
        "reports": reports,
    }
    return render(request, "reports/my_reports.html", context)


@login_required
def add_report(request):
    if request.user.role != "staff":
        return redirect("home")

    if request.method == "POST":
        report_type = request.POST.get("report_type")
        title = request.POST.get("title")
        description = request.POST.get("description")

        StaffReport.objects.create(
            staff=request.user,
            group=request.user.staff_groups.first(),  # assign staff’s first group
            report_type=report_type,
            title=title,
            description=description,
        )
        messages.success(request, 'Report Added Successfully!!')
        return redirect("reports:my_reports")

    return render(request, "reports/add_report.html")
