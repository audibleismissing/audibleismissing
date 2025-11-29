document.addEventListener('DOMContentLoaded', function() {
    // Fetch current wish list
    fetch('/api/user/bookwishlist')
        .then(response => response.json())
        .then(wishlist => {
            const wishlistIds = wishlist.map(item => item.bookId);
            // Update button texts
            document.querySelectorAll('.wish-btn').forEach(btn => {
                const bookId = btn.getAttribute('data-book-id');
                if (wishlistIds.includes(bookId)) {
                    btn.textContent = 'Remove';
                    btn.classList.remove('btn-outline-primary');
                    btn.classList.add('btn-outline-danger');
                } else {
                    btn.textContent = 'Add';
                    btn.classList.remove('btn-outline-danger');
                    btn.classList.add('btn-outline-primary');
                }
            });
        });

    // Handle button clicks
    document.addEventListener('click', function(e) {
        if (e.target.classList.contains('wish-btn')) {
            const btn = e.target;
            const bookId = btn.getAttribute('data-book-id');
            const isRemove = btn.textContent === 'Remove';

            const url = isRemove ? `/api/user/removebookwishlistitem/${bookId}` : '/api/user/addbookwishlistitem';
            const method = isRemove ? 'DELETE' : 'POST';

            const data = isRemove ? null : new URLSearchParams({ book_id: bookId });

            fetch(url, {
                method: method,
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded'
                },
                body: data
            })
            .then(response => response.json())
            .then(data => {
                if ((isRemove && data.message === 'Removed from wish list') || (!isRemove && data.message === 'Added to wish list')) {
                    // Toggle button
                    if (isRemove) {
                        btn.textContent = 'Add';
                        btn.classList.remove('btn-outline-danger');
                        btn.classList.add('btn-outline-primary');
                    } else {
                        btn.textContent = 'Remove';
                        btn.classList.remove('btn-outline-primary');
                        btn.classList.add('btn-outline-danger');
                    }
                } else {
                    console.error('Operation failed:', data.message);
                }
                console.log(data.message);
            })
            .catch(error => console.error('Error:', error));
        }
    });
});