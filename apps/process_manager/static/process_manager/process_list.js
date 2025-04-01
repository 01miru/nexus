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
document.body.addEventListener('htmx:afterOnLoad', function() {
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

    // Reapply sorting after HTMX reload
    if (sortState.column !== null) {
        const table = document.querySelector('#process-table');
        const header = table.querySelector(`th[data-column="${sortState.column}"]`);

        // Reset all sort icons
        document.querySelectorAll('.sort-icon').forEach(icon => {
            icon.classList.remove('fa-sort-up', 'fa-sort-down', 'active', 'fa-sort');
            icon.classList.add('fa-sort');
        });

        // Update current column's sort icon
        const sortIcon = header.querySelector('.sort-icon');
        sortIcon.classList.remove('fa-sort');
        sortIcon.classList.add('active');
        sortIcon.classList.add(sortState.direction === 'asc' ? 'fa-sort-up' : 'fa-sort-down');

        // Re-sort the table
        sortTable(sortState.column, sortState.direction === 'desc');
    }

    // Reapply filters
    applyFilters();
});

// Filtering functionality
function applyFilters() {
    const pidFilter = document.getElementById('pid-filter').value.toLowerCase();
    const statusFilter = document.getElementById('status-filter').value.toLowerCase();
    const nameFilter = document.getElementById('name-filter').value.toLowerCase();

    const rows = document.querySelectorAll('#process-list tr');
    rows.forEach(row => {
        const pid = row.querySelector('td:nth-child(1)').textContent.toLowerCase();
        const status = row.querySelector('td:nth-child(2)').textContent.toLowerCase();
        const name = row.querySelector('td:nth-child(5)').textContent.toLowerCase();

        const pidMatch = pid.includes(pidFilter);
        const statusMatch = !statusFilter || status === statusFilter;
        const nameMatch = name.includes(nameFilter);

        row.style.display = (pidMatch && statusMatch && nameMatch) ? '' : 'none';
    });
}

// Sorting functionality
function sortTable(columnIndex, forceDescending = false) {
    const table = document.querySelector('table tbody');
    const rows = Array.from(table.querySelectorAll('tr'));

    // Determine sort direction
    const isAscending = forceDescending ? false :
        (sortState.column === columnIndex && sortState.direction === 'asc') ? false : true;

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
                case 0: // PID (numbers)
                    return parseInt(a) - parseInt(b);

                case 1: // Status (text)
                    return a.localeCompare(b);

                case 2: // Start Time (custom date format: 28.03.2025 08:03:21)
                    const parseCustomDate = (dateString) => {
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

                    return parseCustomDate(a) - parseCustomDate(b);

                case 3: // Duration
                    const parseDuration = (duration) => {
                        const days = (duration.match(/(\d+)d/) ? parseInt(duration.match(/(\d+)d/)[1]) : 0) * 24 * 60;
                        const hours = (duration.match(/(\d+)h/) ? parseInt(duration.match(/(\d+)h/)[1]) : 0) * 60;
                        const minutes = (duration.match(/(\d+)m/) ? parseInt(duration.match(/(\d+)m/)[1]) : 0);
                        return days + hours + minutes;
                    };
                    return parseDuration(a) - parseDuration(b);

                case 4: // Name (text)
                    return a.localeCompare(b);

                case 5: // Memory Usage (number)
                    return parseFloat(a.replace(' MB', '')) - parseFloat(b.replace(' MB', ''));

                case 6: // CPU Usage (number)
                    return parseFloat(a.replace('%', '')) - parseFloat(b.replace('%', ''));

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
document.getElementById('pid-filter').addEventListener('input', applyFilters);
document.getElementById('status-filter').addEventListener('change', applyFilters);
document.getElementById('name-filter').addEventListener('input', applyFilters);

// Event listeners for sorting
document.querySelectorAll('.sortable').forEach((header, index) => {
    header.addEventListener('click', () => sortTable(index));
});

// Event listener for snapshot button
document.getElementById('snapshot-btn').addEventListener('htmx:afterRequest', function(event) {
    if (event.detail.xhr.status === 200) {
        alert('Snapshot taken successfully!');
    }
});