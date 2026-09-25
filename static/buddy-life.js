/* EduSphere AI — buddy life: animation, moods, talk sync, petting.
 * Drives the inline-SVG animals from animals.js. Each mounted stage
 * (mini topbar + big hero) is its own living instance:
 *   - mountAnimal(el, buddyId, size) : render + start idle life (bob, blink)
 *   - setTalking(el, bool)           : mouth opens/closes in speech rhythm
 *   - setMood(el, mood, secs)        : excited / confused / celebrate
 *   - petAnimal(el)                  : tap the buddy -> wiggle + hearts
 *   - buddyDance(el, secs)           : celebration dance (stars earned)
 * Talk sync runs a layered-sine pseudo-speech envelope — livelier and
 * more lifelike than a fixed chew loop.
 */
"use strict";

const STAGES = new Map();          // el -> instance state

function _anPart(root, name) {
  return root.querySelector('[data-part="' + name + '"]');
}

function mountAnimal(el, buddyId, size) {
  if (!el) return;
  const st = {
    buddy: buddyId || "leo", size: size || "mini",
    talking: false, talkRAF: null, moodTimer: null, blinkTimer: null,
  };
  STAGES.set(el, st);
  el.innerHTML = animalSVG(st.buddy);
  el.classList.add("an-stage");
  if (size === "hero") el.setAttribute("data-size", "hero");
  _startIdle(el, st);
  return el;
}

function _startIdle(root, st) {
  clearTimeout(st.blinkTimer);
  const body = _anPart(root, "body");
  const tail = _anPart(root, "tail");
  const eyes = root.querySelectorAll(".an-eye");
  // idle bob + tail sway (GPU cheap, no layout)
  let t0 = performance.now();
  const bob = (t) => {
    if (STAGES.get(root) !== st) return;          // stage re-mounted
    const s = (t - t0) / 1000;
    if (body && !root.classList.contains("an-dance"))
      body.style.transform =
        "translateY(" + (Math.sin(s * 2.1 + (st.size === "hero" ? 0 : .7)) * 1.6) + "px)";
    if (tail) {
      tail.style.transformOrigin = "78px 78px";
      tail.style.transform = "rotate(" + (Math.sin(s * 3.4) * 9) + "deg)";
    }
    requestAnimationFrame(bob);
  };
  requestAnimationFrame(bob);
  // blinking (every ~3-5s, both eyes together)
  const blink = () => {
    if (STAGES.get(root) !== st) return;
    eyes.forEach((e) => {
      e.style.transition = "transform .07s";
      e.style.transformOrigin = "center";
      e.style.transform = "scaleY(.08)";
      setTimeout(() => { e.style.transform = "scaleY(1)"; }, 110);
    });
    st.blinkTimer = setTimeout(blink, 2800 + Math.random() * 2600);
  };
  st.blinkTimer = setTimeout(blink, 1600);
}

/* ---- talk sync: lively pseudo-speech mouth ---- */
function setTalking(root, on) {
  const st = root && STAGES.get(root);
  if (!st) return;
  st.talking = !!on;
  cancelAnimationFrame(st.talkRAF);
  const mouth = _anPart(root, "mouth");
  if (!mouth) return;
  const open = mouth.querySelector(".an-mouth-open");
  const line = mouth.querySelector(".an-mouth-line");
  const rest = () => {
    if (open) open.style.opacity = "0";
    if (line) line.style.opacity = "1";
    mouth.style.transform = "";
  };
  if (!on) { rest(); return; }
  if (open) open.style.opacity = "1";
  let t0 = performance.now();
  const talkLoop = (t) => {
    if (!st.talking || STAGES.get(root) !== st) { rest(); return; }
    const s = (t - t0) / 1000;
    // layered sines ~ speech envelope; never fully shut mid-word
    const amp = .5 + .5 * Math.sin(s * 11.3) * Math.sin(s * 4.7 + 1.3);
    const ry = 1 + amp * (parseFloat(mouth.dataset.w || 12) * 0.32);
    if (open) { open.setAttribute("ry", ry.toFixed(2)); open.style.opacity = "1"; }
    if (line) line.style.opacity = String(amp > .45 ? .25 : 1);
    st.talkRAF = requestAnimationFrame(talkLoop);
  };
  st.talkRAF = requestAnimationFrame(talkLoop);
}

/* ---- moods ---- */
function setMood(root, mood, secs) {
  const st = root && STAGES.get(root);
  if (!st) return;
  clearTimeout(st.moodTimer);
  ["an-excited", "an-confused", "an-celebrate"]
    .forEach((c) => root.classList.remove(c));
  const cls = { excited: "an-excited", confused: "an-confused",
    celebrate: "an-celebrate" }[mood];
  if (!cls) return;
  root.classList.add(cls);
  if (mood === "celebrate") _anConfetti(root);
  st.moodTimer = setTimeout(() => root.classList.remove(cls),
    (secs || 2.4) * 1000);
}

/* ---- celebration dance (stars earned) ---- */
function buddyDance(root, secs) {
  if (!root || !STAGES.get(root)) return;
  root.classList.remove("an-dance");
  void root.offsetWidth;                       // restart animation
  root.classList.add("an-dance");
  _anConfetti(root);
  setTimeout(() => root.classList.remove("an-dance"), (secs || 3) * 1000);
}

function _anConfetti(root) {
  const bits = ["✨", "⭐", "🎉", "🌟", "💫", "🎈"];
  for (let i = 0; i < 8; i++) {
    const c = document.createElement("span");
    c.className = "an-confetti";
    c.textContent = bits[i % bits.length];
    c.style.left = (8 + Math.random() * 84) + "%";
    c.style.top = (6 + Math.random() * 30) + "%";
    c.style.setProperty("--dx", (Math.random() * 90 - 45) + "px");
    c.style.animationDelay = (Math.random() * .25) + "s";
    root.appendChild(c);
    setTimeout(() => c.remove(), 1500);
  }
}

/* ---- petting: tap the buddy -> wiggle + hearts ---- */
function petAnimal(root) {
  const st = root && STAGES.get(root);
  if (!st) return;
  root.classList.remove("an-pet");
  void root.offsetWidth;                       // restart the wiggle
  root.classList.add("an-pet");
  const hearts = ["💗", "💛", "💙", "🧡"];
  for (let i = 0; i < 3; i++) {
    const h = document.createElement("span");
    h.className = "an-heart";
    h.textContent = hearts[i % 4];
    h.style.left = (30 + Math.random() * 40) + "%";
    h.style.bottom = "8%";
    h.style.animationDelay = (i * .12) + "s";
    root.appendChild(h);
    setTimeout(() => h.remove(), 1400 + i * 120);
  }
  setTimeout(() => root.classList.remove("an-pet"), 700);
}
