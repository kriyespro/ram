// Main JavaScript for RamJaap application

// Helper function to get CSRF token for AJAX requests
function getCsrfToken() {
    return document.querySelector('[name=csrfmiddlewaretoken]').value;
}

// Format number with commas for display
function formatNumber(num) {
    return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}

// Document ready function
document.addEventListener('DOMContentLoaded', function() {
    // Initialize date pickers if present
    const datePickers = document.querySelectorAll('.date-picker');
    if(datePickers.length > 0) {
        datePickers.forEach(picker => {
            // Initialize date picker functionality if needed
        });
    }
    
    // Auto-hide alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    if(alerts.length > 0) {
        alerts.forEach(alert => {
            setTimeout(() => {
                alert.style.opacity = '0';
                setTimeout(() => {
                    alert.style.display = 'none';
                }, 300);
            }, 5000);
        });
    }
}); 