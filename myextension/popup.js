// Listen for messages from background script
chrome.runtime.onMessage.addListener(function(message) {
    if (message.type === 'apiResponse') {
        console.log('Response received in popup:', message.data);
        console.log("222222222");
        const responseDiv = document.getElementById('response');
        responseDiv.textContent = JSON.stringify(message.data, null, 2);
    }
});