// static/js/sw.js
self.addEventListener('install', event => {
  self.skipWaiting(); // activate immediately
});

self.addEventListener('activate', event => {
  event.waitUntil(self.clients.claim());
});
