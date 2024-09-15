const express = require('express');
const bodyParser = require('body-parser');
const QRCode = require('qrcode');
const fs = require('fs');

const app = express();
const port = 3000;

app.use(bodyParser.json());

app.post('/generate-qrcode', async (req, res) => {
    const { batteryInfo } = req.body;

    try {
        // Generate QR code
        const qrCodeDataUrl = await QRCode.toDataURL(batteryInfo);

        // Save data to JSON file
        const data = { batteryInfo, qrCodeDataUrl };
        fs.writeFileSync('data.json', JSON.stringify(data, null, 2));

        res.json({ message: 'QR code generated and data saved', data });
    } catch (error) {
        res.status(500).json({ message: 'Error generating QR code', error });
    }
});

app.listen(port, () => {
    console.log(`Server running at http://localhost:${port}`);
});