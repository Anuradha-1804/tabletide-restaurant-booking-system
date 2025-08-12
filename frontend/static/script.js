document.addEventListener('DOMContentLoaded', () => {
    const bookingForm = document.getElementById('bookingForm');
    const messageDiv = document.getElementById('message');
    const bookingsList = document.getElementById('bookingsList');

    const fetchBookings = async () => {
        try {
            const response = await fetch('/api/bookings');
            const bookings = await response.json();
            bookingsList.innerHTML = '';
            if (bookings.length === 0) {
                bookingsList.innerHTML = '<li>There are no current bookings.</li>';
                return;
            }
            bookings.forEach(booking => {
                const li = document.createElement('li');
                const bookingDate = new Date(booking.datetime);
                const formattedDateTime = bookingDate.toLocaleString('en-US', {
                    day: '2-digit', month: '2-digit', year: 'numeric',
                    hour: '2-digit', minute: '2-digit'
                });
                li.innerHTML = `
                    <span><strong>${booking.name}</strong> (${booking.email})</span>
                    <span>Table ${booking.table_number} - ${formattedDateTime}</span>
                `;
                bookingsList.appendChild(li);
            });
        } catch (error) {
            console.error("Error fetching bookings:", error);
            bookingsList.innerHTML = '<li>Error loading bookings.</li>';
        }
    };

    bookingForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        const formData = {
            name: document.getElementById('name').value,
            email: document.getElementById('email').value,
            date: document.getElementById('date').value,
            time: document.getElementById('time').value,
            table_number: document.getElementById('table_number').value,
        };

        try {
            const response = await fetch('/api/book', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData),
            });

            const result = await response.json();
            messageDiv.textContent = result.message;
            messageDiv.style.color = response.ok ? '#27ae60' : '#c0392b';

            if (response.ok) {
                bookingForm.reset();
                fetchBookings();
            }
        } catch (error) {
            messageDiv.textContent = 'An error occurred while booking. Please try again.';
            messageDiv.style.color = '#c0392b';
        }
    });

    fetchBookings();
});