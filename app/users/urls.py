from django.urls import path
from app.users import views

app_name = 'users'

urlpatterns = [
    path('register/', views.CustomRegisterView.as_view(), name="register"),
    path('login/', views.CustomLoginView.as_view(), name="login"),
    path('logout/', views.CustomLogoutView.as_view(), name="logout"),
]
