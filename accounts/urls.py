from django.urls import path
from . import views

urlpatterns = [
    # unified page; keep legacy names working
    path('', views.AuthPage, name='auth'),
    path('login/', views.AuthPage, name='login'),
    path('signup/', views.AuthPage, name='signup'),
    path('home/', views.HomePage, name='home'),
    path('logout/', views.LogoutPage, name='logout'),
    path('forget-password/', views.forget_password, name='forget_password'),
    path('reset-password/<str:uidb64>/<str:token>/', views.reset_password, name='reset_password'),
]
