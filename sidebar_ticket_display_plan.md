# Right Sidebar Ticket Display Plan

## Overview

The right sidebar will display tickets for the event with the following features:
1. Show all tickets by default
2. Filter tickets by row when a row is selected
3. Visual indicators for ticket status (available/booked)
4. Responsive design that works on different screen sizes

## HTML Structure

```html
<div class="sidebar">
    <div class="sidebar-header">
        <h2>Tickets</h2>
        <div class="ticket-summary">
            <span class="available-count">Available: 0</span>
            <span class="booked-count">Booked: 0</span>
        </div>
    </div>
    
    <div class="ticket-filters">
        <input type="text" id="ticket-search" placeholder="Search tickets...">
        <select id="ticket-sort">
            <option value="row">Sort by Row</option>
            <option value="price">Sort by Price</option>
            <option value="status">Sort by Status</option>
        </select>
    </div>
    
    <div id="tickets-container" class="tickets-container">
        <!-- Tickets will be dynamically inserted here -->
        <div class="ticket-item" data-row-id="1" data-seat-number="5" data-ticket-status="available">
            <div class="ticket-header">
                <h4>Row A - Seat 5</h4>
                <span class="ticket-price">$25.00</span>
            </div>
            <div class="ticket-details">
                <span class="ticket-status available">Available</span>
                <button class="book-ticket-btn" data-ticket-id="1">Book Now</button>
            </div>
        </div>
        
        <div class="ticket-item" data-row-id="1" data-seat-number="6" data-ticket-status="booked">
            <div class="ticket-header">
                <h4>Row A - Seat 6</h4>
                <span class="ticket-price">$25.00</span>
            </div>
            <div class="ticket-details">
                <span class="ticket-status booked">Booked</span>
                <button class="book-ticket-btn disabled" data-ticket-id="2" disabled>Booked</button>
            </div>
        </div>
    </div>
    
    <div class="no-tickets-message" style="display: none;">
        <p>No tickets found matching your criteria.</p>
    </div>
</div>
```

## CSS Styling

```css
.sidebar {
    flex: 1;
    padding: 20px;
    border-left: 1px solid #e0e0e0;
    background-color: #f8f9fa;
    overflow-y: auto;
    min-width: 300px;
}

.sidebar-header {
    margin-bottom: 20px;
    padding-bottom: 15px;
    border-bottom: 1px solid #e0e0e0;
}

.sidebar-header h2 {
    margin: 0 0 10px 0;
    color: #333;
    font-size: 24px;
}

.ticket-summary {
    display: flex;
    gap: 15px;
}

.ticket-summary span {
    padding: 5px 10px;
    border-radius: 20px;
    font-size: 14px;
    font-weight: 500;
}

.available-count {
    background-color: #d4edda;
    color: #155724;
}

.booked-count {
    background-color: #f8d7da;
    color: #721c24;
}

.ticket-filters {
    display: flex;
    gap: 10px;
    margin-bottom: 20px;
    flex-wrap: wrap;
}

.ticket-filters input,
.ticket-filters select {
    padding: 8px 12px;
    border: 1px solid #ced4da;
    border-radius: 4px;
    font-size: 14px;
}

.ticket-filters input {
    flex: 1;
    min-width: 150px;
}

.tickets-container {
    display: flex;
    flex-direction: column;
    gap: 15px;
}

.ticket-item {
    background: white;
    border: 1px solid #e0e0e0;
    border-radius: 8px;
    padding: 15px;
    transition: all 0.3s ease;
    box-shadow: 0 2px 4px rgba(0,0,0,0.05);
}

.ticket-item:hover {
    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    transform: translateY(-2px);
}

.ticket-item.filtered {
    display: none;
}

.ticket-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 10px;
}

.ticket-header h4 {
    margin: 0;
    color: #333;
    font-size: 18px;
}

.ticket-price {
    font-weight: bold;
    color: #007bff;
    font-size: 16px;
}

.ticket-details {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.ticket-status {
    padding: 4px 10px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 500;
}

.ticket-status.available {
    background-color: #d4edda;
    color: #155724;
}

.ticket-status.booked {
    background-color: #f8d7da;
    color: #721c24;
}

.book-ticket-btn {
    padding: 6px 12px;
    background-color: #007bff;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-size: 14px;
    transition: background-color 0.2s;
}

.book-ticket-btn:hover:not(.disabled) {
    background-color: #0056b3;
}

.book-ticket-btn.disabled {
    background-color: #6c757d;
    cursor: not-allowed;
}

.no-tickets-message {
    text-align: center;
    padding: 40px 20px;
    color: #6c757d;
}

.no-tickets-message p {
    margin: 0;
    font-size: 16px;
}
```

## JavaScript Functionality

```javascript
function initializeSidebar() {
    // Initialize ticket counters
    updateTicketCounters();
    
    // Initialize search functionality
    initializeTicketSearch();
    
    // Initialize sorting functionality
    initializeTicketSorting();
    
    // Initialize booking buttons
    initializeBookingButtons();
}

function updateTicketCounters() {
    const tickets = document.querySelectorAll('.ticket-item');
    let availableCount = 0;
    let bookedCount = 0;
    
    tickets.forEach(ticket => {
        const status = ticket.getAttribute('data-ticket-status');
        if (status === 'available') {
            availableCount++;
        } else if (status === 'booked') {
            bookedCount++;
        }
    });
    
    // Update counter displays
    document.querySelector('.available-count').textContent = `Available: ${availableCount}`;
    document.querySelector('.booked-count').textContent = `Booked: ${bookedCount}`;
}

function initializeTicketSearch() {
    const searchInput = document.getElementById('ticket-search');
    
    searchInput.addEventListener('input', function() {
        const searchTerm = this.value.toLowerCase();
        const tickets = document.querySelectorAll('.ticket-item');
        
        tickets.forEach(ticket => {
            const rowName = ticket.querySelector('h4').textContent.toLowerCase();
            const seatNumber = ticket.getAttribute('data-seat-number');
            
            if (rowName.includes(searchTerm) || seatNumber.includes(searchTerm)) {
                ticket.style.display = 'block';
            } else {
                ticket.style.display = 'none';
            }
        });
        
        // Update no tickets message
        updateNoTicketsMessage();
    });
}

function initializeTicketSorting() {
    const sortSelect = document.getElementById('ticket-sort');
    
    sortSelect.addEventListener('change', function() {
        const sortBy = this.value;
        const ticketsContainer = document.getElementById('tickets-container');
        const tickets = Array.from(document.querySelectorAll('.ticket-item'));
        
        tickets.sort((a, b) => {
            switch (sortBy) {
                case 'row':
                    const rowA = a.querySelector('h4').textContent;
                    const rowB = b.querySelector('h4').textContent;
                    return rowA.localeCompare(rowB);
                    
                case 'price':
                    const priceA = parseFloat(a.querySelector('.ticket-price').textContent.replace('$', ''));
                    const priceB = parseFloat(b.querySelector('.ticket-price').textContent.replace('$', ''));
                    return priceB - priceA;
                    
                case 'status':
                    const statusA = a.getAttribute('data-ticket-status');
                    const statusB = b.getAttribute('data-ticket-status');
                    return statusA.localeCompare(statusB);
                    
                default:
                    return 0;
            }
        });
        
        // Re-append sorted tickets
        tickets.forEach(ticket => {
            ticketsContainer.appendChild(ticket);
        });
    });
}

function initializeBookingButtons() {
    const bookButtons = document.querySelectorAll('.book-ticket-btn:not(.disabled)');
    
    bookButtons.forEach(button => {
        button.addEventListener('click', function() {
            const ticketId = this.getAttribute('data-ticket-id');
            bookTicket(ticketId);
        });
    });
}

function bookTicket(ticketId) {
    // In a real implementation, this would make an AJAX call to book the ticket
    console.log(`Booking ticket ${ticketId}`);
    
    // Show confirmation message
    alert(`Ticket ${ticketId} booked successfully!`);
    
    // Update UI to reflect booking
    const ticketElement = document.querySelector(`.book-ticket-btn[data-ticket-id="${ticketId}"]`).closest('.ticket-item');
    ticketElement.setAttribute('data-ticket-status', 'booked');
    ticketElement.querySelector('.ticket-status').className = 'ticket-status booked';
    ticketElement.querySelector('.ticket-status').textContent = 'Booked';
    ticketElement.querySelector('.book-ticket-btn').className = 'book-ticket-btn disabled';
    ticketElement.querySelector('.book-ticket-btn').textContent = 'Booked';
    ticketElement.querySelector('.book-ticket-btn').disabled = true;
    
    // Update counters
    updateTicketCounters();
}

function filterTicketsByRow(rowId) {
    const tickets = document.querySelectorAll('.ticket-item');
    let visibleTickets = 0;
    
    tickets.forEach(ticket => {
        const ticketRowId = ticket.getAttribute('data-row-id');
        
        if (rowId === 'all' || ticketRowId === rowId) {
            ticket.style.display = 'block';
            ticket.classList.remove('filtered');
            visibleTickets++;
        } else {
            ticket.style.display = 'none';
            ticket.classList.add('filtered');
        }
    });
    
    // Update no tickets message
    updateNoTicketsMessage();
    
    // Update ticket counters
    updateTicketCounters();
}

function showAllTickets() {
    const tickets = document.querySelectorAll('.ticket-item');
    
    tickets.forEach(ticket => {
        ticket.style.display = 'block';
        ticket.classList.remove('filtered');
    });
    
    // Update no tickets message
    updateNoTicketsMessage();
    
    // Update ticket counters
    updateTicketCounters();
}

function updateNoTicketsMessage() {
    const visibleTickets = document.querySelectorAll('.ticket-item:not([style*="display: none"]):not(.filtered)');
    const noTicketsMessage = document.querySelector('.no-tickets-message');
    
    if (visibleTickets.length === 0) {
        noTicketsMessage.style.display = 'block';
    } else {
        noTicketsMessage.style.display = 'none';
    }
}

// Initialize sidebar when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    initializeSidebar();
});
```

## Integration with Seat Selection

The sidebar needs to integrate with the seat selection functionality:

```javascript
// In the seat selection code, add this to the row click handler
function selectRow(rowElement) {
    // ... existing selection code ...
    
    // Filter tickets in sidebar
    const rowId = rowElement.getAttribute('data-row-id');
    filterTicketsByRow(rowId);
}

function deselectRow(rowElement) {
    // ... existing deselection code ...
    
    // Show all tickets in sidebar
    showAllTickets();
}
```

## Responsive Design Considerations

```css
@media (max-width: 768px) {
    .container {
        flex-direction: column;
    }
    
    .sidebar {
        border-left: none;
        border-top: 1px solid #e0e0e0;
        min-width: auto;
    }
    
    .ticket-filters {
        flex-direction: column;
    }
    
    .ticket-filters input,
    .ticket-filters select {
        width: 100%;
    }
}
```

## Data Requirements from Backend

The backend needs to provide the following data for each ticket:
1. Ticket ID
2. Row ID
3. Seat number
4. Ticket price
5. Booking status (available/booked)
6. Row name for display

This data structure allows the frontend to:
- Display tickets in the sidebar
- Filter tickets by row
- Show ticket status
- Enable/disable booking buttons
- Update UI when tickets are booked