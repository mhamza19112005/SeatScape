from django.urls import path
from . import views

urlpatterns = [
    # Main home page - accessible to everyone
    path('', views.HomePage, name='home'),
    # Authentication pages
    path('auth/', views.AuthPage, name='auth'),
    path('login/', views.AuthPage, name='login'),
    path('signup/', views.AuthPage, name='signup'),
    path('logout/', views.LogoutPage, name='logout'),
    path('forget-password/', views.forget_password, name='forget_password'),
    path('reset-password/<str:uidb64>/<str:token>/', views.reset_password, name='reset_password'),
]
