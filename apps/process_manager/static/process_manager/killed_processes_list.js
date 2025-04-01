// Sorting state management
let sortState = {
    column: null,
    direction: 'asc'
};

// Mobile menu toggle
document.getElementById('menu-button').addEventListener('click', function(e) {
    e.preventDefault();
    document.querySelector('.dropdown').classList.toggle('open');
});

// Close dropdown when clicking outside
document.addEventListener('click', function(e) {
    const dropdown = document.querySelector('.dropdown');
    const menuButton = document.getElementById('menu-button');

    if (!dropdown.contains(e.target) || e.target === menuButton) {
        return;
    }

    if (dropdown.classList.contains('open')) {
        dropdown.classList.remove('open');
    }
});

// Timestamp update function
function updateTimestamp() {
    const now = new Date();
    document.getElementById('timestamp').textContent =
        now.toLocaleString('pl-PL', {
            year: 'numeric',
            month: '2-digit',
            day: '2-digit',
            hour: '2-digit',
            minute: '2-digit',
            second: '2-digit'
        });
}

// Update timestamp on load and every 30 seconds
updateTimestamp();
setInterval(updateTimestamp, 30000);

// Refresh button handler
document.getElementById('refresh-btn').addEventListener('click', function() {
    // Simulate refresh with spinner
    const indicator = document.getElementById('loading-indicator');
    indicator.classList.remove('htmx-indicator');

    setTimeout(() => {
        updateTimestamp();
        indicator.classList.add('htmx-indicator');
    }, 1000);
});

// Filtering functionality
function applyFilters() {
    const timestampFilter = document.getElementById('timestamp-filter').value.toLowerCase();
    const authorFilter = document.getElementById('author-filter').value.toLowerCase();
    const processFilter = document.getElementById('process-filter').value.toLowerCase();

    const rows = document.querySelectorAll('#elements-list tr');
    rows.forEach(row => {
        const timestamp = row.querySelector('td:nth-child(1)').textContent.toLowerCase();
        const author = row.querySelector('td:nth-child(2)').textContent.toLowerCase();
        const process = row.querySelector('td:nth-child(3)').textContent.toLowerCase();

        const timestampMatch = timestamp.includes(timestampFilter);
        const authorMatch = author.includes(authorFilter);
        const processMatch = process.includes(processFilter);

        row.style.display = (timestampMatch && authorMatch && processMatch) ? '' : 'none';
    });
}

// Sorting functionality
function sortTable(columnIndex) {
    const table = document.querySelector('table tbody');
    const rows = Array.from(table.querySelectorAll('tr'));

    // Determine sort direction
    const isAscending = (sortState.column === columnIndex && sortState.direction === 'asc') ? false : true;

    // Update sort state
    sortState.column = columnIndex;
    sortState.direction = isAscending ? 'asc' : 'desc';

    // Reset all sort icons
    document.querySelectorAll('.sort-icon').forEach(icon => {
        icon.classList.remove('fa-sort-up', 'fa-sort-down', 'active');
        icon.classList.add('fa-sort');
    });

    // Update current column's sort icon
    const currentHeader = document.querySelectorAll('.sortable')[columnIndex];
    const sortIcon = currentHeader.querySelector('.sort-icon');
    sortIcon.classList.remove('fa-sort');
    sortIcon.classList.add('active');
    sortIcon.classList.add(isAscending ? 'fa-sort-up' : 'fa-sort-down');

    const sortedRows = rows.sort((a, b) => {
        const aValue = a.querySelector(`td:nth-child(${columnIndex + 1})`).textContent.trim();
        const bValue = b.querySelector(`td:nth-child(${columnIndex + 1})`).textContent.trim();

        // Sorting logic for different column types
        const compareValues = (a, b) => {
            switch (columnIndex) {
                case 0: // Timestamp
                    const parseTimestamp = (dateString) => {
                        // Split date and time
                        const [datePart, timePart] = dateString.split(' ');

                        // Parse date parts
                        const [day, month, year] = datePart.split('.');

                        // Parse time parts
                        const [hours, minutes, seconds] = timePart.split(':');

                        // Create Date object (month is 0-indexed in JS Date)
                        return new Date(
                            parseInt(year),
                            parseInt(month) - 1,
                            parseInt(day),
                            parseInt(hours),
                            parseInt(minutes),
                            parseInt(seconds)
                        );
                    };

                    return parseTimestamp(a) - parseTimestamp(b);

                case 1: // Author (text)
                case 2: // Process name (text)
                    return a.localeCompare(b);

                default:
                    return 0;
            }
        };

        // Apply sort direction
        return isAscending
            ? compareValues(aValue, bValue)
            : compareValues(bValue, aValue);
    });

    // Clear and refill tbody
    table.innerHTML = '';
    sortedRows.forEach(row => table.appendChild(row));
}

// Event listeners for filters
document.getElementById('timestamp-filter').addEventListener('input', applyFilters);
document.getElementById('author-filter').addEventListener('input', applyFilters);
document.getElementById('process-filter').addEventListener('input', applyFilters);

// Event listeners for sorting
document.querySelectorAll('.sortable').forEach((header, index) => {
    header.addEventListener('click', () => sortTable(index));
});