// Function to fetch and display top 10 rows
async function displayTop10Rows() {
    try {
        // Fetch data from the endpoint
        const response = await fetch('/get_top_10');
        const data = await response.json();

        // Get the container element where we'll display the data
        const container = document.getElementById('data-container');
        
        // Clear any existing content
        container.innerHTML = '';

        // Create and populate the table
        const table = document.createElement('table');
        table.className = 'data-table';

        // Create table header
        const thead = document.createElement('thead');
        const headerRow = document.createElement('tr');
        
        // Assuming data[0] contains our first row with all columns
        if (data.length > 0) {
            Object.keys(data[0]).forEach(key => {
                const th = document.createElement('th');
                th.textContent = key;
                headerRow.appendChild(th);
            });
        }
        
        thead.appendChild(headerRow);
        table.appendChild(thead);

        // Create table body
        const tbody = document.createElement('tbody');
        data.forEach(row => {
            const tr = document.createElement('tr');
            Object.values(row).forEach(value => {
                const td = document.createElement('td');
                td.textContent = value;
                tr.appendChild(td);
            });
            tbody.appendChild(tr);
        });

        table.appendChild(tbody);
        container.appendChild(table);

    } catch (error) {
        console.error('Error fetching data:', error);
        document.getElementById('data-container').innerHTML = 'Error loading data';
    }
}

// Call the function when the page loads
document.addEventListener('DOMContentLoaded', displayTop10Rows);