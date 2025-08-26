from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import StaffReport
from .forms import StaffReportForm

@login_required
def staff_reports(request):
    if request.user.role != "staff":
        return redirect("home")  # only staff can write reports

    reports = StaffReport.objects.filter(staff=request.user)

    return render(request, "reports/my_reports.html", {"reports": reports})


@login_required
def add_report(request):
    if request.user.role != "staff":
        return redirect("index")

    if request.method == "POST":
        form = StaffReportForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.staff = request.user
            report.group = request.user.staff_groups.first()  # assign staff's first group
            report.save()
            return redirect("reports:my_reports")
    else:
        form = StaffReportForm()

    return render(request, "reports/add_report.html", {"form": form})
