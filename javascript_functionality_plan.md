# JavaScript Functionality Plan for Interactive Seat Selection

## Overview

The JavaScript functionality will provide the following interactive features:
1. Hover tooltips showing row information
2. Click-based row selection
3. Dynamic filtering of tickets in the sidebar
4. Visual feedback for user interactions

## Event Listener Structure

```javascript
document.addEventListener('DOMContentLoaded', function() {
    // Initialize all interactive elements after DOM is loaded
    initializeSeatMap();
    initializeTooltips();
    initializeRowSelection();
    initializeTicketFiltering();
});
```

## Tooltip System

### HTML Structure
```html
<div class="tooltip" id="seat-tooltip"></div>
```

### JavaScript Implementation
```javascript
function initializeTooltips() {
    const tooltip = document.getElementById('seat-tooltip');
    const seatRows = document.querySelectorAll('.seat-row');
    
    seatRows.forEach(row => {
        // Show tooltip on mouse enter
        row.addEventListener('mouseenter', function(e) {
            const rowData = getRowData(this);
            
            tooltip.innerHTML = `
                <div class="tooltip-content">
                    <h4>${rowData.name}</h4>
                    <p>Seats: ${rowData.capacity}</p>
                    <p>Price: $${rowData.price}</p>
                    <p>Available: ${rowData.available}</p>
                </div>
            `;
            
            tooltip.style.display = 'block';
            updateTooltipPosition(e);
        });
        
        // Update tooltip position on mouse move
        row.addEventListener('mousemove', function(e) {
            updateTooltipPosition(e);
        });
        
        // Hide tooltip on mouse leave
        row.addEventListener('mouseleave', function() {
            tooltip.style.display = 'none';
        });
    });
}

function updateTooltipPosition(event) {
    const tooltip = document.getElementById('seat-tooltip');
    const tooltipWidth = tooltip.offsetWidth;
    const tooltipHeight = tooltip.offsetHeight;
    const windowWidth = window.innerWidth;
    const windowHeight = window.innerHeight;
    
    let x = event.pageX + 15;
    let y = event.pageY + 15;
    
    // Adjust position if tooltip would go off screen
    if (x + tooltipWidth > windowWidth) {
        x = event.pageX - tooltipWidth - 15;
    }
    
    if (y + tooltipHeight > windowHeight) {
        y = event.pageY - tooltipHeight - 15;
    }
    
    tooltip.style.left = x + 'px';
    tooltip.style.top = y + 'px';
}

function getRowData(rowElement) {
    return {
        id: rowElement.getAttribute('data-row-id'),
        name: rowElement.getAttribute('data-row-name'),
        capacity: rowElement.getAttribute('data-row-capacity'),
        price: rowElement.getAttribute('data-row-price'),
        available: rowElement.getAttribute('data-row-available')
    };
}
```

## Row Selection System

### JavaScript Implementation
```javascript
function initializeRowSelection() {
    const seatRows = document.querySelectorAll('.seat-row');
    
    seatRows.forEach(row => {
        row.addEventListener('click', function() {
            const rowId = this.getAttribute('data-row-id');
            
            // Toggle selection state
            if (this.classList.contains('selected')) {
                deselectRow(this);
                showAllTickets();
            } else {
                selectRow(this);
                filterTicketsByRow(rowId);
            }
        });
    });
}

function selectRow(rowElement) {
    // Remove selection from all rows
    document.querySelectorAll('.seat-row').forEach(row => {
        row.classList.remove('selected');
    });
    
    // Add selection to clicked row
    rowElement.classList.add('selected');
    
    // Add visual feedback
    rowElement.style.stroke = '#007bff';
    rowElement.style.strokeWidth = '3';
}

function deselectRow(rowElement) {
    rowElement.classList.remove('selected');
    rowElement.style.stroke = '';
    rowElement.style.strokeWidth = '';
}

function showAllTickets() {
    document.querySelectorAll('.ticket-item').forEach(ticket => {
        ticket.style.display = 'block';
    });
}
```

## Ticket Filtering System

### JavaScript Implementation
```javascript
function initializeTicketFiltering() {
    // Filter tickets when a row is selected
    document.querySelectorAll('.seat-row').forEach(row => {
        row.addEventListener('click', function() {
            const rowId = this.getAttribute('data-row-id');
            filterTicketsByRow(rowId);
        });
    });
    
    // Show all tickets when clicking outside rows
    document.addEventListener('click', function(e) {
        if (!e.target.closest('.seat-row') && !e.target.closest('.ticket-item')) {
            showAllTickets();
            deselectAllRows();
        }
    });
}

function filterTicketsByRow(rowId) {
    const tickets = document.querySelectorAll('.ticket-item');
    
    tickets.forEach(ticket => {
        const ticketRowId = ticket.getAttribute('data-row-id');
        
        if (ticketRowId === rowId) {
            ticket.style.display = 'block';
            ticket.classList.add('highlighted');
        } else {
            ticket.style.display = 'none';
            ticket.classList.remove('highlighted');
        }
    });
}

function deselectAllRows() {
    document.querySelectorAll('.seat-row').forEach(row => {
        row.classList.remove('selected');
        row.style.stroke = '';
        row.style.strokeWidth = '';
    });
}
```

## Visual Feedback Enhancements

### CSS Classes for Interactions
```css
.seat-row {
    cursor: pointer;
    transition: all 0.2s ease;
}

.seat-row:hover {
    opacity: 0.8;
    transform: scale(1.02);
}

.seat-row.selected {
    stroke: #007bff;
    stroke-width: 3;
    filter: drop-shadow(0 0 5px rgba(0, 123, 255, 0.5));
}

.ticket-item {
    transition: all 0.3s ease;
}

.ticket-item.highlighted {
    background-color: #e6f7ff;
    border-left: 4px solid #007bff;
    transform: translateX(5px);
}

.tooltip {
    position: absolute;
    background: rgba(0, 0, 0, 0.9);
    color: white;
    padding: 10px;
    border-radius: 6px;
    font-size: 14px;
    pointer-events: none;
    z-index: 1000;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    backdrop-filter: blur(4px);
    transition: opacity 0.2s ease;
}

.tooltip h4 {
    margin: 0 0 5px 0;
    color: #fff;
}

.tooltip p {
    margin: 2px 0;
    font-size: 13px;
    color: #ccc;
}
```

## Complete Initialization Function

```javascript
function initializeSeatMap() {
    // Initialize all interactive features
    initializeTooltips();
    initializeRowSelection();
    initializeTicketFiltering();
    
    // Add keyboard navigation support
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') {
            showAllTickets();
            deselectAllRows();
        }
    });
    
    // Add touch support for mobile devices
    const seatRows = document.querySelectorAll('.seat-row');
    
    seatRows.forEach(row => {
        // Touch events for mobile
        let touchStartTime;
        
        row.addEventListener('touchstart', function() {
            touchStartTime = new Date().getTime();
        });
        
        row.addEventListener('touchend', function(e) {
            const touchEndTime = new Date().getTime();
            const touchDuration = touchEndTime - touchStartTime;
            
            // Treat long press (500ms+) as hover
            if (touchDuration > 500) {
                // Simulate hover for tooltip
                const mouseEnterEvent = new MouseEvent('mouseenter', {
                    view: window,
                    bubbles: true,
                    cancelable: true
                });
                this.dispatchEvent(mouseEnterEvent);
                
                // Hide tooltip after delay
                setTimeout(() => {
                    const mouseLeaveEvent = new MouseEvent('mouseleave', {
                        view: window,
                        bubbles: true,
                        cancelable: true
                    });
                    this.dispatchEvent(mouseLeaveEvent);
                }, 2000);
            } else {
                // Treat as click
                this.click();
            }
        });
    });
}
```

## Data Structure for Frontend

The JavaScript will work with the following data attributes on HTML elements:

1. **Seat Rows**:
   - `data-row-id`: Unique identifier
   - `data-row-name`: Row name (e.g., "Row A")
   - `data-row-capacity`: Total seats in row
   - `data-row-price`: Price per seat
   - `data-row-available`: Available seats count

2. **Tickets**:
   - `data-row-id`: Links to row
   - `data-seat-number`: Seat number
   - `data-ticket-status`: "available" or "booked"
   - `data-ticket-price`: Price for this ticket

## Error Handling and Fallbacks

```javascript
function initializeSeatMap() {
    try {
        // Check if required elements exist
        const svgContainer = document.getElementById('svg-container');
        const tooltip = document.getElementById('seat-tooltip');
        
        if (!svgContainer || !tooltip) {
            console.warn('Required elements for seat map not found');
            return;
        }
        
        // Initialize features
        initializeTooltips();
        initializeRowSelection();
        initializeTicketFiltering();
        
        // Add success indicator
        document.body.classList.add('seat-map-initialized');
    } catch (error) {
        console.error('Error initializing seat map:', error);
        
        // Show fallback message
        const errorMessage = document.createElement('div');
        errorMessage.className = 'error-message';
        errorMessage.innerHTML = '<p>Interactive seat map failed to load. Please refresh the page.</p>';
        document.body.appendChild(errorMessage);
    }
}
```

This JavaScript implementation provides a robust, interactive seat selection experience with proper error handling and mobile support.