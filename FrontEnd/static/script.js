async function fetchResidueTypes() {
    try {
        console.log('Fetching residue types...'); // Debugging statement
        const response = await fetch('http://127.0.0.1:5001/api/residue_types/');
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        const data = await response.json();
        console.log('Fetched residue types:', data); // Debugging statement
        const residueTypeSelect = document.getElementById('residueType');
        data.forEach(type => {
            const option = document.createElement('option');
            option.value = type;
            option.text = type;
            residueTypeSelect.appendChild(option);
        });
        console.log('Dropdown options added:', residueTypeSelect.options); // Debugging statement
    } catch (error) {
        console.error('Failed to fetch residue types:', error);
    }
}

async function generateGraph() {
    const residueType = document.getElementById('residueType').value;
    const startDate = document.getElementById('startDate').value;
    const endDate = document.getElementById('endDate').value;

    try {
        console.log('Generating graph...'); // Debugging statement
        const response = await fetch('http://127.0.0.1:5001/api/generate_graph', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ residue_type: residueType, start_date: startDate, end_date: endDate })
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

async function fetchAndDisplayGraphs() {
    try {
        const response = await fetch('http://127.0.0.1:5001/api/residue_types/');
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        const residueTypes = await response.json();
        const graphsContainer = document.getElementById('graphsContainer');
        graphsContainer.innerHTML = ''; // Clear any existing content

        for (const type of residueTypes) {
            const graphResponse = await fetch('http://127.0.0.1:5001/api/generate_graph', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ residue_type: type, start_date: '2020-01-01', end_date: '2023-12-31' })
            });

            if (graphResponse.ok) {
                const data = await graphResponse.json();
                const img = document.createElement('img');
                img.src = `http://127.0.0.1:5001/api/images/${data.filename}?t=${new Date().getTime()}`;
                img.alt = `Graph for ${type}`;
                img.onerror = () => {
                    img.style.display = 'none';
                    console.error(`Image not found for ${type}`);
                };
                graphsContainer.appendChild(img);
            } else {
                console.error(`Failed to generate graph for ${type}`);
            }
        }
    } catch (error) {
        console.error('Error fetching and displaying graphs:', error);
    }
}

// Populate residue types on page load
document.addEventListener('DOMContentLoaded', fetchResidueTypes);

// Populate graphs on page load
document.addEventListener('DOMContentLoaded', fetchAndDisplayGraphs);