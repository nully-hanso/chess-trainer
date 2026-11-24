// 오프라인용 서비스 워커: 한 번 열어 두면 인터넷이 없어도 열려요.
// 인터넷이 될 때는 항상 새 버전을 받아 와서 저장하고, 안 되면 저장해 둔 것을 보여 줘요.
const CACHE = 'chess-v25';
const FILES = ['./', './index.html', './manifest.json', './icon-180.png', './icon-192.png', './icon-512.png', './story.js','./voice/index.json', './vendor/gsap.min.js', ...['p','n','b','r','q','k'].flatMap(t => ['w','b'].map(c => './pieces/' + c + t + '.svg'))];

self.addEventListener('install', e => {
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(FILES)).then(() => self.skipWaiting()));
});
self.addEventListener('activate', e => {
  e.waitUntil(caches.keys()
    .then(keys => Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k))))
    .then(() => self.clients.claim()));
});
self.addEventListener('fetch', e => {
  const req = e.request;
  if (req.method !== 'GET' || new URL(req.url).origin !== location.origin) return;
  e.respondWith(
    fetch(req).then(res => {
      if (res.ok) { const copy = res.clone(); caches.open(CACHE).then(c => c.put(req, copy)); }
      return res;
    }).catch(() => caches.match(req, { ignoreSearch: true }).then(r => r || caches.match('./index.html')))
  );
});
