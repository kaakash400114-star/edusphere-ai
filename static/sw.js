/* EduSphere AI service worker — app-shell & CDN asset caching for offline opens. */
const CACHE = "edusphere-v15"; /* v15: KaTeX + Mermaid offline cache + streaming + study tools */
const SHELL = [
  "/", "/index.html", "/manifest.json",
  "/animals.js", "/buddy-life.js", "/buddy-actions.js", "/kinder.js", "/tracing.js",
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

  // CDN caching for KaTeX and Mermaid (supports offline math & diagrams)
  if (url.hostname.includes("jsdelivr.net") || url.pathname.endsWith(".woff2") || url.pathname.endsWith(".ttf")) {
    event.respondWith(
      caches.match(event.request).then((hit) => {
        if (hit) return hit;
        return fetch(event.request).then((res) => {
          if (res && res.ok) {
            const copy = res.clone();
            caches.open(CACHE).then((c) => c.put(event.request, copy));
          }
          return res;
        }).catch(() => hit);
      })
    );
    return;
  }

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
