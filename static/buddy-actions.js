/* EduSphere AI — living-buddy ACTION DIRECTOR (KG–2 only).
 * The buddy ACTS WHILE TALKING: wave, point, count, think, jump, cheer,
 * dance, nod, look around, sniff — chosen from what the buddy is saying
 * (keywords first, playful random otherwise) and timed to the speech.
 * Drives CSS keyframe classes on the stage; body parts carry
 * transform-box: fill-box so every animal animates with one rule set.
 * API:
 *   buddyAct(root, name, secs)   start one named action
 *   buddyActStop(root)           clear every action class
 *   actWhileSpeaking(root, text, opts)   full speech: pick + schedule
 * Everything is guarded: no stage, grade > 2 -> no-op.
 */
"use strict";

const AN_ACTIONS = {
  wave:    { dur: 1.8 },
  point:   { dur: 1.6 },
  count:   { dur: 2.2 },
  think:   { dur: 2.2 },
  jump:    { dur: 1.2 },
  cheer:   { dur: 1.8 },
  dance:   { dur: 2.4 },
  nod:     { dur: 1.4 },
  look:    { dur: 2.2 },
  sniff:   { dur: 1.6 },
};

/* keyword -> action, checked in order (first hit wins for the opener) */
const AN_KEYWORDS = [
  [/\b(hi|hello|hey|welcome|morning|namaste)\b/i, "wave"],
  [/\b(look|see|watch|find|here|this one)\b/i, "point"],
  [/\b(count|how many|number|numbers|one|two|three|four|five|six|seven|eight|nine|ten|add|plus|math)\b/i, "count"],
  [/\b(why|think|wonder|maybe|hmm|guess|puzzle|riddle)\b/i, "think"],
  [/\b(yay|hooray|great|amazing|correct|well done|proud|brilliant|super)\b/i, "cheer"],
  [/\b(dance|party|celebrate|finish|finished)\b/i, "dance"],
  [/\b(yes|right|exactly|true)\b/i, "nod"],
  [/\b(story|once upon|listen|imagine)\b/i, "look"],
  [/\b(smell|flower|sniff)\b/i, "sniff"],
  [/\b(jump|hop|bounce)\b/i, "jump"],
];

const AN_STAGE = new WeakMap();     // root -> {timers:[]}

function _gradeLittle() {
  try {
    const p = (typeof state !== "undefined" && state && state.profile) || null;
    return !!(p && (p.grade <= 2));
  } catch (e) { return false; }
}

function _acting(root) {
  return Object.keys(AN_ACTIONS).some((k) =>
    root.classList.contains("an-" + k));
}

/* start one action; returns true if it actually started */
function buddyAct(root, name, secs) {
  if (!root || !AN_ACTIONS[name]) return false;
  if (root.classList.contains("an-dance")) return false;  // star dance wins
  buddyActStop(root);
  root.classList.add("an-" + name);
  root.classList.add("an-acting");
  const st = AN_STAGE.get(root) || { timers: [] };
  AN_STAGE.set(root, st);
  st.timers.push(setTimeout(() => {
    root.classList.remove("an-" + name);
    if (!_acting(root)) root.classList.remove("an-acting");
  }, (secs || AN_ACTIONS[name].dur) * 1000));
  return true;
}

function buddyActStop(root) {
  if (!root) return;
  const st = AN_STAGE.get(root);
  if (st && st.timers) { st.timers.forEach(clearTimeout); st.timers = []; }
  Object.keys(AN_ACTIONS).forEach((k) => root.classList.remove("an-" + k));
  root.classList.remove("an-acting");
}

function _pickAction(text) {
  for (const [re, act] of AN_KEYWORDS) {
    try { if (re.test(text)) return act; } catch (e) {}
  }
  const pool = ["wave", "point", "count", "think", "nod", "look", "sniff", "jump"];
  return pool[Math.random() * pool.length | 0];
}

/* Full speech: opener from keywords, then follow-ups spread across the
 * estimated speaking time (kids' TTS ~2.3 words/sec), ending on a high. */
function actWhileSpeaking(root, text, opts = {}) {
  if (!root || !_gradeLittle()) return;
  if (typeof text !== "string" || !text.trim()) return;
  if (opts.onEnd) {
    const oldEnd = opts.onEnd;
    opts.onEnd = () => { buddyActStop(root); oldEnd(); };
  } else {
    opts.onEnd = () => buddyActStop(root);
  }
  if (root.classList.contains("an-dance")) return;   // mid-celebration
  const words = text.trim().split(/\s+/).length;
  const est = Math.max(2.5, words / 2.3);
  const opener = _pickAction(text);
  buddyAct(root, opener, Math.min(opener === "think" ? 2.6 : 2.0, est));
  const st = AN_STAGE.get(root);
  const sched = [];
  if (est > 5) sched.push(["look", est * 0.45, 2.0]);
  if (est > 8) {
    sched.push([opener === "point" ? "nod" : "point", est * 0.72, 1.6]);
  }
  if (/[!]|\b(great|wow|yay|correct|amazing|hooray)\b/i.test(text) &&
      opener !== "cheer" && opener !== "dance") {
    sched.push(["cheer", Math.max(1, est - 1.9), 1.8]);
  }
  sched.forEach(([act, at, dur]) => {
    st.timers.push(setTimeout(() => {
      try {
        if (typeof Buddy === "undefined" || !Buddy.speaking) return;
      } catch (e) { return; }
      buddyAct(root, act, dur);
    }, at * 1000));
  });
}
