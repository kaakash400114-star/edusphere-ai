/* EduSphere AI service worker — app-shell caching for offline opens. */
const CACHE = "edusphere-v2";
const SHELL = [
  "/", "/index.html", "/manifest.json",
  "/icon-192.png", "/icon-512.png", "/favicon.svg",
];

self.addEventListener("install", (event) => {
  event.waitUntil(
    caches.open(CACHE).then((c) => c.addAll(SHELL)).then(() => self.skipWaiting())
  );
});

self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches.keys()
      .then((keys) => Promise.all(keys.filter((k) => k !== CACHE)
        .map((k) => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener("fetch", (event) => {
  const url = new URL(event.request.url);
  if (event.request.method !== "GET") return;           // never cache API POSTs
  if (url.pathname.startsWith("/api/")) return;         // always live

  // static + shell: cache-first, refresh in background
  event.respondWith(
    caches.match(event.request).then((hit) => {
      const fetcher = fetch(event.request).then((res) => {
        if (res && res.ok && url.origin === location.origin) {
          const copy = res.clone();
          caches.open(CACHE).then((c) => c.put(event.request, copy));
        }
        return res;
      }).catch(() => hit);
      return hit || fetcher;
    })
  );
});
