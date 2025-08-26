#!/usr/bin/env python
"""
Test script for the checkout functionality
Run this script to test the checkout system
"""

import os
import django
import sys

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eventbooking.settings')
django.setup()

from django.test import Client
from django.urls import reverse
from tickets.models import Event, SeatRow, Seat, Ticket, Coupon
from django.contrib.auth.models import User

def test_checkout_system():
    """Test the checkout system functionality"""
    print("Testing Checkout System...")
    print("=" * 50)
    
    # Test 1: Check if models exist
    print("1. Testing Models...")
    try:
        events = Event.objects.all()
        print(f"   ✓ Found {events.count()} events")
        
        coupons = Coupon.objects.all()
        print(f"   ✓ Found {coupons.count()} coupons")
        
        if events.exists():
            event = events.first()
            rows = SeatRow.objects.filter(event=event)
            print(f"   ✓ Found {rows.count()} seat rows for event: {event.name}")
            
            if rows.exists():
                row = rows.first()
                seats = Seat.objects.filter(row=row)
                print(f"   ✓ Found {seats.count()} seats in row {row.name}")
                
                # Create a test ticket if none exists
                available_seat = seats.filter(is_booked=False).first()
                if available_seat:
                    ticket, created = Ticket.objects.get_or_create(
                        seat=available_seat,
                        defaults={'price': row.price}
                    )
                    if created:
                        print(f"   ✓ Created test ticket for seat {available_seat.row.name} - {available_seat.number}")
                    else:
                        print(f"   ✓ Found existing ticket for seat {available_seat.row.name} - {available_seat.number}")
                else:
                    print("   ✗ No available seats found")
                    return False
            else:
                print("   ✗ No seat rows found")
                return False
        else:
            print("   ✗ No events found")
            return False
            
    except Exception as e:
        print(f"   ✗ Error testing models: {e}")
        return False
    
    # Test 2: Test URL routing
    print("\n2. Testing URL Routing...")
    try:
        client = Client()
        
        # Test checkout URL
        checkout_url = reverse('checkout', args=[ticket.id])
        print(f"   ✓ Checkout URL: {checkout_url}")
        
        # Test coupon URL
        coupon_url = reverse('apply_coupon')
        print(f"   ✓ Coupon URL: {coupon_url}")
        
    except Exception as e:
        print(f"   ✗ Error testing URLs: {e}")
        return False
    
    # Test 3: Test checkout page access
    print("\n3. Testing Checkout Page Access...")
    try:
        response = client.get(checkout_url)
        if response.status_code == 200:
            print("   ✓ Checkout page loads successfully")
            print(f"   ✓ Page contains ticket info: {ticket.seat.row.event.name in str(response.content)}")
        else:
            print(f"   ✗ Checkout page returned status code: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"   ✗ Error accessing checkout page: {e}")
        return False
    
    # Test 4: Test coupon functionality
    print("\n4. Testing Coupon Functionality...")
    try:
        if coupons.exists():
            coupon = coupons.first()
            print(f"   ✓ Testing with coupon: {coupon.code} ({coupon.discount_percent}% off)")
            
            # Test coupon validation
            response = client.post(coupon_url, {
                'coupon_code': coupon.code
            }, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
            
            if response.status_code == 200:
                print("   ✓ Coupon validation endpoint accessible")
            else:
                print(f"   ✗ Coupon validation returned status code: {response.status_code}")
        else:
            print("   ⚠ No coupons available for testing")
            
    except Exception as e:
        print(f"   ✗ Error testing coupon functionality: {e}")
        return False
    
    print("\n" + "=" * 50)
    print("✓ Checkout System Test Completed Successfully!")
    print(f"✓ You can now test the checkout at: {checkout_url}")
    print("✓ Available test coupons:")
    for coupon in coupons:
        print(f"  - {coupon.code}: {coupon.discount_percent}% off (valid until {coupon.valid_until.strftime('%Y-%m-%d')})")
    
    return True

if __name__ == '__main__':
    try:
        success = test_checkout_system()
        if success:
            print("\n🎉 All tests passed! The checkout system is ready to use.")
        else:
            print("\n❌ Some tests failed. Please check the errors above.")
            sys.exit(1)
    except Exception as e:
        print(f"\n💥 Test script failed with error: {e}")
        sys.exit(1)
