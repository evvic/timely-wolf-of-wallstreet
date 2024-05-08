// URL to open in the new tab
const targetUrl = "https://dailychart.freewebhostmost.com/";

// Create a daily alarm to trigger the new tab opening
chrome.alarms.create("openNewTab", { periodInMinutes: 1440 });

// Listen for the alarm and open the new tab
chrome.alarms.onAlarm.addListener((alarm) => {
  if (alarm.name === "openNewTab") {
    openNewTab();
  }
});

// Function to open a new tab
function openNewTab() {
  chrome.tabs.create({ url: targetUrl });
}

// Listen for the extension icon click and open a new tab
chrome.action.onClicked.addListener(openNewTab);
