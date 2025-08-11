from django.shortcuts import render, redirect


app_name = 'core_app'
# Create your views here.
def IndexView(request):
    return render(request, 'core_app/index.html')