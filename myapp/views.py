from django.shortcuts import render,HttpResponse


def index(request):
    return render(request,'index.html')

def about(request):
    return render(request,'about.html')

def service(request):
    return render(request,'service.html')

def menu(request):
    return render(request,'menu.html')