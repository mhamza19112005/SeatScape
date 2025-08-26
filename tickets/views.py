from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.db import transaction
from decimal import Decimal
from .models import Event, SeatRow, Seat, Ticket, Payment, Coupon
from .forms import ContactDetailsForm, PaymentForm, CouponForm

def event_list(request):
    events = Event.objects.all()
    return render(request, 'event_list.html', {'events': events})


def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    # Get all seat rows for this event with annotated seat counts
    rows = SeatRow.objects.filter(event=event).prefetch_related('seats').order_by('name')
    
    # Annotate rows with available and booked seat counts
    from django.db.models import Count, Q
    rows = rows.annotate(
        available_seats=Count('seats', filter=Q(seats__is_booked=False)),
        booked_seats=Count('seats', filter=Q(seats__is_booked=True))
    )
    
    # Add position information to rows
    rows_with_positions = []
    for i, row in enumerate(rows):
        row_data = {
            'row': row,
            'x_position': i * 120,
            'text_x_position': (i * 120) + 50
        }
        rows_with_positions.append(row_data)
    
    # Get all seats for this event through rows
    seats = Seat.objects.filter(row__event=event).select_related('row').order_by('row__name', 'number')
    
    # Get all tickets for this event
    tickets = Ticket.objects.filter(seat__row__event=event).select_related('seat', 'seat__row')
    
    return render(request, 'event_detail.html', {
        'event': event,
        'rows_with_positions': rows_with_positions,
        'seats': seats,
        'tickets': tickets,
    })


def checkout(request, ticket_id):
    # Get the ticket
    ticket = get_object_or_404(Ticket, id=ticket_id)
    
    # Check if ticket is already booked
    if ticket.seat.is_booked:
        messages.error(request, 'This ticket is already booked.')
        return redirect('event_detail', event_id=ticket.seat.row.event.id)
    
    # Initialize forms
    contact_form = ContactDetailsForm()
    payment_form = PaymentForm()
    coupon_form = CouponForm()
    
    # Calculate initial amounts
    subtotal = ticket.price
    discount_amount = Decimal('0.00')
    tax_amount = subtotal * Decimal('0.15')  # 15% tax
    total_amount = subtotal + tax_amount - discount_amount
    
    # Store ticket info in session for processing
    request.session['checkout_ticket_id'] = ticket_id
    request.session['checkout_subtotal'] = float(subtotal)
    request.session['checkout_tax_amount'] = float(tax_amount)
    request.session['checkout_discount_amount'] = float(discount_amount)
    request.session['checkout_total_amount'] = float(total_amount)
    
    # Handle coupon validation via AJAX
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest' and request.method == 'POST':
        coupon_form = CouponForm(request.POST)
        if coupon_form.is_valid():
            try:
                coupon = Coupon.objects.get(code=coupon_form.cleaned_data['coupon_code'].upper())
                if coupon.valid_until > timezone.now():
                    discount_amount = (subtotal * Decimal(coupon.discount_percent)) / Decimal('100')
                    total_amount = subtotal + tax_amount - discount_amount
                    
                    # Update session
                    request.session['checkout_discount_amount'] = float(discount_amount)
                    request.session['checkout_total_amount'] = float(total_amount)
                    
                    return JsonResponse({
                        'success': True,
                        'discount_amount': float(discount_amount),
                        'total_amount': float(total_amount),
                        'discount_percent': coupon.discount_percent
                    })
                else:
                    return JsonResponse({'success': False, 'error': 'Coupon has expired.'})
            except Coupon.DoesNotExist:
                return JsonResponse({'success': False, 'error': 'Invalid coupon code.'})
        else:
            return JsonResponse({'success': False, 'error': 'Invalid coupon code.'})
    
    # Handle form submission
    if request.method == 'POST':
        contact_form = ContactDetailsForm(request.POST)
        payment_form = PaymentForm(request.POST)
        
        if contact_form.is_valid() and payment_form.is_valid():
            try:
                with transaction.atomic():
                    # Mark seat as booked
                    ticket.seat.is_booked = True
                    ticket.seat.save()
                    
                    # Update ticket with user (if user is logged in)
                    if request.user.is_authenticated:
                        ticket.user = request.user
                        ticket.save()
                    
                    # Create payment record
                    payment = Payment.objects.create(
                        user=request.user if request.user.is_authenticated else None,
                        amount=request.session.get('checkout_total_amount', float(total_amount)),
                        status='completed'
                    )
                    payment.tickets.add(ticket)
                    
                    # Store contact details in session for confirmation
                    request.session['checkout_contact'] = {
                        'full_name': contact_form.cleaned_data['full_name'],
                        'email': contact_form.cleaned_data['email'],
                        'phone': contact_form.cleaned_data['phone']
                    }
                    
                    # Clear checkout session data
                    for key in ['checkout_ticket_id', 'checkout_subtotal', 'checkout_tax_amount', 
                               'checkout_discount_amount', 'checkout_total_amount']:
                        request.session.pop(key, None)
                    
                    messages.success(request, 'Ticket booked successfully!')
                    return redirect('booking_confirmation', payment_id=payment.id)
                    
            except Exception as e:
                messages.error(request, f'An error occurred during checkout: {str(e)}')
                return redirect('event_detail', event_id=ticket.seat.row.event.id)
    
    # Get event details for display
    event = ticket.seat.row.event
    
    return render(request, 'checkout.html', {
        'ticket': ticket,
        'event': event,
        'contact_form': contact_form,
        'payment_form': payment_form,
        'coupon_form': coupon_form,
        'subtotal': subtotal,
        'tax_amount': tax_amount,
        'discount_amount': discount_amount,
        'total_amount': total_amount,
    })


def booking_confirmation(request, payment_id):
    payment = get_object_or_404(Payment, id=payment_id)
    return render(request, 'booking_confirmation.html', {
        'payment': payment,
    })

def apply_coupon(request):
    """AJAX view for applying coupon codes"""
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        coupon_form = CouponForm(request.POST)
        if coupon_form.is_valid():
            try:
                coupon = Coupon.objects.get(code=coupon_form.cleaned_data['coupon_code'].upper())
                if coupon.valid_until > timezone.now():
                    # Get ticket info from session
                    subtotal = Decimal(str(request.session.get('checkout_subtotal', 0)))
                    tax_amount = Decimal(str(request.session.get('checkout_tax_amount', 0)))
                    
                    discount_amount = (subtotal * Decimal(coupon.discount_percent)) / Decimal('100')
                    total_amount = subtotal + tax_amount - discount_amount
                    
                    # Update session
                    request.session['checkout_discount_amount'] = float(discount_amount)
                    request.session['checkout_total_amount'] = float(total_amount)
                    
                    return JsonResponse({
                        'success': True,
                        'discount_amount': float(discount_amount),
                        'total_amount': float(total_amount),
                        'discount_percent': coupon.discount_percent,
                        'message': f'Coupon applied! {coupon.discount_percent}% discount added.'
                    })
                else:
                    return JsonResponse({'success': False, 'error': 'Coupon has expired.'})
            except Coupon.DoesNotExist:
                return JsonResponse({'success': False, 'error': 'Invalid coupon code.'})
        else:
            return JsonResponse({'success': False, 'error': 'Invalid coupon code.'})
    
    return JsonResponse({'success': False, 'error': 'Invalid request method.'})