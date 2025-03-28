// Movies App JavaScript

document.addEventListener('DOMContentLoaded', function () {
    // Initialize all rating systems
    initRatings();

    // Initialize watchlist buttons
    initWatchlistButtons();

    // Initialize filter form in media list
    initFilterForm();

    // Initialize video player components
    initVideoPlayers();
});

/**
 * Initialize star rating functionality
 */
function initRatings() {
    const ratingContainers = document.querySelectorAll('.rating-stars.clickable');

    ratingContainers.forEach(container => {
        const stars = container.querySelectorAll('.star');
        const ratingInput = container.nextElementSibling;

        // Show rating on hover
        stars.forEach((star, index) => {
            star.addEventListener('mouseenter', () => {
                // Fill this star and all previous stars
                for (let i = 0; i <= index; i++) {
                    stars[i].classList.remove('bi-star');
                    stars[i].classList.add('bi-star-fill');
                }
                // Empty all next stars
                for (let i = index + 1; i < stars.length; i++) {
                    stars[i].classList.remove('bi-star-fill');
                    stars[i].classList.add('bi-star');
                }
            });

            // Set rating on click
            star.addEventListener('click', () => {
                const value = index + 1;
                ratingInput.value = value;

                // Update visual feedback
                for (let i = 0; i <= index; i++) {
                    stars[i].classList.remove('bi-star');
                    stars[i].classList.add('bi-star-fill');
                }
                for (let i = index + 1; i < stars.length; i++) {
                    stars[i].classList.remove('bi-star-fill');
                    stars[i].classList.add('bi-star');
                }
            });
        });

        // Reset on mouse leave if no rating is selected
        container.addEventListener('mouseleave', () => {
            const currentRating = parseInt(ratingInput.value) || 0;

            stars.forEach((star, index) => {
                if (index < currentRating) {
                    star.classList.remove('bi-star');
                    star.classList.add('bi-star-fill');
                } else {
                    star.classList.remove('bi-star-fill');
                    star.classList.add('bi-star');
                }
            });
        });
    });
}

/**
 * Initialize watchlist functionality
 */
function initWatchlistButtons() {
    const watchlistButtons = document.querySelectorAll('.watchlist-btn');

    watchlistButtons.forEach(button => {
        button.addEventListener('click', function (e) {
            e.preventDefault();

            const mediaId = this.dataset.mediaId;
            const isInWatchlist = this.classList.contains('active');
            const url = isInWatchlist ? `/movies/watchlist/remove/${mediaId}/` : `/movies/watchlist/add/${mediaId}/`;

            // Show loading state
            const icon = this.querySelector('i');
            const originalIcon = icon.className;
            icon.className = 'bi bi-hourglass';

            fetch(url, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
                    'Content-Type': 'application/json'
                },
                credentials: 'same-origin'
            })
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Network response was not ok');
                    }
                    return response.json();
                })
                .then(data => {
                    // Update UI
                    this.classList.toggle('active');
                    this.querySelector('.watchlist-text').textContent = isInWatchlist ? 'Add to Watchlist' : 'Remove from Watchlist';
                    icon.className = isInWatchlist ? 'bi bi-bookmark-plus' : 'bi bi-bookmark-check-fill';

                    // Show toast notification
                    showToast(data.message, 'success');
                })
                .catch(error => {
                    console.error('Error:', error);
                    icon.className = originalIcon;
                    showToast('Error updating watchlist', 'danger');
                });
        });
    });
}

/**
 * Initialize filter form in media list
 */
function initFilterForm() {
    const filterForm = document.getElementById('filter-form');

    if (filterForm) {
        // Auto-submit form when select fields change
        const selectFields = filterForm.querySelectorAll('select');
        selectFields.forEach(select => {
            select.addEventListener('change', () => {
                filterForm.submit();
            });
        });

        // Handle clear filters button
        const clearButton = document.getElementById('clear-filters');
        if (clearButton) {
            clearButton.addEventListener('click', (e) => {
                e.preventDefault();

                // Reset all form fields
                filterForm.querySelectorAll('input, select').forEach(field => {
                    if (field.type === 'checkbox') {
                        field.checked = false;
                    } else if (field.type !== 'submit') {
                        field.value = '';
                    }
                });

                // Submit the form
                filterForm.submit();
            });
        }
    }
}

/**
 * Initialize video players
 */
function initVideoPlayers() {
    const videoContainers = document.querySelectorAll('.video-container');

    videoContainers.forEach(container => {
        const video = container.querySelector('video');

        if (video) {
            // Custom video controls could be implemented here
            console.log('Video player initialized');
        }
    });
}

/**
 * Show toast notification
 */
function showToast(message, type = 'info') {
    // Create toast container if it doesn't exist
    let toastContainer = document.querySelector('.toast-container');

    if (!toastContainer) {
        toastContainer = document.createElement('div');
        toastContainer.className = 'toast-container position-fixed bottom-0 end-0 p-3';
        document.body.appendChild(toastContainer);
    }

    // Create toast element
    const toastId = 'toast-' + Date.now();
    const toast = document.createElement('div');
    toast.className = `toast align-items-center text-white bg-${type} border-0`;
    toast.setAttribute('role', 'alert');
    toast.setAttribute('aria-live', 'assertive');
    toast.setAttribute('aria-atomic', 'true');
    toast.setAttribute('id', toastId);

    toast.innerHTML = `
        <div class="d-flex">
            <div class="toast-body">
                ${message}
            </div>
            <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
        </div>
    `;

    toastContainer.appendChild(toast);

    // Initialize and show the toast
    const bsToast = new bootstrap.Toast(toast, {
        autohide: true,
        delay: 3000
    });

    bsToast.show();

    // Remove the toast from DOM after it's hidden
    toast.addEventListener('hidden.bs.toast', function () {
        this.remove();
    });
}

/**
 * Get CSRF token from cookies
 */
function getCookie(name) {
    let cookieValue = null;

    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');

        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();

            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }

    return cookieValue;
} 