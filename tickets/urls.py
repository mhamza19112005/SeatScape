from django.urls import path
from . import views

urlpatterns = [
    path('', views.event_list, name='event_list'),
    path('<int:event_id>/', views.event_detail, name='event_detail'),
    path('checkout/<int:ticket_id>/', views.checkout, name='checkout'),
    path('apply-coupon/', views.apply_coupon, name='apply_coupon'),
    path('booking-confirmation/<int:payment_id>/', views.booking_confirmation, name='booking_confirmation'),
]
