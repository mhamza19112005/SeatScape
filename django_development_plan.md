# Django Event Booking System Development Plan

## Current Issues Identified

1. The `event_detail` view in `tickets/views.py` has incorrect data retrieval:
   - It's trying to filter `Seat` by `event`, but `Seat` is related to `SeatRow`, not `Event` directly
   - Missing proper data structure for SVG visualization

## Required Changes to views.py

### Fix event_detail view

```python
from django.shortcuts import render, get_object_or_404
from .models import Event, SeatRow, Seat, Ticket

def event_list(request):
    events = Event.objects.all()
    return render(request, 'event_list.html', {'events': events})


def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    # Get all seat rows for this event
    rows = SeatRow.objects.filter(event=event).prefetch_related('seats').order_by('name')
    
    # Get all seats for this event through rows
    seats = Seat.objects.filter(row__event=event).select_related('row').order_by('row__name', 'number')
    
    # Get all tickets for this event
    tickets = Ticket.objects.filter(seat__row__event=event).select_related('seat', 'seat__row')
    
    return render(request, 'event_detail.html', {
        'event': event,
        'rows': rows,
        'seats': seats,
        'tickets': tickets,
    })
```

## Template Structure for event_detail.html

The template should include:
1. Main content area with SVG seat arrangement
2. Right sidebar showing tickets
3. Interactive features:
   - Hover tooltips showing row information
   - Clicking rows filters tickets in sidebar
   - Visual feedback for selected rows

## Data Structure for Frontend

The frontend will need:
1. Event information
2. Seat rows with capacity and price
3. Seats within each row
4. Tickets for each seat (booked/unbooked status)

## JavaScript Functionality

1. Event listeners for hover and click on SVG elements
2. Dynamic updating of sidebar content when rows are selected
3. Tooltip display on hover with row information
4. Row selection highlighting

## CSS Requirements

1. Responsive layout with main content and sidebar
2. SVG styling for seats and rows
3. Visual feedback for interactive elements
4. Tooltip styling