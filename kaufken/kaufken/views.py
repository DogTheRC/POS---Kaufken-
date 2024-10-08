from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required(login_url="users:login")
def homepage(request):
    return render(request, 'home.html')
    #return HttpResponse('Hello World')
@login_required(login_url="users:login")
def view_navbar(request): 
    return render(request, 'base.html')  