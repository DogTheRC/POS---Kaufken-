from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

@login_required(login_url="users:login")
def homepage(request):
    return render(request, 'home.html')
    #return HttpResponse('Hello World')
@login_required(login_url="users:login")
def view_navbar(request): 
    return render(request, 'base.html')  

# Vista basada en clase (CBV) protegida con LoginRequiredMixin
class IndexView(LoginRequiredMixin, TemplateView):
    template_name = "home.html"  # Define el template que quieres usar