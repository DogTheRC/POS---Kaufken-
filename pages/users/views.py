from django.shortcuts import redirect, render
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.sessions.models import Session
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .models import Visitor
# Create your views here.
def register_view(request):
    if request.method == "POST": 
        form = UserCreationForm(request.POST) 
        if form.is_valid(): 
            login(request, form.save())
            return redirect("/")
    else:
        form = UserCreationForm()
    return render(request, "users/register.html", { "form": form })

def login_view(request):
    if request.method == "POST": 
        form = AuthenticationForm(data=request.POST) 
        if form.is_valid(): 
            user = form.get_user()
            login(request, form.get_user())
            
                        # Verifica si el usuario ya tiene una sesión activa
            if hasattr(user, 'visitor'):
                # Si existe, eliminamos la sesión anterior
                if Session.objects.filter(session_key=user.visitor.session_key).exists():
                    old_session = Session.objects.get(session_key=user.visitor.session_key)
                    old_session.delete()

                # Eliminar el objeto Visitor anterior
                user.visitor.delete()

            # Realiza el inicio de sesión
            login(request, user)

            # Guarda la nueva sesión en el modelo Visitor
            new_session_key = request.session.session_key
            Visitor.objects.create(target_user=user, session_key=new_session_key)

            
            return redirect("/")
    else:
        form = AuthenticationForm()
    return render(request, "users/login.html", { "form": form })

@login_required(login_url="users:login") # Añade esta decoración a las vistas que requieren estar logueados
def logout_view(request):
    if request.method == "POST":
        if hasattr(request.user, 'visitor'):
            request.user.visitor.delete()
        logout(request)  # Cierra la sesión del usuario
        return redirect('users:login')  # Redirige a la página de inicio de sesión
    return render(request, 'users:login')  # En caso de acceso directo, redirige