// Armazenar em cache os arquivos necessários para a PWA
const CACHE_NAME = 'swot-cache-v1';
const urlsToCache = [
    '/',
    '/formulario/',
    '/swot/',
    '/static/manifest.json',
    // Adicione outros arquivos estáticos que você deseja armazenar em cache
];

// Instalação do service worker
self.addEventListener('install', (event) => {
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then((cache) => {
                return cache.addAll(urlsToCache);
            })
    );
});

// Ativar o service worker
self.addEventListener('activate', (event) => {
    event.waitUntil(
        caches.keys().then((cacheNames) => {
            return Promise.all(
                cacheNames.map((cacheName) => {
                    if (cacheName !== CACHE_NAME) {
                        return caches.delete(cacheName);
                    }
                })
            );
        })
    );
});

// Recuperar recursos do cache
self.addEventListener('fetch', (event) => {
    event.respondWith(
        caches.match(event.request)
            .then((response) => {
                return response || fetch(event.request);
            })
    );
});
