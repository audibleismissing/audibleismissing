document.addEventListener('DOMContentLoaded', function() {
    // Fetch current watch list
    fetch('/api/user/bookwishlist')
        .then(response => response.json())
        .then(watchlist => {
            const watchlistIds = watchlist.map(item => item.bookId);
            // Update button texts
            document.querySelectorAll('.watch-btn').forEach(btn => {
                const bookId = btn.getAttribute('data-book-id');
                if (watchlistIds.includes(bookId)) {
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
        if (e.target.classList.contains('watch-btn')) {
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
                console.log(data.message);
            })
            .catch(error => console.error('Error:', error));
        }
    });
});