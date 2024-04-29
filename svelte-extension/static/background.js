chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.type === 'save-data') {
        const { counter, symbol, num_weeks } = request.data;
        chrome.storage.local.set({ counter, symbol, num_weeks });
        sendResponse({ message: 'Data saved successfully!' });
    }
});