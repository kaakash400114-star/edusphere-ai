/* EduSphere AI — Magic Tracing: draw A-Z and 1-10 with your finger.
 * The letter shows as a soft dotted guide; the child traces over it.
 * Coverage of the glyph's cell-mask decides success (>=55%) — forgiving,
 * zero-failure feel: the animal cheers for every honest attempt, and
 * "Try again" just clears the canvas.
 */
"use strict";

const TRACE_CHARS = ["A","B","C","D","E","F","G","H","I","J","K","L","M",
  "N","O","P","Q","R","S","T","U","V","W","X","Y","Z",
  "1","2","3","4","5","6","7","8","9","10"];

const Trace = { canvas: null, ctx: null, mask: null, need: 0, hit: 0,
  drawing: false, ch: "", busy: false };

function openTracer(ch) {
  const modal = $("trace-modal");
  modal.classList.remove("hidden");
  $("trace-title").textContent = "✏️ Trace the letter " + ch;
  const cv = $("trace-canvas");
  const size = Math.min(320, Math.floor(Math.min(window.innerWidth * .8, 340)));
  cv.width = size; cv.height = size;
  Trace.canvas = cv;
  Trace.ctx = cv.getContext("2d");
  Trace.ch = ch;
  _buildMask(ch, size);
  _clearTracing();
  animalMood("excited", 1.5);
  speak("Trace the " + (/^[0-9]$/.test(ch) ? "number " : "letter ") + ch +
    " with your finger!", {});
}

function _nextTrace() {
  const i = TRACE_CHARS.indexOf(Trace.ch);
  openTracer(TRACE_CHARS[(i + 1) % TRACE_CHARS.length]);
}

function _buildMask(ch, size) {
  // rasterize the glyph offscreen, then sample a 24x24 grid of filled cells
  const off = document.createElement("canvas");
  off.width = size; off.height = size;
  const c = off.getContext("2d");
  c.fillStyle = "#fff"; c.fillRect(0, 0, size, size);
  c.fillStyle = "#000";
  c.font = "bold " + Math.floor(size * .74) + "px 'Comic Sans MS', sans-serif";
  c.textAlign = "center"; c.textBaseline = "middle";
  c.fillText(ch, size / 2, size / 2 + size * .04);
  const img = c.getImageData(0, 0, size, size).data;
  const G = 24, cells = new Set();
  for (let gy = 0; gy < G; gy++) {
    for (let gx = 0; gx < G; gx++) {
      const x0 = Math.floor(gx * size / G), y0 = Math.floor(gy * size / G);
      const x1 = Math.floor((gx + 1) * size / G), y1 = Math.floor((gy + 1) * size / G);
      let filled = 0, tot = 0;
      for (let y = y0; y < y1; y += 2) for (let x = x0; x < x1; x += 2) {
        tot++;
        if (img[(y * size + x) * 4] < 128) filled++;
      }
      if (tot && filled / tot > .28) cells.add(gy * G + gx);
    }
  }
  Trace.mask = cells;
  Trace.need = cells.size;
  Trace.hit = 0;
  Trace.seen = new Set();
  Trace.G = G;
}

function _clearTracing() {
  const cv = Trace.canvas, ctx = Trace.ctx, size = cv.width;
  ctx.clearRect(0, 0, size, size);
  _drawGuide(size);
  Trace.hit = 0; Trace.seen = new Set();
  $("trace-progress").style.width = "0%";
  $("trace-done").classList.add("hidden");
  $("trace-msg").textContent = "Use your finger — follow the dots!";
}

function _drawGuide(size) {
  const ctx = Trace.ctx, G = Trace.G || 24;
  // dotted guide from the mask
  ctx.save();
  ctx.fillStyle = "#c7d2fe";
  Trace.mask.forEach((cell) => {
    const gx = cell % G, gy = Math.floor(cell / G);
    ctx.beginPath();
    ctx.arc((gx + .5) * size / G, (gy + .5) * size / G, size / G * .22, 0, 7);
    ctx.fill();
  });
  // start dot
  const first = Math.min(...Trace.mask);
  if (isFinite(first)) {
    ctx.fillStyle = "#22c55e";
    ctx.beginPath();
    ctx.arc(((first % G) + .5) * size / G, (Math.floor(first / G) + .5) * size / G,
      size / G * .5, 0, 7);
    ctx.fill();
  }
  ctx.restore();
}

function _tracePos(e) {
  const r = Trace.canvas.getBoundingClientRect();
  const p = e.touches ? e.touches[0] : e;
  return { x: (p.clientX - r.left) * Trace.canvas.width / r.width,
           y: (p.clientY - r.top) * Trace.canvas.height / r.height };
}

function _traceMove(e) {
  if (!Trace.drawing) return;
  e.preventDefault();
  const { x, y } = _tracePos(e);
  const ctx = Trace.ctx, size = Trace.canvas.width;
  ctx.fillStyle = "#f472b6";
  ctx.beginPath(); ctx.arc(x, y, size / 26, 0, 7); ctx.fill();
  const G = Trace.G;
  const gx = Math.floor(x * G / size), gy = Math.floor(y * G / size);
  const cell = gy * G + gx;
  for (const c of [cell, cell + 1, cell - 1, cell + G, cell - G]) {
    if (Trace.mask.has(c) && !Trace.seen.has(c)) {
      Trace.seen.add(c); Trace.hit++;
    }
  }
  const pct = Math.min(100, Math.round(Trace.hit / Math.max(1, Trace.need) * 100));
  $("trace-progress").style.width = pct + "%";
  if (pct >= 55 && !Trace.busy) {
    Trace.busy = true;
    $("trace-msg").textContent = "🎉 Beautiful " + Trace.ch + "!";
    $("trace-done").classList.remove("hidden");
    animalMood("dance", 2.5);
    speak("Wow! Beautiful " + (/^[0-9]$/.test(Trace.ch) ? "number " : "letter ")
      + Trace.ch + "! You did it!", {});
    finishKinderRound("tracing", 1, 1);
    setTimeout(() => { Trace.busy = false; }, 800);
  }
}

function wireTracer() {
  const cv = $("trace-canvas");
  const down = (e) => { Trace.drawing = true; _traceMove(e); };
  const move = (e) => { if (Trace.drawing) _traceMove(e); };
  const up = () => { Trace.drawing = false; };
  cv.addEventListener("mousedown", down); cv.addEventListener("touchstart", down, { passive: false });
  window.addEventListener("mousemove", move); cv.addEventListener("touchmove", move, { passive: false });
  window.addEventListener("mouseup", up); window.addEventListener("touchend", up);
  $("trace-x").onclick = () => $("trace-modal").classList.add("hidden");
  $("trace-clear").onclick = _clearTracing;
  $("trace-next").onclick = _nextTrace;
}
