from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import JsonResponse
from .models import Event, SeatRow, Seat, Ticket, Payment

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
    
    # Calculate total amount (in a real app, you might have additional fees)
    total_amount = ticket.price
    
    # If form is submitted
    if request.method == 'POST':
        # In a real app, you would process payment here
        # For now, we'll just mark the ticket as booked
        
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
            amount=total_amount,
            status='completed'
        )
        payment.tickets.add(ticket)
        
        messages.success(request, 'Ticket booked successfully!')
        return redirect('booking_confirmation', payment_id=payment.id)
    
    return render(request, 'checkout.html', {
        'ticket': ticket,
        'total_amount': total_amount,
    })


def booking_confirmation(request, payment_id):
    payment = get_object_or_404(Payment, id=payment_id)
    return render(request, 'booking_confirmation.html', {
        'payment': payment,
    })