// Global event listeners
document.addEventListener('DOMContentLoaded', function() {
    // Mobile menu toggle
    setupMobileMenu();
    
    // Message close buttons
    setupMessageClosers();
    
    // Library tabs
    setupLibraryTabs();
    
    // Reading progress management
    setupReadingProgress();
    
    // Book review form
    setupReviewForm();
});

// Mobile menu functionality
function setupMobileMenu() {
    const menuToggle = document.querySelector('.menu-toggle');
    const mainNav = document.querySelector('.main-nav');
    
    if (menuToggle && mainNav) {
        menuToggle.addEventListener('click', function() {
            mainNav.classList.toggle('active');
        });
        
        // Handle dropdowns in mobile view
        const dropdownToggles = document.querySelectorAll('.dropdown-toggle');
        
        dropdownToggles.forEach(toggle => {
            toggle.addEventListener('click', function(e) {
                if (window.innerWidth <= 768) {
                    e.preventDefault();
                    const dropdown = this.closest('.dropdown');
                    dropdown.classList.toggle('active');
                }
            });
        });
    }
}

// Message closing functionality
function setupMessageClosers() {
    const closeButtons = document.querySelectorAll('.close-message');
    
    closeButtons.forEach(button => {
        button.addEventListener('click', function() {
            const message = this.closest('.message');
            message.style.opacity = '0';
            setTimeout(() => {
                message.style.display = 'none';
            }, 300);
        });
    });
}

// Library page tab functionality
function setupLibraryTabs() {
    const tabs = document.querySelectorAll('.library-tab');
    
    if (tabs.length > 0) {
        tabs.forEach(tab => {
            tab.addEventListener('click', function() {
                // Remove active class from all tabs
                document.querySelectorAll('.library-tab').forEach(t => {
                    t.classList.remove('active');
                });
                
                // Hide all sections
                document.querySelectorAll('.library-section').forEach(section => {
                    section.classList.remove('active');
                });
                
                // Add active class to clicked tab
                this.classList.add('active');
                
                // Show corresponding section
                const targetId = this.getAttribute('data-target');
                document.getElementById(targetId).classList.add('active');
            });
        });
    }
}

// Reading progress functionality
function setupReadingProgress() {
    // Progress increment/decrement buttons
    const progressContainers = document.querySelectorAll('.reading-progress');
    
    progressContainers.forEach(container => {
        const decrementBtn = container.querySelector('.decrement-progress');
        const incrementBtn = container.querySelector('.increment-progress');
        const progressInput = container.querySelector('.progress-input-small');
        const statusId = container.getAttribute('data-status-id');
        
        if (decrementBtn && incrementBtn && progressInput && statusId) {
            decrementBtn.addEventListener('click', function() {
                let value = parseInt(progressInput.value) || 0;
                value = Math.max(0, value - 1);
                progressInput.value = value;
                updateProgress(statusId, value);
            });
            
            incrementBtn.addEventListener('click', function() {
                let value = parseInt(progressInput.value) || 0;
                value += 1;
                progressInput.value = value;
                updateProgress(statusId, value);
            });
            
            progressInput.addEventListener('change', function() {
                let value = parseInt(progressInput.value) || 0;
                value = Math.max(0, value);
                progressInput.value = value;
                updateProgress(statusId, value);
            });
        }
    });
}

// Send AJAX request to update reading progress
function updateProgress(statusId, progress) {
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    
    fetch(`/update-progress/${statusId}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': csrfToken
        },
        body: `progress=${progress}`
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Update the progress display
            const progressBar = document.querySelector(`.reading-progress[data-status-id="${statusId}"] .progress-fill`);
            if (progressBar) {
                progressBar.style.width = `${data.progress}%`;
            }
            
            // Show a temporary success message
            showToast('Progress updated!');
        } else {
            showToast('Error updating progress', 'error');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showToast('Failed to update progress', 'error');
    });
}

// Review form functionality
function setupReviewForm() {
    const ratingInput = document.querySelector('.rating-input');
    
    if (ratingInput) {
        ratingInput.addEventListener('input', function() {
            const value = parseInt(this.value) || 0;
            if (value < 1) this.value = 1;
            if (value > 10) this.value = 10;
            
            // Update star display if present
            const starDisplay = document.querySelector('.dynamic-stars');
            if (starDisplay) {
                updateStars(starDisplay, value);
            }
        });
    }
}

// Update star display based on rating value
function updateStars(container, rating) {
    // Clear the container
    container.innerHTML = '';
    
    // Calculate full and half stars
    const fullStars = Math.floor(rating / 2);
    const halfStar = rating % 2 === 1;
    const emptyStars = 5 - fullStars - (halfStar ? 1 : 0);
    
    // Add full stars
    for (let i = 0; i < fullStars; i++) {
        container.innerHTML += '<i class="fas fa-star"></i>';
    }
    
    // Add half star if needed
    if (halfStar) {
        container.innerHTML += '<i class="fas fa-star-half-alt"></i>';
    }
    
    // Add empty stars
    for (let i = 0; i < emptyStars; i++) {
        container.innerHTML += '<i class="far fa-star"></i>';
    }
}

// Show a toast notification
function showToast(message, type = 'success') {
    // Check if toast container exists, create if not
    let toastContainer = document.querySelector('.toast-container');
    
    if (!toastContainer) {
        toastContainer = document.createElement('div');
        toastContainer.className = 'toast-container';
        document.body.appendChild(toastContainer);
        
        // Add CSS for the toast container
        const style = document.createElement('style');
        style.textContent = `
            .toast-container {
                position: fixed;
                bottom: 20px;
                right: 20px;
                z-index: 1000;
            }
            
            .toast {
                padding: 12px 20px;
                margin-bottom: 10px;
                border-radius: 4px;
                color: white;
                box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
                animation: fadeIn 0.3s, fadeOut 0.3s 2.7s;
                opacity: 0;
                max-width: 300px;
            }
            
            .toast.success {
                background-color: #4caf50;
            }
            
            .toast.error {
                background-color: #f44336;
            }
            
            .toast.info {
                background-color: #2196f3;
            }
            
            @keyframes fadeIn {
                from { opacity: 0; transform: translateY(20px); }
                to { opacity: 1; transform: translateY(0); }
            }
            
            @keyframes fadeOut {
                from { opacity: 1; transform: translateY(0); }
                to { opacity: 0; transform: translateY(-20px); }
            }
        `;
        document.head.appendChild(style);
    }
    
    // Create toast element
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.textContent = message;
    
    // Add toast to container
    toastContainer.appendChild(toast);
    
    // Force a reflow to ensure animation plays
    void toast.offsetWidth;
    
    // Make the toast visible
    toast.style.opacity = '1';
    
    // Remove toast after animation
    setTimeout(() => {
        toast.style.opacity = '0';
        setTimeout(() => {
            toastContainer.removeChild(toast);
        }, 300);
    }, 3000);
}