// static/js/sw.js
self.addEventListener('install', event => {
  console.log('Service Worker installed');
  self.skipWaiting(); // optional, activates immediately
});

self.addEventListener('activate', event => {
  console.log('Service Worker activated');
  // no clients.claim() needed
});
