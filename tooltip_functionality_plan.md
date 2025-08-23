# Tooltip Functionality Plan

## Overview

The tooltip functionality will provide users with detailed information about seat rows when they hover over them. This includes:
1. Row name
2. Total capacity
3. Price per seat
4. Available seats count
5. Booked seats count

## HTML Structure

The tooltip will be a single element positioned absolutely on the page:

```html
<div id="seat-tooltip" class="tooltip" role="tooltip" aria-hidden="true">
    <div class="tooltip-content">
        <h4 class="tooltip-title">Row A</h4>
        <div class="tooltip-details">
            <div class="tooltip-row">
                <span class="tooltip-label">Capacity:</span>
                <span class="tooltip-value">50 seats</span>
            </div>
            <div class="tooltip-row">
                <span class="tooltip-label">Price:</span>
                <span class="tooltip-value">$25.00 per seat</span>
            </div>
            <div class="tooltip-row">
                <span class="tooltip-label">Available:</span>
                <span class="tooltip-value">35 seats</span>
            </div>
            <div class="tooltip-row">
                <span class="tooltip-label">Booked:</span>
                <span class="tooltip-value">15 seats</span>
            </div>
        </div>
    </div>
    <div class="tooltip-arrow" data-popper-arrow></div>
</div>
```

## CSS Styling

```css
.tooltip {
    position: absolute;
    z-index: 1000;
    display: none;
    background: rgba(0, 0, 0, 0.9);
    color: white;
    border-radius: 6px;
    padding: 0;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
    font-size: 14px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
    backdrop-filter: blur(4px);
    transition: opacity 0.2s ease, transform 0.2s ease;
    opacity: 0;
    transform: scale(0.95);
    pointer-events: none;
}

.tooltip.visible {
    display: block;
    opacity: 1;
    transform: scale(1);
}

.tooltip-content {
    padding: 12px 16px;
}

.tooltip-title {
    margin: 0 0 8px 0;
    font-size: 16px;
    font-weight: 600;
    color: #fff;
}

.tooltip-details {
    display: flex;
    flex-direction: column;
    gap: 6px;
}

.tooltip-row {
    display: flex;
    justify-content: space-between;
    gap: 15px;
}

.tooltip-label {
    color: #ccc;
    font-size: 13px;
}

.tooltip-value {
    color: #fff;
    font-weight: 500;
    text-align: right;
}

.tooltip-arrow {
    position: absolute;
    width: 12px;
    height: 12px;
    background: inherit;
    visibility: hidden;
}

.tooltip-arrow::before {
    position: absolute;
    width: 12px;
    height: 12px;
    background: inherit;
    visibility: visible;
    content: '';
    transform: rotate(45deg);
}

.tooltip[data-popper-placement^='top'] > .tooltip-arrow {
    bottom: -6px;
}

.tooltip[data-popper-placement^='bottom'] > .tooltip-arrow {
    top: -6px;
}

.tooltip[data-popper-placement^='left'] > .tooltip-arrow {
    right: -6px;
}

.tooltip[data-popper-placement^='right'] > .tooltip-arrow {
    left: -6px;
}

/* Animation for tooltip entrance */
@keyframes tooltipFadeIn {
    from {
        opacity: 0;
        transform: translateY(5px) scale(0.95);
    }
    to {
        opacity: 1;
        transform: translateY(0) scale(1);
    }
}

.tooltip.visible {
    animation: tooltipFadeIn 0.2s ease-out forwards;
}

/* Dark mode support */
@media (prefers-color-scheme: dark) {
    .tooltip {
        background: rgba(30, 30, 30, 0.95);
    }
}
```

## JavaScript Implementation

```javascript
class SeatTooltip {
    constructor() {
        this.tooltip = null;
        this.currentTarget = null;
        this.isVisible = false;
        this.init();
    }
    
    init() {
        // Create tooltip element
        this.createTooltip();
        
        // Initialize event listeners
        this.initEventListeners();
    }
    
    createTooltip() {
        // Check if tooltip already exists
        this.tooltip = document.getElementById('seat-tooltip');
        
        if (!this.tooltip) {
            this.tooltip = document.createElement('div');
            this.tooltip.id = 'seat-tooltip';
            this.tooltip.className = 'tooltip';
            this.tooltip.setAttribute('role', 'tooltip');
            this.tooltip.setAttribute('aria-hidden', 'true');
            
            this.tooltip.innerHTML = `
                <div class="tooltip-content">
                    <h4 class="tooltip-title">Row Name</h4>
                    <div class="tooltip-details">
                        <div class="tooltip-row">
                            <span class="tooltip-label">Capacity:</span>
                            <span class="tooltip-value">0 seats</span>
                        </div>
                        <div class="tooltip-row">
                            <span class="tooltip-label">Price:</span>
                            <span class="tooltip-value">$0.00 per seat</span>
                        </div>
                        <div class="tooltip-row">
                            <span class="tooltip-label">Available:</span>
                            <span class="tooltip-value">0 seats</span>
                        </div>
                        <div class="tooltip-row">
                            <span class="tooltip-label">Booked:</span>
                            <span class="tooltip-value">0 seats</span>
                        </div>
                    </div>
                </div>
                <div class="tooltip-arrow" data-popper-arrow></div>
            `;
            
            document.body.appendChild(this.tooltip);
        }
    }
    
    initEventListeners() {
        // Add event listeners to all seat rows
        const seatRows = document.querySelectorAll('.seat-row');
        
        seatRows.forEach(row => {
            row.addEventListener('mouseenter', (e) => this.show(e.currentTarget));
            row.addEventListener('mouseleave', () => this.hide());
            row.addEventListener('mousemove', (e) => this.updatePosition(e));
        });
        
        // Hide tooltip when moving outside SVG
        const svgContainer = document.getElementById('svg-container');
        if (svgContainer) {
            svgContainer.addEventListener('mouseleave', () => this.hide());
        }
    }
    
    show(targetElement) {
        if (!targetElement || !this.tooltip) return;
        
        this.currentTarget = targetElement;
        
        // Update tooltip content with row data
        this.updateContent(targetElement);
        
        // Position tooltip
        this.positionTooltip(targetElement);
        
        // Show tooltip with animation
        this.tooltip.classList.add('visible');
        this.tooltip.setAttribute('aria-hidden', 'false');
        this.isVisible = true;
    }
    
    hide() {
        if (!this.tooltip) return;
        
        this.tooltip.classList.remove('visible');
        this.tooltip.setAttribute('aria-hidden', 'true');
        this.isVisible = false;
        this.currentTarget = null;
    }
    
    updateContent(targetElement) {
        if (!targetElement || !this.tooltip) return;
        
        // Get row data from attributes
        const rowData = {
            name: targetElement.getAttribute('data-row-name') || 'Unknown Row',
            capacity: targetElement.getAttribute('data-row-capacity') || '0',
            price: targetElement.getAttribute('data-row-price') || '0.00',
            available: targetElement.getAttribute('data-row-available') || '0',
            booked: targetElement.getAttribute('data-row-booked') || '0'
        };
        
        // Update tooltip content
        this.tooltip.querySelector('.tooltip-title').textContent = rowData.name;
        this.tooltip.querySelector('.tooltip-details').innerHTML = `
            <div class="tooltip-row">
                <span class="tooltip-label">Capacity:</span>
                <span class="tooltip-value">${rowData.capacity} seats</span>
            </div>
            <div class="tooltip-row">
                <span class="tooltip-label">Price:</span>
                <span class="tooltip-value">$${parseFloat(rowData.price).toFixed(2)} per seat</span>
            </div>
            <div class="tooltip-row">
                <span class="tooltip-label">Available:</span>
                <span class="tooltip-value">${rowData.available} seats</span>
            </div>
            <div class="tooltip-row">
                <span class="tooltip-label">Booked:</span>
                <span class="tooltip-value">${rowData.booked} seats</span>
            </div>
        `;
    }
    
    positionTooltip(targetElement) {
        if (!targetElement || !this.tooltip) return;
        
        // Get target element position
        const targetRect = targetElement.getBoundingClientRect();
        const tooltipRect = this.tooltip.getBoundingClientRect();
        
        // Calculate position (centered above the target)
        let x = targetRect.left + (targetRect.width / 2) - (tooltipRect.width / 2);
        let y = targetRect.top - tooltipRect.height - 10;
        
        // Ensure tooltip stays within viewport
        const padding = 10;
        x = Math.max(padding, Math.min(x, window.innerWidth - tooltipRect.width - padding));
        y = Math.max(padding, y);
        
        // Apply position
        this.tooltip.style.left = `${x}px`;
        this.tooltip.style.top = `${y}px`;
    }
    
    updatePosition(event) {
        if (!this.isVisible || !this.tooltip) return;
        
        // Update tooltip position to follow cursor
        const tooltipRect = this.tooltip.getBoundingClientRect();
        const padding = 15;
        
        let x = event.pageX + 15;
        let y = event.pageY + 15;
        
        // Ensure tooltip stays within viewport
        if (x + tooltipRect.width > window.innerWidth - padding) {
            x = event.pageX - tooltipRect.width - 15;
        }
        
        if (y + tooltipRect.height > window.innerHeight - padding) {
            y = event.pageY - tooltipRect.height - 15;
        }
        
        this.tooltip.style.left = `${x}px`;
        this.tooltip.style.top = `${y}px`;
    }
    
    // Method to update tooltip data dynamically
    updateRowData(rowId, data) {
        if (this.currentTarget && this.currentTarget.getAttribute('data-row-id') === rowId) {
            // Update the current tooltip if it's showing this row
            this.updateContent(this.currentTarget);
        }
    }
}

// Initialize tooltip when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    window.seatTooltip = new SeatTooltip();
});

// Export for potential use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = SeatTooltip;
}
```

## Integration with Existing Code

The tooltip functionality needs to integrate with the existing seat selection code:

```javascript
// In the existing seat selection code, modify the mouseenter handler:
function initializeTooltips() {
    const seatRows = document.querySelectorAll('.seat-row');
    
    seatRows.forEach(row => {
        // Mouse enter - show tooltip
        row.addEventListener('mouseenter', function(e) {
            if (window.seatTooltip) {
                window.seatTooltip.show(this);
            } else {
                // Fallback to simple tooltip if class not available
                showSimpleTooltip(this, e);
            }
        });
        
        // Mouse move - update tooltip position
        row.addEventListener('mousemove', function(e) {
            if (window.seatTooltip) {
                window.seatTooltip.updatePosition(e);
            }
        });
        
        // Mouse leave - hide tooltip
        row.addEventListener('mouseleave', function() {
            if (window.seatTooltip) {
                window.seatTooltip.hide();
            }
        });
    });
}
```

## Data Attributes Required

For the tooltip to work properly, the seat row elements need these data attributes:

```html
<rect 
    class="seat-row" 
    id="row-{{ row.id }}"
    data-row-id="{{ row.id }}"
    data-row-name="{{ row.name }}"
    data-row-capacity="{{ row.capacity }}"
    data-row-price="{{ row.price }}"
    data-row-available="{{ row.available_seats }}"
    data-row-booked="{{ row.booked_seats }}"
    x="{{ forloop.counter0|mul:120 }}" 
    y="50" 
    width="100" 
    height="50" 
    fill="#007bff"
    rx="5"
/>
```

## Backend Data Requirements

The Django backend needs to provide the following additional data for each row:
1. `available_seats`: Count of unbooked seats in the row
2. `booked_seats`: Count of booked seats in the row

This can be added to the view:

```python
# In views.py event_detail function
rows = SeatRow.objects.filter(event=event).prefetch_related('seats').order_by('name')
# Annotate with seat counts
from django.db.models import Count, Q
rows = rows.annotate(
    available_seats=Count('seats', filter=Q(seats__is_booked=False)),
    booked_seats=Count('seats', filter=Q(seats__is_booked=True))
)
```

## Accessibility Considerations

1. Proper ARIA attributes for screen readers
2. Keyboard navigation support
3. Sufficient color contrast
4. Appropriate focus management

```javascript
// Add keyboard support
document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape' && window.seatTooltip && window.seatTooltip.isVisible) {
        window.seatTooltip.hide();
    }
});

// Focus management for keyboard users
function initializeKeyboardSupport() {
    const seatRows = document.querySelectorAll('.seat-row');
    
    seatRows.forEach(row => {
        row.setAttribute('tabindex', '0');
        row.setAttribute('role', 'button');
        row.setAttribute('aria-label', `Select ${row.getAttribute('data-row-name')}`);
        
        row.addEventListener('focus', function() {
            if (window.seatTooltip) {
                window.seatTooltip.show(this);
            }
        });
        
        row.addEventListener('blur', function() {
            if (window.seatTooltip) {
                window.seatTooltip.hide();
            }
        });
        
        row.addEventListener('keydown', function(e) {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                this.click();
            }
        });
    });
}
```

This tooltip implementation provides a rich, accessible user experience with smooth animations and proper positioning.