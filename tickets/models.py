from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True, blank=True, null=True)

    def __str__(self):
        return self.name

class Event(models.Model):
    name = models.CharField(max_length=200)
    date = models.DateTimeField()
    location = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    # Optional image upload or external image URL
    image = models.ImageField(upload_to='events/', blank=True, null=True)
    image_url = models.URLField(blank=True, null=True)
    categories = models.ManyToManyField('Category', blank=True, related_name='events')

    def __str__(self):
        return self.name


class SeatRow(models.Model):
    event = models.ForeignKey('Event', on_delete=models.CASCADE, related_name="rows")
    name = models.CharField(max_length=50)  # e.g. "Row A"
    capacity = models.IntegerField()
    price = models.DecimalField(max_digits=8, decimal_places=2)  # Base price per seat
    svg_id = models.CharField(max_length=100, blank=True, null=True)  # For SVG mapping later

    def __str__(self):
        return f"{self.name} ({self.event.name})"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Auto-generate seats if not already created
        if not self.seats.exists():  
            for num in range(1, self.capacity + 1):
                Seat.objects.create(row=self, number=num)



class Seat(models.Model):
    row = models.ForeignKey(SeatRow, on_delete=models.CASCADE, related_name="seats")
    number = models.IntegerField()
    is_booked = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.row.name} - Seat {self.number}"


class Ticket(models.Model):
    seat = models.OneToOneField(Seat, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    booked_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return f"Ticket {self.id} - {self.seat}"


class Coupon(models.Model):
    code = models.CharField(max_length=20, unique=True)
    discount_percent = models.IntegerField()  # e.g. 10 for 10% off
    valid_until = models.DateTimeField()

    def __str__(self):
        return self.code


class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tickets = models.ManyToManyField(Ticket)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[("pending", "Pending"), ("completed", "Completed")])
    stripe_payment_id = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"Payment {self.id} - {self.user.username}"
