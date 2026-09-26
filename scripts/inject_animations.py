"""Inject animation CSS, dark mode CSS, and JavaScript enhancements into EduSphere PWA."""
with open('static/index.html', 'rb') as f:
    content = f.read().decode('utf-8')

# ─── 1. Dark mode CSS variables ───────────────────────────────────────────────
DARK_MODE_CSS = """
/* ===== DARK MODE ===== */
@media (prefers-color-scheme: dark) {
  :root {
    --bg:#1e1b2e; --card:#2d2a45; --ink:#e2e0ff; --muted:#9ca3af;
    --brand:#818cf8; --brand2:#a78bfa;
  }
  body { background: linear-gradient(160deg,#1e1b2e 0%,#2d1f3d 45%,#1a2d35 75%,#2a1f1b 100%); }
  .msg.bot { background: #2d2a45; color: #e2e0ff; }
  .msg.user { background: linear-gradient(90deg,#4338ca,#7c3aed); }
  .topbar { background: rgba(30,27,46,0.95); }
  .onboard-card, .modal-card { background: #2d2a45; color: #e2e0ff; }
}
body.dark-mode {
  --bg:#1e1b2e; --card:#2d2a45; --ink:#e2e0ff; --muted:#9ca3af;
  --brand:#818cf8; --brand2:#a78bfa;
  background: linear-gradient(160deg,#1e1b2e 0%,#2d1f3d 45%,#1a2d35 75%,#2a1f1b 100%) !important;
}
body.dark-mode .msg.bot { background: #2d2a45; color: #e2e0ff; }
body.dark-mode .topbar { background: rgba(30,27,46,0.95); }
body.dark-mode .onboard-card, body.dark-mode .modal-card { background: #2d2a45; color: #e2e0ff; }

/* ===== EXTENDED CHARACTER ANIMATIONS ===== */
/* Action: idle — gentle float */
.anim-idle { animation: esIdleFloat 3s ease-in-out infinite; }
@keyframes esIdleFloat {
  0%,100% { transform: translateY(0) rotate(0deg); }
  33%      { transform: translateY(-5px) rotate(1deg); }
  66%      { transform: translateY(-2px) rotate(-1deg); }
}
/* Action: talk — lip-sync head shimmer */
.anim-talk { animation: esTalk .25s ease-in-out infinite alternate; }
@keyframes esTalk {
  from { transform: scaleY(1) rotate(0deg); }
  to   { transform: scaleY(1.06) rotate(.8deg); }
}
/* Action: celebrate — joyful big bounce + scale */
.anim-celebrate { animation: esCelebrate .5s ease-in-out infinite alternate; }
@keyframes esCelebrate {
  from { transform: scale(1) translateY(0); }
  to   { transform: scale(1.18) translateY(-10px); }
}
/* Action: jump */
.anim-jump { animation: esJump .6s ease-out; }
@keyframes esJump {
  0%  { transform: translateY(0) scaleY(1); }
  30% { transform: translateY(-28px) scaleY(1.15); }
  60% { transform: translateY(-10px) scaleY(.95); }
  80% { transform: translateY(-4px) scaleY(1.05); }
  100%{ transform: translateY(0) scaleY(1); }
}
/* Action: backflip — full 360 somersault */
.anim-backflip { animation: esBackflip .9s cubic-bezier(.36,.07,.19,.97); }
@keyframes esBackflip {
  0%  { transform: rotate(0deg) translateY(0); }
  25% { transform: rotate(-90deg) translateY(-20px); }
  50% { transform: rotate(-180deg) translateY(-35px); }
  75% { transform: rotate(-270deg) translateY(-20px); }
  100%{ transform: rotate(-360deg) translateY(0); }
}
/* Action: spin */
.anim-spin { animation: esSpin .8s linear; }
@keyframes esSpin {
  from { transform: rotate(0deg); }
  to   { transform: rotate(360deg); }
}
/* Action: wave — arm-like swing */
.anim-wave { animation: esWave 1.8s ease-in-out; }
@keyframes esWave {
  0%,100% { transform: rotate(0deg); transform-origin: 70% 70%; }
  15%     { transform: rotate(8deg); }
  35%     { transform: rotate(-8deg); }
  55%     { transform: rotate(6deg); }
  75%     { transform: rotate(-4deg); }
}
/* Action: think — slow head tilt */
.anim-think { animation: esThink 2.5s ease-in-out infinite alternate; }
@keyframes esThink {
  from { transform: rotate(-5deg) translateY(0); }
  to   { transform: rotate(5deg) translateY(-4px); }
}
/* Action: shy — shrink + look away */
.anim-shy { animation: esShy 2s ease-in-out; }
@keyframes esShy {
  0%  { transform: scale(1) rotate(0); }
  20% { transform: scale(.92) rotate(-8deg); }
  50% { transform: scale(.88) rotate(-10deg) translateX(-6px); }
  80% { transform: scale(.95) rotate(-4deg); }
  100%{ transform: scale(1) rotate(0); }
}
/* Action: sad — droop */
.anim-sad { animation: esSad 2.2s ease-in-out; }
@keyframes esSad {
  0%,100% { transform: translateY(0) rotate(0deg); }
  30%     { transform: translateY(6px) rotate(-5deg); }
  70%     { transform: translateY(8px) rotate(3deg); }
}
/* Action: nod */
.anim-nod { animation: esNod 1.2s ease-in-out; }
@keyframes esNod {
  0%,100% { transform: rotate(0deg); }
  25%     { transform: rotate(8deg); }
  50%     { transform: rotate(-4deg); }
  75%     { transform: rotate(6deg); }
}
/* Action: shake_head */
.anim-shake-head { animation: esShake .9s ease-in-out; }
@keyframes esShake {
  0%,100% { transform: translateX(0); }
  20%     { transform: translateX(-8px) rotate(-4deg); }
  40%     { transform: translateX(8px) rotate(4deg); }
  60%     { transform: translateX(-6px) rotate(-3deg); }
  80%     { transform: translateX(6px) rotate(3deg); }
}
/* Action: clap — scale pulse representing clapping */
.anim-clap { animation: esClap 2.5s ease; }
@keyframes esClap {
  0%,10%,20%,30%,40%,100% { transform: scale(1); }
  5%,15%,25%,35%           { transform: scale(1.1) translateY(-3px); }
}
/* Action: wink */
.anim-wink { animation: esWink .7s ease; }
@keyframes esWink {
  0%,100% { transform: scaleX(1) skewY(0); }
  30%     { transform: scaleX(1.05) skewY(2deg); }
  60%     { transform: scaleX(.95) skewY(-2deg); }
}
/* Action: flip — horizontal flip (Kiko's dolphin flip) */
.anim-flip { animation: esFlip 1s ease; }
@keyframes esFlip {
  0%  { transform: scaleX(1) translateY(0); }
  25% { transform: scaleX(-1) translateY(-15px); }
  50% { transform: scaleX(-1) translateY(-25px) rotate(180deg); }
  75% { transform: scaleX(1) translateY(-15px) rotate(360deg); }
  100%{ transform: scaleX(1) translateY(0) rotate(0); }
}
/* Action: sneeze — Dodo's fiery sneeze */
.anim-sneeze { animation: esSneeze 1.2s ease; }
@keyframes esSneeze {
  0%,100% { transform: scale(1) rotate(0); }
  20%     { transform: scale(.9) rotate(-6deg); }
  35%     { transform: scale(.85) rotate(-10deg) translateY(4px); }
  50%     { transform: scale(1.25) rotate(8deg) translateY(-10px); }
  65%     { transform: scale(1.1) rotate(4deg); }
  80%     { transform: scale(.98) rotate(-2deg); }
}
/* Action: trumpet — Chintu's trunk wave */
.anim-trumpet { animation: esTrumpet 2s ease; }
@keyframes esTrumpet {
  0%,100% { transform: rotate(0deg) translateY(0); }
  15%     { transform: rotate(-6deg) translateY(-5px); }
  30%     { transform: rotate(8deg) translateY(-8px); }
  50%     { transform: rotate(-4deg) translateY(-12px) scale(1.08); }
  70%     { transform: rotate(6deg) translateY(-5px); }
  85%     { transform: rotate(-2deg) translateY(-2px); }
}
/* Action: sleep — gentle sway + bob */
.anim-sleep { animation: esSleep 3s ease-in-out infinite; }
@keyframes esSleep {
  0%,100% { transform: rotate(-3deg) translateY(0); }
  50%     { transform: rotate(3deg) translateY(-3px); }
}
/* Action: run — horizontal hop */
.anim-run { animation: esRun .4s ease-in-out infinite alternate; }
@keyframes esRun {
  from { transform: translateX(-3px) rotate(-4deg) scaleX(1.05); }
  to   { transform: translateX(3px) rotate(4deg) scaleX(.95); }
}
/* Action: storyteller — gentle reading pose */
.anim-storyteller { animation: esStoryteller 4s ease-in-out infinite; }
@keyframes esStoryteller {
  0%,100% { transform: rotate(-2deg) translateY(0); }
  50%     { transform: rotate(2deg) translateY(-4px); }
}
/* Action: quiz_host — authoritative pulse */
.anim-quiz-host { animation: esQuiz 2s ease-in-out infinite alternate; }
@keyframes esQuiz {
  from { transform: scale(1) rotate(0deg); }
  to   { transform: scale(1.05) rotate(1deg); }
}

/* ===== PARTICLE EFFECTS ===== */
.es-particle-wrap { position:absolute;top:0;left:50%;transform:translateX(-50%);pointer-events:none;z-index:100;width:0;height:0; }
.es-particle { position:absolute;border-radius:50%;opacity:1;animation:esParticleFly var(--dur,1.2s) ease-out forwards; }
@keyframes esParticleFly {
  from { opacity:1;transform:translate(var(--px,0),var(--py,0)) scale(1) rotate(0deg); }
  to   { opacity:0;transform:translate(var(--ex,0),var(--ey,-80px)) scale(.3) rotate(var(--er,360deg)); }
}

/* ===== DARK MODE TOGGLE BUTTON ===== */
#dark-toggle {
  position:fixed;bottom:16px;right:16px;z-index:999;
  width:44px;height:44px;border-radius:50%;border:2px solid #c7d2fe;
  background:#fff;font-size:1.2rem;cursor:pointer;
  box-shadow:0 2px 8px rgba(0,0,0,.15);
  display:flex;align-items:center;justify-content:center;
  transition:background .2s,border-color .2s;
}
body.dark-mode #dark-toggle { background:#2d2a45;border-color:#818cf8;color:#e2e0ff; }

/* ===== SRS REVIEW BADGE ===== */
#srs-badge {
  display:none;background:#fef3c7;border:2px solid #fde047;
  border-radius:12px;padding:6px 12px;font-size:.78rem;font-weight:700;
  color:#92400e;margin:4px 12px;text-align:center;cursor:pointer;
}
#srs-badge.visible { display:block; }

/* ===== MATH RENDERING ===== */
.katex-display { overflow-x:auto;padding:4px 0; }
.msg.bot .katex { font-size:.95em; }

/* ===== WORLD BOARD PICKER (22 boards) ===== */
.board-select option { padding:4px; }
"""

# Find insertion point: just before the </style> closing tag
close_style = '</style>'
idx = content.rfind(close_style)  # last </style> in the file
if idx < 0:
    print('ERROR: </style> not found')
else:
    content = content[:idx] + DARK_MODE_CSS + '\n' + content[idx:]
    print('SUCCESS: Animation CSS, dark mode CSS, KaTeX CSS injected')

# ─── 2. Dark mode toggle button ───────────────────────────────────────────────
DARK_TOGGLE_BTN = '\n<button id="dark-toggle" title="Toggle dark mode" onclick="document.body.classList.toggle(\'dark-mode\');localStorage.setItem(\'edusphere_dark\',document.body.classList.contains(\'dark-mode\'))">🌙</button>\n'
body_end = '</body>'
if body_end in content:
    content = content.replace(body_end, DARK_TOGGLE_BTN + body_end, 1)
    print('SUCCESS: Dark mode toggle button injected')

# ─── 3. Write updated file ────────────────────────────────────────────────────
with open('static/index.html', 'wb') as f:
    f.write(content.encode('utf-8'))
print('File written successfully.')
print(f'New size: {len(content)} chars')
