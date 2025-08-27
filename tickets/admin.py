from django.contrib import admin
from .models import Event, SeatRow, Seat, Ticket, Coupon, Payment, Category

admin.site.register(Event)
admin.site.register(Category)
admin.site.register(SeatRow)
admin.site.register(Seat)
admin.site.register(Ticket)
admin.site.register(Coupon)
admin.site.register(Payment)
