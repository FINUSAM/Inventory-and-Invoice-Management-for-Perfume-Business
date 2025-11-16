

let deferredPrompt; // Store the install prompt
let alreadyPrompted = 1000; // Show after 3 seconds for the first prompt

function show_addToHomeScreen(wait_time) {
  setTimeout(() => {
    document.getElementById('addToHomeScreenContainer').classList.add('show');
  }, wait_time);
}

// Detect if the user is on an iOS device
function isIos() {
  const userAgent = window.navigator.userAgent.toLowerCase();
  return /iphone|ipad|ipod/.test(userAgent);
}

// Check if the app is already installed in standalone mode
function isInStandaloneMode() {
  return window.navigator.standalone === true || window.matchMedia('(display-mode: standalone)').matches;
}

if (isIos() && !isInStandaloneMode()) {
  // Show a custom iOS install prompt
  console.log('Showing iOS A2HS prompt');
  show_addToHomeScreen(alreadyPrompted);
  alreadyPrompted = 1 * 1000; // Show after 10 seconds after the first prompt
} else {
  // Handle Android/Windows A2HS using beforeinstallprompt
  window.addEventListener('beforeinstallprompt', (e) => {
    e.preventDefault(); // Prevent the default browser prompt
    deferredPrompt = e; // Stash the event so it can be triggered later

    console.log('beforeinstallprompt called');

    // Show the addToHomeScreenContainer after a delay or user interaction
    show_addToHomeScreen(alreadyPrompted);
    alreadyPrompted = 1 * 1000; // Show after 10 seconds after first prompt
  });
}

// Event handler for the "Add to Home Screen" button
document.getElementById('addToHomeScreenButton').addEventListener('click', (e) => {
  if (isIos()) {
    console.log('iOS users must use the Share menu to add to home screen');
    alert('To add this app to your home screen, tap the Share icon and select "Add to Home Screen".');
  } else if (deferredPrompt) {
    deferredPrompt.prompt(); // Show the install prompt

    deferredPrompt.userChoice.then((choiceResult) => {
      if (choiceResult.outcome === 'accepted') {
        console.log('User accepted the A2HS prompt');
      } else {
        console.log('User dismissed the A2HS prompt');
      }
      deferredPrompt = null; // Reset the deferred prompt variable
    });
  }

  // Hide the button after it's clicked
  document.getElementById('addToHomeScreenContainer').classList.remove('show');
});

// Event handler for the "Close" button
document.getElementById('close_addToHomeScreenButton').addEventListener('click', (e) => {
  console.log('User closed the addToHomeScreen');
  document.getElementById('addToHomeScreenContainer').classList.remove('show');
  // You might want to show it again after a longer delay, e.g., 60 seconds
  show_addToHomeScreen(1 * 1000);
});


