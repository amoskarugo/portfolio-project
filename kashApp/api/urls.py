from django.urls import path

from .  import views
from app.views import CreateUser, login

urlpatterns = [
    path('', views.getdata),
    path('sign-up/', CreateUser),
    path('login/', login)
]