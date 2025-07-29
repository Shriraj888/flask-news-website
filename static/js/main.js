// Enhanced JavaScript for Flask News Website with Modern UI and Validations

document.addEventListener('DOMContentLoaded', function() {
    // Initialize all components
    initContactForm();
    initSmoothScrolling();
    initTooltips();
    initMobileNav();
    initAnimations();
    initThemeEffects();
    initFormValidations();
    
    // Add loading state to page
    setTimeout(() => {
        document.body.classList.add('loaded');
    }, 100);
});

/**
 * Enhanced contact form with real-time validation
 */
function initContactForm() {
    const contactForm = document.getElementById('contactForm');
    const responseMessage = document.getElementById('responseMessage');
    const messageTextarea = document.getElementById('message');
    const charCount = document.getElementById('charCount');
    
    if (contactForm) {
        // Character counter for message
        if (messageTextarea && charCount) {
            messageTextarea.addEventListener('input', function() {
                const currentLength = this.value.length;
                charCount.textContent = currentLength;
                
                // Color coding based on length
                if (currentLength < 10) {
                    charCount.style.color = 'var(--error-color)';
                } else if (currentLength > 900) {
                    charCount.style.color = 'var(--warning-color)';
                } else {
                    charCount.style.color = 'var(--success-color)';
                }
            });
        }
        
        // Real-time validation for all form fields
        const formFields = contactForm.querySelectorAll('input, select, textarea');
        formFields.forEach(field => {
            field.addEventListener('blur', () => validateField(field));
            field.addEventListener('input', () => {
                if (field.classList.contains('is-invalid')) {
                    validateField(field);
                }
            });
        });
        
        // Form submission
        contactForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            // Validate all fields
            let isValid = true;
            formFields.forEach(field => {
                if (!validateField(field)) {
                    isValid = false;
                }
            });
            
            if (!isValid) {
                showToast('Please fix the errors in the form', 'error');
                return;
            }
            
            const formData = new FormData(contactForm);
            const submitBtn = contactForm.querySelector('button[type="submit"]');
            const btnText = submitBtn.querySelector('.btn-text');
            const spinner = submitBtn.querySelector('.spinner-border');
            
            // Show loading state
            submitBtn.disabled = true;
            btnText.textContent = 'Sending...';
            spinner.style.display = 'inline-block';
            
            // Create full name from first and last name
            const firstName = formData.get('firstName');
            const lastName = formData.get('lastName');
            formData.set('name', `${firstName} ${lastName}`);
            
            // Send form data
            fetch('/contact', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    showMessage(data.message, 'success');
                    contactForm.reset();
                    formFields.forEach(field => {
                        field.classList.remove('is-valid', 'is-invalid');
                    });
                    showToast('Message sent successfully!', 'success');
                } else {
                    showMessage(data.message || 'An error occurred. Please try again.', 'danger');
                    showToast('Failed to send message', 'error');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                showMessage('An error occurred. Please try again.', 'danger');
                showToast('Network error occurred', 'error');
            })
            .finally(() => {
                // Reset button state
                submitBtn.disabled = false;
                btnText.textContent = 'Send Message';
                spinner.style.display = 'none';
            });
        });
    }
    
    function showMessage(message, type) {
        if (responseMessage) {
            responseMessage.innerHTML = `
                <div class="alert alert-${type} alert-dismissible fade show animate-fadeInUp" role="alert">
                    <i class="fas fa-${type === 'success' ? 'check-circle' : 'exclamation-triangle'} me-2"></i>
                    ${message}
                    <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                </div>
            `;
            responseMessage.style.display = 'block';
            
            // Auto-hide after 5 seconds
            setTimeout(() => {
                const alert = responseMessage.querySelector('.alert');
                if (alert && alert.classList.contains('show')) {
                    alert.classList.remove('show');
                    setTimeout(() => {
                        responseMessage.style.display = 'none';
                    }, 150);
                }
            }, 5000);
        }
    }
}

/**
 * Advanced form field validation
 */
function validateField(field) {
    const value = field.value.trim();
    let isValid = true;
    
    // Remove previous validation classes
    field.classList.remove('is-valid', 'is-invalid');
    
    // Required field validation
    if (field.hasAttribute('required') && !value) {
        isValid = false;
    }
    
    // Specific field validations
    switch (field.type) {
        case 'email':
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (value && !emailRegex.test(value)) {
                isValid = false;
            }
            break;
            
        case 'tel':
            const phoneRegex = /^[0-9\-\+\s\(\)]+$/;
            if (value && !phoneRegex.test(value)) {
                isValid = false;
            }
            break;
            
        case 'text':
            if (field.hasAttribute('minlength')) {
                const minLength = parseInt(field.getAttribute('minlength'));
                if (value.length < minLength) {
                    isValid = false;
                }
            }
            break;
            
        case 'textarea':
            if (field.hasAttribute('minlength')) {
                const minLength = parseInt(field.getAttribute('minlength'));
                if (value.length < minLength) {
                    isValid = false;
                }
            }
            if (field.hasAttribute('maxlength')) {
                const maxLength = parseInt(field.getAttribute('maxlength'));
                if (value.length > maxLength) {
                    isValid = false;
                }
            }
            break;
    }
    
    // Custom validation for select fields
    if (field.tagName.toLowerCase() === 'select' && field.hasAttribute('required')) {
        if (!value) {
            isValid = false;
        }
    }
    
    // Custom validation for checkboxes
    if (field.type === 'checkbox' && field.hasAttribute('required')) {
        if (!field.checked) {
            isValid = false;
        }
    }
    
    // Apply validation classes with animation
    if (isValid) {
        field.classList.add('is-valid');
        animateValidation(field, true);
    } else {
        field.classList.add('is-invalid');
        animateValidation(field, false);
    }
    
    return isValid;
}

/**
 * Animate validation feedback
 */
function animateValidation(field, isValid) {
    const feedback = field.parentNode.querySelector(isValid ? '.valid-feedback' : '.invalid-feedback');
    if (feedback) {
        feedback.style.opacity = '0';
        feedback.style.transform = 'translateY(-10px)';
        setTimeout(() => {
            feedback.style.transition = 'all 0.3s ease';
            feedback.style.opacity = '1';
            feedback.style.transform = 'translateY(0)';
        }, 100);
    }
}

/**
 * Initialize smooth scrolling for anchor links
 */
function initSmoothScrolling() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

/**
 * Initialize Bootstrap tooltips with custom styling
 */
function initTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl, {
            customClass: 'custom-tooltip'
        });
    });
}

/**
 * Enhanced mobile navigation
 */
function initMobileNav() {
    const navbarToggler = document.querySelector('.navbar-toggler');
    const navbarCollapse = document.querySelector('.navbar-collapse');
    
    if (navbarToggler && navbarCollapse) {
        // Close navbar when clicking on a nav link (mobile)
        document.querySelectorAll('.navbar-nav .nav-link').forEach(link => {
            link.addEventListener('click', () => {
                if (window.innerWidth < 992) {
                    const bsCollapse = new bootstrap.Collapse(navbarCollapse, {
                        toggle: false
                    });
                    bsCollapse.hide();
                }
            });
        });
        
        // Add burger animation
        navbarToggler.addEventListener('click', function() {
            this.classList.toggle('active');
        });
    }
}

/**
 * Initialize scroll-based animations
 */
function initAnimations() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-fadeInUp');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);
    
    // Observe all cards and important elements
    document.querySelectorAll('.card, .jumbotron, .alert').forEach(el => {
        observer.observe(el);
    });
}

/**
 * Initialize theme effects and interactions
 */
function initThemeEffects() {
    // Add hover effects to cards
    document.querySelectorAll('.card').forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-10px) scale(1.02)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0) scale(1)';
        });
    });
    
    // Add ripple effect to buttons
    document.querySelectorAll('.btn').forEach(button => {
        button.addEventListener('click', function(e) {
            const ripple = document.createElement('span');
            const rect = this.getBoundingClientRect();
            const size = Math.max(rect.width, rect.height);
            const x = e.clientX - rect.left - size / 2;
            const y = e.clientY - rect.top - size / 2;
            
            ripple.style.width = ripple.style.height = size + 'px';
            ripple.style.left = x + 'px';
            ripple.style.top = y + 'px';
            ripple.classList.add('ripple');
            
            this.appendChild(ripple);
            
            setTimeout(() => {
                ripple.remove();
            }, 600);
        });
    });
}

/**
 * Initialize form-specific validations
 */
function initFormValidations() {
    // Email format validation
    document.querySelectorAll('input[type="email"]').forEach(emailField => {
        emailField.addEventListener('input', function() {
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            const isValid = emailRegex.test(this.value);
            
            if (this.value.length > 0) {
                this.classList.toggle('is-valid', isValid);
                this.classList.toggle('is-invalid', !isValid);
            }
        });
    });
    
    // Phone number formatting
    document.querySelectorAll('input[type="tel"]').forEach(phoneField => {
        phoneField.addEventListener('input', function() {
            // Remove non-numeric characters except for common phone symbols
            this.value = this.value.replace(/[^0-9\-\+\s\(\)]/g, '');
        });
    });
}

/**
 * Enhanced toast notifications
 */
function showToast(message, type = 'info') {
    let toastContainer = document.querySelector('.toast-container');
    if (!toastContainer) {
        toastContainer = document.createElement('div');
        toastContainer.className = 'toast-container position-fixed top-0 end-0 p-3';
        toastContainer.style.zIndex = '9999';
        document.body.appendChild(toastContainer);
    }
    
    const toastId = 'toast-' + Date.now();
    const iconMap = {
        success: 'check-circle',
        error: 'exclamation-triangle',
        warning: 'exclamation-circle',
        info: 'info-circle'
    };
    
    const toastHtml = `
        <div id="${toastId}" class="toast" role="alert" data-bs-autohide="true" data-bs-delay="4000">
            <div class="toast-header">
                <i class="fas fa-${iconMap[type] || 'info-circle'} me-2 text-${type === 'error' ? 'danger' : type}"></i>
                <strong class="me-auto">Notification</strong>
                <button type="button" class="btn-close" data-bs-dismiss="toast"></button>
            </div>
            <div class="toast-body">
                ${message}
            </div>
        </div>
    `;
    
    toastContainer.insertAdjacentHTML('beforeend', toastHtml);
    const toastElement = document.getElementById(toastId);
    const toast = new bootstrap.Toast(toastElement);
    
    // Add entrance animation
    toastElement.style.opacity = '0';
    toastElement.style.transform = 'translateX(100%)';
    
    setTimeout(() => {
        toastElement.style.transition = 'all 0.3s ease';
        toastElement.style.opacity = '1';
        toastElement.style.transform = 'translateX(0)';
    }, 10);
    
    toast.show();
    
    // Remove toast element after it's hidden
    toastElement.addEventListener('hidden.bs.toast', function() {
        toastElement.remove();
    });
}

/**
 * Utility functions
 */
function formatDate(dateString) {
    const options = { 
        year: 'numeric', 
        month: 'long', 
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    };
    return new Date(dateString).toLocaleDateString('en-US', options);
}

function truncateText(text, maxLength) {
    if (text.length <= maxLength) return text;
    return text.substr(0, maxLength) + '...';
}

function addLoadingState(button, loadingText = 'Loading...') {
    const originalText = button.textContent;
    button.disabled = true;
    button.innerHTML = `<span class="spinner-border spinner-border-sm me-2" role="status"></span> ${loadingText}`;
    
    return function removeLoadingState() {
        button.disabled = false;
        button.textContent = originalText;
    };
}

// Add CSS for ripple effect
const style = document.createElement('style');
style.textContent = `
    .btn {
        position: relative;
        overflow: hidden;
    }
    
    .ripple {
        position: absolute;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.3);
        transform: scale(0);
        animation: ripple-animation 0.6s linear;
        pointer-events: none;
    }
    
    @keyframes ripple-animation {
        to {
            transform: scale(4);
            opacity: 0;
        }
    }
    
    .custom-tooltip .tooltip-inner {
        background: var(--bg-card);
        color: var(--text-primary);
        border: 1px solid var(--border-color);
        border-radius: 8px;
    }
    
    .custom-tooltip.bs-tooltip-top .tooltip-arrow::before {
        border-top-color: var(--bg-card);
    }
`;
document.head.appendChild(style);

// Export functions for global use
window.FlaskNews = {
    formatDate,
    truncateText,
    addLoadingState,
    showToast,
    validateField
};
