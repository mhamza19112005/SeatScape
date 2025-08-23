# SVG Seat Arrangement Template Plan

## Template Structure

The `event_detail.html` template should have the following structure:

```html
<!DOCTYPE html>
<html>
<head>
    <title>{{ event.name }} - Seat Selection</title>
    <style>
        /* CSS styles for layout and interactivity */
        .container {
            display: flex;
            flex-direction: row;
            height: 100vh;
        }
        
        .main-content {
            flex: 3;
            padding: 20px;
            overflow: auto;
        }
        
        .sidebar {
            flex: 1;
            padding: 20px;
            border-left: 1px solid #ccc;
            background-color: #f5f5f5;
            overflow: auto;
        }
        
        .seat-row {
            cursor: pointer;
            transition: opacity 0.3s;
        }
        
        .seat-row:hover {
            opacity: 0.8;
        }
        
        .seat-row.selected {
            stroke: #007bff;
            stroke-width: 3;
        }
        
        .tooltip {
            position: absolute;
            background-color: #333;
            color: white;
            padding: 5px 10px;
            border-radius: 4px;
            font-size: 14px;
            pointer-events: none;
            z-index: 1000;
            opacity: 0;
            transition: opacity 0.3s;
        }
        
        .ticket-item {
            padding: 10px;
            margin: 5px 0;
            border: 1px solid #ddd;
            border-radius: 4px;
            background-color: white;
        }
        
        .ticket-item.booked {
            background-color: #f8d7da;
        }
        
        .ticket-item.available {
            background-color: #d4edda;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="main-content">
            <h1>{{ event.name }}</h1>
            <p>{{ event.date }} at {{ event.location }}</p>
            <p>{{ event.description }}</p>
            
            <!-- SVG Seat Arrangement -->
            <div id="svg-container">
                <svg width="100%" height="500">
                    <!-- Rows will be generated here -->
                    {% for row in rows %}
                    <rect 
                        class="seat-row" 
                        id="row-{{ row.id }}"
                        data-row-id="{{ row.id }}"
                        data-row-name="{{ row.name }}"
                        data-row-capacity="{{ row.capacity }}"
                        data-row-price="{{ row.price }}"
                        x="{{ forloop.counter0|mul:120 }}" 
                        y="50" 
                        width="100" 
                        height="50" 
                        fill="#007bff"
                        rx="5"
                    />
                    <text 
                        x="{{ forloop.counter0|mul:120|add:50 }}" 
                        y="80" 
                        text-anchor="middle" 
                        fill="white" 
                        font-family="Arial"
                    >
                        {{ row.name }}
                    </text>
                    {% endfor %}
                </svg>
            </div>
        </div>
        
        <div class="sidebar">
            <h2>Tickets</h2>
            <div id="tickets-container">
                <!-- Tickets will be displayed here -->
                {% for ticket in tickets %}
                <div class="ticket-item {% if ticket.seat.is_booked %}booked{% else %}available{% endif %}" 
                     data-row-id="{{ ticket.seat.row.id }}">
                    <h4>{{ ticket.seat.row.name }} - Seat {{ ticket.seat.number }}</h4>
                    <p>Price: ${{ ticket.price }}</p>
                    <p>Status: {% if ticket.seat.is_booked %}Booked{% else %}Available{% endif %}</p>
                </div>
                {% endfor %}
            </div>
        </div>
    </div>
    
    <div class="tooltip" id="tooltip"></div>
    
    <script>
        // JavaScript for interactivity will be added here
        document.addEventListener('DOMContentLoaded', function() {
            const tooltip = document.getElementById('tooltip');
            const seatRows = document.querySelectorAll('.seat-row');
            const ticketItems = document.querySelectorAll('.ticket-item');
            
            // Add event listeners for seat rows
            seatRows.forEach(row => {
                // Hover events for tooltip
                row.addEventListener('mouseenter', function(e) {
                    const rowName = this.getAttribute('data-row-name');
                    const capacity = this.getAttribute('data-row-capacity');
                    const price = this.getAttribute('data-row-price');
                    
                    tooltip.innerHTML = `
                        <strong>${rowName}</strong><br>
                        Capacity: ${capacity} seats<br>
                        Price: $${price} per seat
                    `;
                    
                    tooltip.style.left = (e.pageX + 10) + 'px';
                    tooltip.style.top = (e.pageY + 10) + 'px';
                    tooltip.style.opacity = '1';
                });
                
                row.addEventListener('mousemove', function(e) {
                    tooltip.style.left = (e.pageX + 10) + 'px';
                    tooltip.style.top = (e.pageY + 10) + 'px';
                });
                
                row.addEventListener('mouseleave', function() {
                    tooltip.style.opacity = '0';
                });
                
                // Click events for row selection
                row.addEventListener('click', function() {
                    const rowId = this.getAttribute('data-row-id');
                    
                    // Remove selected class from all rows
                    seatRows.forEach(r => r.classList.remove('selected'));
                    
                    // Add selected class to clicked row
                    this.classList.add('selected');
                    
                    // Filter tickets in sidebar
                    ticketItems.forEach(ticket => {
                        if (ticket.getAttribute('data-row-id') === rowId) {
                            ticket.style.display = 'block';
                        } else {
                            ticket.style.display = 'none';
                        }
                    });
                });
            });
            
            // Show all tickets by default
            document.addEventListener('click', function(e) {
                if (!e.target.closest('.seat-row')) {
                    // Remove selected class from all rows
                    seatRows.forEach(r => r.classList.remove('selected'));
                    
                    // Show all tickets
                    ticketItems.forEach(ticket => {
                        ticket.style.display = 'block';
                    });
                }
            });
        });
    </script>
</body>
</html>
```

## Key Features of the Template

1. **Responsive Layout**: Uses flexbox for a main content area and sidebar
2. **SVG Visualization**: Each row is represented as a rectangle with text label
3. **Interactive Elements**:
   - Hover effects on seat rows
   - Click selection for filtering tickets
   - Tooltips with row information
4. **Ticket Display**: Shows all tickets by default, filters by row when selected
5. **Visual Feedback**:
   - Selected row highlighting
   - Color-coded ticket status (booked vs available)
   - Smooth transitions

## Data Attributes Used

1. **Seat Rows**:
   - `data-row-id`: Unique identifier for the row
   - `data-row-name`: Name of the row (e.g., "Row A")
   - `data-row-capacity`: Number of seats in the row
   - `data-row-price`: Price per seat in the row

2. **Tickets**:
   - `data-row-id`: Links ticket to its row
   - CSS classes for status (`booked` or `available`)

## JavaScript Functionality

1. **Tooltip System**:
   - Shows row information on hover
   - Follows cursor movement
   - Smooth fade in/out

2. **Row Selection**:
   - Highlights selected row
   - Filters tickets in sidebar
   - Deselects when clicking elsewhere

3. **Ticket Filtering**:
   - Shows all tickets by default
   - Filters by row when selected
   - Resets when deselecting