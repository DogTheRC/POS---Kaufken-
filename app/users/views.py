from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView
from django.contrib.sessions.models import Session
from django.contrib.auth import login
from django.urls import reverse_lazy
from .models import Visitor

class CustomLoginView(LoginView):
    template_name = 'users/login.html'
    
    def form_valid(self, form):
        user = form.get_user()
        
        # Handle existing Visitor session
        if hasattr(user, 'visitor'):
            # Delete previous session if exists
            if Session.objects.filter(session_key=user.visitor.session_key).exists():
                Session.objects.get(session_key=user.visitor.session_key).delete()
            
            # Remove previous Visitor object
            user.visitor.delete()
        
        # Perform login
        response = super().form_valid(form)
        
        # Create new Visitor entry
        new_session_key = self.request.session.session_key
        Visitor.objects.create(target_user=user, session_key=new_session_key)
        
        return response

class CustomLogoutView(LogoutView):
    next_page = 'users:login'
    
    def dispatch(self, request, *args, **kwargs):
        # Delete Visitor entry if exists
        if hasattr(request.user, 'visitor'):
            request.user.visitor.delete()
        
        return super().dispatch(request, *args, **kwargs)

class CustomRegisterView(CreateView):
    form_class = UserCreationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('home')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        user = form.save()
        login(self.request, user)
        return response