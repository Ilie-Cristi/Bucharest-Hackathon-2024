
function checkAPIEndpoint() {
    fetch('http://localhost:8080/')
        .then(response => {
            // Check if the response is successful (status code 200)
            if (response.ok) {
                // API endpoint is reachable, show a success notification
                chrome.notifications.create({
                    type: 'basic',
                    iconUrl: 'hello_extensions.png',
                    title: 'API Status',
                    message: 'API endpoint is reachable!',
                });
            } else {
                // API endpoint is not reachable, show an error notification
                chrome.notifications.create({
                    type: 'basic',
                    iconUrl: 'hello_extensions.png',
                    title: 'API Status',
                    message: 'API endpoint is unreachable!',
                });
            }
        })
        .catch(error => {
            // Error occurred while making the request, show an error notification
            chrome.notifications.create({
                type: 'basic',
                iconUrl: 'hello_extensions.png',
                title: 'API Status',
                message: 'Error occurred while checking API endpoint!',
            });
        });
}



// Function to handle the context menu item click
function onContextMenuClicked(info, tab) {
    if (info.menuItemId === "checkAPI") {
        // Call the function to check the API endpoint
        checkAPIEndpoint();
    }
}


// Create the context menu item
chrome.contextMenus.create({
    id: "checkAPI",
    title: "Check API Endpoint",
    contexts: ["page"]
});

// Add listener for context menu item click
chrome.contextMenus.onClicked.addListener(onContextMenuClicked);