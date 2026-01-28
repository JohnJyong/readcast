document.getElementById('addBtn').addEventListener('click', async () => {
    const statusDiv = document.getElementById('status');
    statusDiv.textContent = "Processing...";
    
    // Get current tab
    let [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    
    if (!tab) {
        statusDiv.textContent = "Error: No active tab.";
        return;
    }

    const url = tab.url;
    
    try {
        const response = await fetch('http://127.0.0.1:8000/ingest', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ url: url, source: "chrome-extension" })
        });

        if (response.ok) {
            statusDiv.textContent = "✅ Added to Queue!";
            statusDiv.style.color = "green";
        } else {
            statusDiv.textContent = "❌ Error: " + response.statusText;
            statusDiv.style.color = "red";
        }
    } catch (error) {
        statusDiv.textContent = "❌ Connection Failed. Is ReadCast running?";
        statusDiv.style.color = "red";
    }
});
