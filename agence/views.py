from django.shortcuts import render


def home(request):
    return render(request, 'home.html')
def base(request):
    return render(request, 'base.html')
