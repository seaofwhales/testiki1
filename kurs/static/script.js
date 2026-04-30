const tg = window.Telegram.WebApp;
tg.expand();

let userId = tg.initDataUnsafe.user?.id || 123456; // Fallback for testing

async function loadEvents() {
    try {
        const response = await fetch(`/api/events/${userId}`);
        const events = await response.json();
        displayEvents(events);
    } catch (error) {
        console.error('Error loading events:', error);
    }
}

function displayEvents(events) {
    const eventsList = document.getElementById('eventsList');
    eventsList.innerHTML = '<h3>Your Events</h3>';
    
    if (events.length === 0) {
        eventsList.innerHTML += '<p>No events yet</p>';
        return;
    }

    events.forEach(event => {
        const eventElement = document.createElement('div');
        eventElement.className = 'event-item';
        eventElement.innerHTML = `
            <strong>${event.title}</strong>
            <p>Date: ${event.date}</p>
            ${event.description ? `<p>${event.description}</p>` : ''}
            <button class="delete-btn" onclick="deleteEvent('${event.date}', '${event.title}')">
                Delete
            </button>
        `;
        eventsList.appendChild(eventElement);
    });
}

async function addEvent() {
    const date = document.getElementById('eventDate').value;
    const title = document.getElementById('eventTitle').value;
    const description = document.getElementById('eventDesc').value;

    if (!date || !title) {
        alert('Please fill required fields');
        return;
    }

    try {
        const response = await fetch('/api/events/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                user_id: userId,
                date: date,
                title: title,
                description: description
            })
        });

        if (response.ok) {
            document.getElementById('eventDate').value = '';
            document.getElementById('eventTitle').value = '';
            document.getElementById('eventDesc').value = '';
            loadEvents();
        }
    } catch (error) {
        console.error('Error adding event:', error);
    }
}

async function deleteEvent(date, title) {
    if (!confirm('Delete this event?')) return;

    try {
        const response = await fetch(`/api/events/${userId}?date=${date}&title=${encodeURIComponent(title)}`, {
            method: 'DELETE'
        });

        if (response.ok) {
            loadEvents();
        }
    } catch (error) {
        console.error('Error deleting event:', error);
    }
}

// Load events when page loads https://timeweb.cloud/tutorials/react/telegram-web-app-kak-sozdat-mini-prilozhenie-v-telegram#shag-1--podgotovka-okrujeniya

document.addEventListener('DOMContentLoaded', loadEvents);
