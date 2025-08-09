self.addEventListener('install', event => {
  // Activate immediately without waiting
  self.skipWaiting();
});

self.addEventListener('activate', event => {
  // Take control of pages right away
  event.waitUntil(self.clients.claim());
});

self.addEventListener('fetch', event => {
  // Always go to network first (no offline caching)
  event.respondWith(fetch(event.request).catch(() => new Response('Offline')));
});
