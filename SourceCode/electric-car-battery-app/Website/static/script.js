document.getElementById('batteryForm').addEventListener('submit', async function(event) {
    event.preventDefault();

    const batteryInfo = {
        model: document.getElementById('model').value,
        capacity: document.getElementById('capacity').value,
        voltage: document.getElementById('voltage').value,
        manufacturer: document.getElementById('manufacturer').value
    };

    // Send data to backend API
    const response = await fetch('http://192.168.1.77:3000/generate-qrcode', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(batteryInfo)
    });

    if (response.ok) {
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.style.display = 'none';
        a.href = url;
        a.download = 'qrcode.png';
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
    } else {
        console.error('Failed to generate QR code');
    }
});