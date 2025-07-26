const CACHE_NAME = 'gatewaymagnet-cache-v1';
const STATIC_ASSETS = [
  '/',                    // Homepage
  '/dashboard/',          // User dashboard
  '/accounts/login/',     // Login page
  '/post-login/',         // Redirect after login
  '/offline/',            // Fallback offline page (optional)

  // Static files - ensure these match your actual file paths
  '/static/tabler/css/tabler.min.css',
  '/static/tabler/js/tabler.min.js',
  '/static/images/church_logo.png',
];

// Install – Cache static assets
self.addEventListener('install', (event) => {
  console.log('[ServiceWorker] Install event');
  event.waitUntil(
    caches.open(CACHE_NAME).then(async (cache) => {
      for (const asset of STATIC_ASSETS) {
        try {
          await cache.add(asset);
        } catch (err) {
          console.warn(`[ServiceWorker] Caching failed for: ${asset}`, err);
        }
      }
    })
  );
  self.skipWaiting();
});

// Activate – Clean up old caches
self.addEventListener('activate', (event) => {
  console.log('[ServiceWorker] Activate event');
  event.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(
        keys.filter((key) => key !== CACHE_NAME).map((key) => caches.delete(key))
      )
    )
  );
  self.clients.claim();
});

// Fetch – Serve from cache first, fallback to network
self.addEventListener('fetch', (event) => {
  event.respondWith(
    caches.match(event.request).then((cachedResponse) => {
      return (
        cachedResponse ||
        fetch(event.request).catch(() =>
          caches.match('/offline/')
        )
      );
    })
  );
});
