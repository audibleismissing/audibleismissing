document.addEventListener('DOMContentLoaded', function() {
    // Fetch current watch list
    fetch('/api/user/serieswatchlist')
        .then(response => response.json())
        .then(watchlist => {
            const watchlistIds = watchlist.map(item => item.seriesId);
            // Update button texts
            document.querySelectorAll('.watch-btn').forEach(btn => {
                const seriesId = btn.getAttribute('data-series-id');
                if (watchlistIds.includes(seriesId)) {
                    btn.textContent = 'Remove Watch';
                    btn.classList.remove('btn-outline-primary');
                    btn.classList.add('btn-outline-danger');
                } else {
                    btn.textContent = 'Add Watch';
                    btn.classList.remove('btn-outline-danger');
                    btn.classList.add('btn-outline-primary');
                }
            });
        });

    // Handle button clicks
    document.addEventListener('click', function(e) {
        if (e.target.classList.contains('watch-btn')) {
            const btn = e.target;
            const seriesId = btn.getAttribute('data-series-id');
            const isRemove = btn.textContent === 'Remove Watch';

            const url = isRemove ? `/api/user/removeserieswatchlistitem/${seriesId}` : '/api/user/addserieswatchlistitem';
            const method = isRemove ? 'DELETE' : 'POST';

            const data = isRemove ? null : new URLSearchParams({ series_id: seriesId });

            fetch(url, {
                method: method,
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded'
                },
                body: data
            })
            .then(response => response.json())
            .then(data => {
                if ((isRemove && data.message === 'Removed from watch list') || (!isRemove && data.message === 'Added to watch list')) {
                    // Toggle button
                    if (isRemove) {
                        btn.textContent = 'Add Watch';
                        btn.classList.remove('btn-outline-danger');
                        btn.classList.add('btn-outline-primary');
                    } else {
                        btn.textContent = 'Remove Watch';
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