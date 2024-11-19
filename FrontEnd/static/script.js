async function fetchResidueTypes() {
    try {
        console.log('Fetching residue types...'); // Debugging statement
        const response = await fetch('http://127.0.0.1:5001/api/residue_types/');
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        const data = await response.json();
        console.log('Fetched residue types:', data); // Debugging statement
        const residueTypeSelect = document.getElementById('residueTypeSelect');
        const barResidueTypeCheckboxes = document.getElementById('barResidueTypeCheckboxes');
        data.forEach(type => {
            const option = document.createElement('option');
            option.value = type;
            option.text = type;
            residueTypeSelect.appendChild(option);

            const checkbox = document.createElement('input');
            checkbox.type = 'checkbox';
            checkbox.value = type;
            checkbox.id = `checkbox-${type}`;
            checkbox.name = 'residueTypes';
            const label = document.createElement('label');
            label.htmlFor = `checkbox-${type}`;
            label.appendChild(document.createTextNode(type));
            barResidueTypeCheckboxes.appendChild(checkbox);
            barResidueTypeCheckboxes.appendChild(label);
            barResidueTypeCheckboxes.appendChild(document.createElement('br'));
        });
        console.log('Dropdown options and checkboxes added:', residueTypeSelect.options); // Debugging statement
        updateGraph(); // Display the initial graph
    } catch (error) {
        console.error('Failed to fetch residue types:', error);
    }
}

async function updateGraph() {
    const residueType = document.getElementById('residueTypeSelect').value;
    const timeRange = document.getElementById('timeRangeSelect').value;

    try {
        console.log('Generating graph...'); // Debugging statement
        const response = await fetch('http://127.0.0.1:5001/api/generate_graph', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ residue_type: residueType, time_range: timeRange })
        });

        if (response.ok) {
            const data = await response.json();
            const img = document.getElementById('graphImage');
            img.src = `http://127.0.0.1:5001/api/images/${data.filename}?t=${new Date().getTime()}`;
            img.style.display = 'block';
            console.log('Graph generated successfully'); // Debugging statement
        } else {
            console.error('Failed to generate graph');
        }
    } catch (error) {
        console.error('Error generating graph:', error);
    }
}

async function updateBarChart() {
    const residueTypes = Array.from(document.querySelectorAll('input[name="residueTypes"]:checked')).map(checkbox => checkbox.value);
    const timeRange = document.getElementById('barTimeRangeSelect').value;

    try {
        console.log('Generating bar chart...'); // Debugging statement
        const response = await fetch('http://127.0.0.1:5001/api/generate_bar_chart', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ residue_types: residueTypes, time_range: timeRange })
        });

        if (response.ok) {
            const data = await response.json();
            const img = document.getElementById('barChartImage');
            img.src = `http://127.0.0.1:5001/api/images/${data.filename}?t=${new Date().getTime()}`;
            img.style.display = 'block';
            console.log('Bar chart generated successfully'); // Debugging statement
        } else {
            console.error('Failed to generate bar chart');
        }
    } catch (error) {
        console.error('Error generating bar chart:', error);
    }
}

// Populate residue types on page load
document.addEventListener('DOMContentLoaded', fetchResidueTypes);