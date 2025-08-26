from django.urls import path
from . import views

urlpatterns = [
    # unified page remains available
    path('auth/', views.AuthPage, name='auth'),
    # dedicated auth pages
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('about/', views.about, name='about'),
    path('', views.HomePage, name='home'),
    path('logout/', views.LogoutPage, name='logout'),
    path('forget-password/', views.forget_password, name='forget_password'),
    path('reset-password/<str:uidb64>/<str:token>/', views.reset_password, name='reset_password'),
]
