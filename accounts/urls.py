from django.urls import path
from django.contrib.auth.views import LogoutView

from . import views

urlpatterns = [
    path('login/', views.BankSwiftLoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('profile/', views.profile_view, name='profile'),
]
