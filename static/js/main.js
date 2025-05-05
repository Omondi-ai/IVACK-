// Online status indicator
document.addEventListener('DOMContentLoaded', function() {
    // Update online status periodically
    function updateOnlineStatus() {
        fetch('/accounts/update_online_status/')
            .then(response => response.json())
            .then(data => {
                console.log('Online status updated');
            });
    }
    
    // Update every 5 minutes
    setInterval(updateOnlineStatus, 5 * 60 * 1000);
    
    // Update on page load
    updateOnlineStatus();
    
    // Mark notifications as read when dropdown is shown
    const notificationDropdown = document.getElementById('notificationDropdown');
    if (notificationDropdown) {
        notificationDropdown.addEventListener('shown.bs.dropdown', function() {
            fetch('/accounts/mark_notifications_read/')
                .then(response => response.json())
                .then(data => {
                    const badge = document.querySelector('.notification-badge');
                    if (badge) {
                        badge.style.display = 'none';
                    }
                });
        });
    }
    
    // Initialize tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
});
document.querySelector('#message-form').addEventListener('submit', async function(e) {
    e.preventDefault();
    const messageInput = document.querySelector('#id_text');
    const fileInput = document.querySelector('#id_attachment');
    const formData = new FormData();
    
    formData.append('text', messageInput.value);
    if (fileInput.files[0]) {
        formData.append('attachment', fileInput.files[0]);
    }
    formData.append('csrfmiddlewaretoken', document.querySelector('[name=csrfmiddlewaretoken]').value);
    
    try {
        const response = await fetch(window.location.href, {
            method: 'POST',
            body: formData
        });
        
        if (response.ok) {
            messageInput.value = '';
            fileInput.value = '';
        }
    } catch (error) {
        console.error('Error:', error);
    }
});