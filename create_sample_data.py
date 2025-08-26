import os
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eventbooking.settings')
django.setup()

from django.contrib.auth.models import User
from tickets.models import Event, SeatRow, Seat, Ticket, Coupon
from datetime import datetime, timedelta

# Create a sample user
user, created = User.objects.get_or_create(
    username='testuser',
    defaults={
        'email': 'test@example.com',
        'first_name': 'Test',
        'last_name': 'User'
    }
)

if created:
    user.set_password('testpass123')
    user.save()
    print("Created test user: testuser / testpass123")

# Create a sample event
event, created = Event.objects.get_or_create(
    name='Concert at Central Park',
    defaults={
        'date': datetime.now() + timedelta(days=30),
        'location': 'Central Park Amphitheater',
        'description': 'An amazing outdoor concert featuring top artists.'
    }
)

if created:
    print(f"Created event: {event.name}")

# Create sample seat rows
rows_data = [
    {'name': 'Row A', 'capacity': 20, 'price': 50.00},
    {'name': 'Row B', 'capacity': 25, 'price': 45.00},
    {'name': 'Row C', 'capacity': 30, 'price': 40.00},
    {'name': 'Row D', 'capacity': 25, 'price': 35.00},
    {'name': 'Row E', 'capacity': 20, 'price': 30.00},
]

for row_data in rows_data:
    row, created = SeatRow.objects.get_or_create(
        event=event,
        name=row_data['name'],
        defaults={
            'capacity': row_data['capacity'],
            'price': row_data['price']
        }
    )
    
    if created:
        print(f"Created seat row: {row.name}")

# Create seats for each row (this is automatically done by the SeatRow save method)
print("Seats automatically created for each row")

# Create some sample tickets
seats = Seat.objects.filter(row__event=event)
for i, seat in enumerate(seats):
    # Book every 5th seat as an example
    if i % 5 == 0:
        seat.is_booked = True
        seat.save()
        
        ticket, created = Ticket.objects.get_or_create(
            seat=seat,
            defaults={
                'user': user,
                'price': seat.row.price
            }
        )
        
        if created:
            print(f"Booked ticket for seat: {seat.row.name} - Seat {seat.number}")

# Create sample coupons
coupons_data = [
    {'code': 'WELCOME10', 'discount_percent': 10, 'valid_until': datetime.now() + timedelta(days=30)},
    {'code': 'SAVE20', 'discount_percent': 20, 'valid_until': datetime.now() + timedelta(days=60)},
    {'code': 'SPECIAL15', 'discount_percent': 15, 'valid_until': datetime.now() + timedelta(days=45)},
]

for coupon_data in coupons_data:
    coupon, created = Coupon.objects.get_or_create(
        code=coupon_data['code'],
        defaults={
            'discount_percent': coupon_data['discount_percent'],
            'valid_until': coupon_data['valid_until']
        }
    )
    
    if created:
        print(f"Created coupon: {coupon.code} ({coupon.discount_percent}% off)")

print("Sample data creation completed!")
print("You can now access the site at http://127.0.0.1:8000/")
print("Admin interface: http://127.0.0.1:8000/admin/")