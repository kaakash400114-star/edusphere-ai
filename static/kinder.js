/* EduSphere AI — Kinder Corner: voice-first tap games (KG).
 * Round = 5 tasks from the server (phonics, counting, shapes, colors,
 * rhymes). Every task is FULLY SPOKEN by the buddy (word-highlighted
 * karaoke bubble) and answered by BIG TAPS — no reading, no typing.
 * Wrong taps just wiggle (no failure). Finishing a round posts
 * /api/kinder/{pid}/finish (+2 points first correct round of the day).
 */
"use strict";

const Kinder = { tasks: [], i: 0, correct: 0, open: false };

async function openKinder() {
  const modal = $("kinder-modal");
  modal.classList.remove("hidden");
  Kinder.open = true;
  const list = $("kinder-home"), play = $("kinder-play");
  list.classList.remove("hidden");
  play.classList.add("hidden");
  try {
    const r = await fetch("/api/kinder/" + state.pid);
    if (!r.ok) throw 0;
    const d = await r.json();
    $("kinder-points").textContent = "💠 " + d.points +
      " points · 5 games · every round wins points!";
    Kinder.allTasks = d.tasks || [];
    const grid = $("kinder-grid");
    grid.innerHTML = "";
    Object.entries(d.games || {}).forEach(([kind, g]) => {
      const card = document.createElement("button");
      card.type = "button";
      card.className = "game-card";
      card.dataset.subject = kind === "phonics" || kind === "rhymes" ? "english" : "math";
      card.innerHTML = `<span class="em">${g.emoji}</span><span class="nm">${g.name}</span>` +
        `<span class="tg">tap & learn</span>`;
      card.onclick = () => startKinderKind(kind);
      grid.appendChild(card);
    });
    const mix = document.createElement("button");
    mix.type = "button";
    mix.className = "btn-primary";
    mix.style.marginTop = "10px";
    mix.textContent = "🎲 Play everything (5 games)";
    mix.onclick = () => startKinderRound();
    list.appendChild(mix);
  } catch (e) {
    $("kinder-points").textContent = "Could not load — check the connection.";
  }
}

function _kinderCard(task) {
  return `<div class="kinder-display">${task.display || task.emoji}</div>`;
}

function startKinderRound() {
  Kinder.tasks = (Kinder.allTasks || []).slice();
  Kinder.i = 0; Kinder.correct = 0;
  $("kinder-home").classList.add("hidden");
  $("kinder-play").classList.remove("hidden");
  showKinderTask();
}

async function startKinderKind(kind) {
  try {
    const r = await fetch("/api/kinder/" + state.pid + "/" + kind);
    const d = await r.json();
    Kinder.tasks = d.tasks || [];
  } catch (e) { Kinder.tasks = []; }
  Kinder.i = 0; Kinder.correct = 0;
  $("kinder-home").classList.add("hidden");
  $("kinder-play").classList.remove("hidden");
  showKinderTask();
}

function showKinderTask() {
  const t = Kinder.tasks[Kinder.i];
  if (!t) return finishKinderUI();
  $("kinder-qnum").textContent = `${Kinder.i + 1} / ${Kinder.tasks.length}`;
  const stage = $("kinder-stage");
  stage.innerHTML = _kinderCard(t);
  // karaoke spoken prompt: buddy says it, words light up
  karaokeSpeak(t.prompt, "kinder-karaoke", () => {
    if (state.profile && state.profile.voice_on !== false) {} // spoken already
  });
  const box = $("kinder-opts");
  box.innerHTML = "";
  (t.options || []).forEach((o) => {
    const b = document.createElement("button");
    b.className = "kinder-opt";
    b.textContent = o.text;
    b.onclick = () => {
      if (o.id === t.answer) {
        Kinder.correct++;
        b.classList.add("kinder-right");
        animalMood("celebrate", 1.4);
        cheerBuddy();
        speak(pickCheer(), {});
      } else {
        b.classList.add("kinder-wrong");
        animalMood("confused", 1);
        // gentle: say the right one after a wiggle
        setTimeout(() => {
          const right = (t.options || []).find(x => x.id === t.answer);
          if (right) speak("This one is " + right.text + ". " + t.say, {});
        }, 900);
      }
      [...box.children].forEach(x => x.disabled = true);
      setTimeout(() => { Kinder.i++; showKinderTask(); }, 1900);
    };
    box.appendChild(b);
  });
}

const CHEERS = ["Yay! You got it!", "Wow, amazing!", "High five! Correct!",
  "You are so clever!", "Roar-some! Correct!"];
function pickCheer() { return CHEERS[Math.random() * CHEERS.length | 0]; }

function finishKinderUI() {
  const t = Kinder.tasks[Kinder.i - 1];
  const kind = t ? t.kind : "mixed";
  finishKinderRound(kind, Kinder.correct, Kinder.tasks.length);
  $("kinder-stage").innerHTML =
    `<div class="kinder-display">🎉</div>` +
    `<div style="font-weight:800;font-size:1.2rem;margin:4px 0">` +
    `${Kinder.correct} / ${Kinder.tasks.length} — hooray!</div>`;
  $("kinder-opts").innerHTML = "";
  $("kinder-karaoke").innerHTML = "";
  animalMood("dance", 3);
  speak("Hooray! You finished! " + Kinder.correct + " out of " +
    Kinder.tasks.length + "!", {});
  const again = document.createElement("button");
  again.className = "btn-primary";
  again.textContent = "🔁 Play again";
  again.onclick = () => { $("kinder-home").classList.remove("hidden");
    $("kinder-play").classList.add("hidden"); openKinder(); };
  $("kinder-opts").appendChild(again);
}

async function finishKinderRound(kind, correct, total) {
  try {
    const r = await fetch("/api/kinder/" + state.pid + "/finish", {
      method: "POST", headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ kind, correct, total }),
    });
    if (!r.ok) return;
    const d = await r.json();
    state.profile = d.profile;
    updatePointsBadge();
    if (d.result && d.result.points_awarded > 0) flyStar($("points-badge"));
  } catch (e) {}
}

function cheerBuddy() { /* animalMood covers the visuals; kept for hooks */ }

function wireKinder() {
  $("kinder-x").onclick = () => { Kinder.open = false;
    $("kinder-modal").classList.add("hidden"); };
}
// kinder.js's opener name; index.html wires the button to openKinderCorner
function openKinderCorner() { return openKinder(); }

function openTracing() {
  // kinder-friendly menu: pick a letter or number to trace
  const modal = $("trace-modal");
  modal.classList.remove("hidden");
  const title = $("trace-title");
  title.textContent = "✏️ Magic Tracing";
  const cv = $("trace-canvas");
  const msg = $("trace-msg");
  // simple picker row injected above the canvas
  let pick = $("trace-pick");
  if (!pick) {
    pick = document.createElement("div");
    pick.id = "trace-pick";
    pick.style.cssText = "display:flex;gap:6px;flex-wrap:wrap;justify-content:center;margin:8px 0";
    cv.parentNode.insertBefore(pick, cv);
  }
  pick.innerHTML = "";
  const addBtns = (chars) => chars.forEach((ch) => {
    const b = document.createElement("button");
    b.className = "kinder-opt";
    b.style.cssText = "min-width:44px;padding:10px 12px;font-size:1.05rem";
    b.textContent = ch;
    b.onclick = () => openTracer(ch);
    pick.appendChild(b);
  });
  const l = document.createElement("span");
  l.textContent = "Letters:";
  l.style.cssText = "width:100%;font-weight:800;color:#6366f1;font-size:.85rem";
  const n = document.createElement("span");
  n.textContent = "Numbers:";
  n.style.cssText = "width:100%;font-weight:800;color:#ec4899;font-size:.85rem";
  pick.appendChild(l);
  addBtns("ABCDEFG".split(""));
  pick.appendChild(n);
  addBtns("12345".split(""));
  cv.style.display = "none";
  $(".trace-bar").style.display = "none";
  msg.textContent = "Tap a letter or number to trace it! 👆";
  $("trace-next").style.display = "none";
  $("trace-clear").style.display = "none";
}

// (openTracer from tracing.js takes over once a character is picked —
// restore the hidden UI there)
const _openTracerBase = openTracer;
openTracer = function (ch) {
  const cv = $("trace-canvas");
  const pick = $("trace-pick");
  if (pick) pick.style.display = "none";
  cv.style.display = "block";
  document.querySelector(".trace-bar").style.display = "block";
  $("trace-next").style.display = "";
  $("trace-clear").style.display = "";
  $("trace-title").textContent = "✏️ Trace!";
  _openTracerBase(ch);
};
