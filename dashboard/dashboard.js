// Dashboard Charts and Interactivity
document.addEventListener('DOMContentLoaded', function() {
    // Chart defaults for dark theme
    Chart.defaults.color = '#a1a1aa';
    Chart.defaults.borderColor = '#2a2a2a';
    
    // Inboxes Chart
    const inboxCtx = document.getElementById('inboxChart').getContext('2d');
    new Chart(inboxCtx, {
        type: 'line',
        data: {
            labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
            datasets: [{
                data: [3, 4, 3, 5, 4, 5, 5],
                borderColor: '#ef4444',
                backgroundColor: 'rgba(239, 68, 68, 0.1)',
                borderWidth: 2,
                tension: 0.4,
                fill: true,
                pointRadius: 0,
                pointHoverRadius: 4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false }
            },
            scales: {
                x: { display: false },
                y: { display: false, min: 0 }
            }
        }
    });
    
    // Messages Chart
    const messagesCtx = document.getElementById('messagesChart').getContext('2d');
    new Chart(messagesCtx, {
        type: 'line',
        data: {
            labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
            datasets: [{
                data: [45, 52, 48, 65, 58, 72, 128],
                borderColor: '#22c55e',
                backgroundColor: 'rgba(34, 197, 94, 0.1)',
                borderWidth: 2,
                tension: 0.4,
                fill: true,
                pointRadius: 0,
                pointHoverRadius: 4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false }
            },
            scales: {
                x: { display: false },
                y: { display: false, min: 0 }
            }
        }
    });
    
    // Attachments Chart
    const attachmentsCtx = document.getElementById('attachmentsChart').getContext('2d');
    new Chart(attachmentsCtx, {
        type: 'line',
        data: {
            labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
            datasets: [{
                data: [12, 15, 18, 14, 22, 19, 23],
                borderColor: '#eab308',
                backgroundColor: 'rgba(234, 179, 8, 0.1)',
                borderWidth: 2,
                tension: 0.4,
                fill: true,
                pointRadius: 0,
                pointHoverRadius: 4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false }
            },
            scales: {
                x: { display: false },
                y: { display: false, min: 0 }
            }
        }
    });
    
    // Navigation active state
    document.querySelectorAll('.nav-item').forEach(item => {
        item.addEventListener('click', function(e) {
            e.preventDefault();
            document.querySelectorAll('.nav-item').forEach(i => i.classList.remove('active'));
            this.classList.add('active');
        });
    });
    
    // Simulate live data updates
    setInterval(() => {
        // Update timestamps
        document.querySelectorAll('.message-time').forEach(el => {
            const text = el.textContent;
            if (text.includes('min ago')) {
                const mins = parseInt(text);
                if (!isNaN(mins) && mins < 60) {
                    el.textContent = `${mins + 1} min ago`;
                }
            }
        });
    }, 60000); // Every minute
    
    // New Inbox button
    document.querySelector('.btn-primary').addEventListener('click', function() {
        // Show notification
        showNotification('Creating new inbox...', 'info');
        
        // Simulate creation delay
        setTimeout(() => {
            showNotification('New inbox created successfully!', 'success');
        }, 1500);
    });
    
    // View All button
    document.querySelector('.btn-secondary').addEventListener('click', function() {
        showNotification('Loading all activities...', 'info');
    });
});

// Notification system
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;
    
    notification.style.cssText = `
        position: fixed;
        top: 24px;
        right: 24px;
        padding: 16px 24px;
        border-radius: 8px;
        font-size: 14px;
        font-weight: 500;
        z-index: 1000;
        animation: slideIn 0.3s ease;
    `;
    
    if (type === 'success') {
        notification.style.background = 'rgba(34, 197, 94, 0.1)';
        notification.style.border = '1px solid #22c55e';
        notification.style.color = '#22c55e';
    } else {
        notification.style.background = 'rgba(59, 130, 246, 0.1)';
        notification.style.border = '1px solid #3b82f6';
        notification.style.color = '#3b82f6';
    }
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease';
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

// Add animation keyframes
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);