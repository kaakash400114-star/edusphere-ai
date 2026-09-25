/* EduSphere AI — the Animal Cast.
 * Ten full-body SVG animals. Each is a plain function returning SVG markup
 * with named groups the animator drives:
 *   data-part="mouth"  — the talking mouth (scaled while speaking)
 *   data-part="body"   — idle bob target
 *   data-part="eyes"   — blink (scaleY)
 *   data-part="tail"   — wag/sway loop
 *   data-part="earL"/"earR" — twitch on pet
 * Everything is inline SVG: no downloads, works offline, scales crisply.
 * Palette: soft flat fills + darker stroke, big glossy eyes — baby-animal
 * proportions (big head ~45% of body) because that is what kids bond with.
 */
"use strict";

function _eyes(cx, cy, look) {
  return `<g data-part="eyes">
    <g class="an-eye"><circle cx="${cx - 13}" cy="${cy}" r="6.5" fill="#fff" stroke="#3a3a4a" stroke-width="1.4"/>
      <circle class="an-pupil" cx="${cx - 13 + look}" cy="${cy + 1}" r="3" fill="#26263a"/>
      <circle cx="${cx - 15}" cy="${cy - 2}" r="1.2" fill="#fff"/></g>
    <g class="an-eye"><circle cx="${cx + 13}" cy="${cy}" r="6.5" fill="#fff" stroke="#3a3a4a" stroke-width="1.4"/>
      <circle class="an-pupil" cx="${cx + 13 + look}" cy="${cy + 1}" r="3" fill="#26263a"/>
      <circle cx="${cx + 11}" cy="${cy - 2}" r="1.2" fill="#fff"/></g>
  </g>`;
}
function _mouth(x, y, w) {
  return `<g data-part="mouth" transform="translate(${x} ${y})">
    <ellipse class="an-mouth-open" cx="0" cy="0" rx="${w / 2}" ry="1" fill="#8a3142"/>
    <ellipse class="an-mouth-open" cx="0" cy="2.4" rx="${w / 3}" ry="0.9" fill="#e0647e" opacity=".85"/>
    <path class="an-mouth-line" d="M ${-w / 2} 0 Q 0 ${w * 0.32} ${w / 2} 0" fill="none" stroke="#3a3a4a" stroke-width="1.8" stroke-linecap="round"/>
  </g>`;
}
function _blush(x, y) {
  return `<ellipse cx="${x}" cy="${y}" rx="5" ry="2.8" fill="#ff9fb0" opacity=".55"/>`;
}

const ANIMALS = {
  /* ---- Leo the lion cub ---- */
  leo: (look) => `
    <g data-part="tail"><path d="M78 78 Q 96 70 92 52" fill="none" stroke="#e8912d" stroke-width="5" stroke-linecap="round"/>
      <circle cx="92" cy="52" r="4.5" fill="#b45f16"/></g>
    <g data-part="body">
      <ellipse cx="50" cy="72" rx="24" ry="18" fill="#f6a83c" stroke="#d97f18" stroke-width="2"/>
      <ellipse cx="50" cy="80" rx="14" ry="8" fill="#ffdfa8"/>
      <g data-part="earL"><circle cx="28" cy="22" r="7" fill="#f6a83c" stroke="#d97f18" stroke-width="2"/></g>
      <g data-part="earR"><circle cx="72" cy="22" r="7" fill="#f6a83c" stroke="#d97f18" stroke-width="2"/></g>
      <circle cx="30" cy="24" r="3" fill="#ffdfa8"/><circle cx="70" cy="24" r="3" fill="#ffdfa8"/>
      <circle cx="50" cy="40" r="26" fill="#f6a83c" stroke="#d97f18" stroke-width="2"/>
      <path d="M26 30 Q 32 10 50 12 Q 68 10 74 30 Q 66 20 50 20 Q 34 20 26 30" fill="#c96f14"/>
      <circle cx="40" cy="30" r="4" fill="#c96f14" opacity=".5"/>
      <circle cx="60" cy="30" r="4" fill="#c96f14" opacity=".5"/>
      ${_eyes(50, 40, look)}
      <path d="M50 46 l-3.5 -3 h7 z" fill="#8a5416"/>
      ${_mouth(50, 51, 12)}
      ${_blush(30, 48)}${_blush(70, 48)}
      <ellipse cx="38" cy="90" rx="7" ry="4" fill="#ffdfa8" stroke="#d97f18" stroke-width="1.5"/>
      <ellipse cx="62" cy="90" rx="7" ry="4" fill="#ffdfa8" stroke="#d97f18" stroke-width="1.5"/>
    </g>`,
  /* ---- Miko the panda ---- */
  miko: (look) => `
    <g data-part="tail"><circle cx="82" cy="80" r="5" fill="#3f4756"/></g>
    <g data-part="body">
      <ellipse cx="50" cy="72" rx="25" ry="19" fill="#fff" stroke="#3f4756" stroke-width="2"/>
      <ellipse cx="50" cy="75" rx="13" ry="10" fill="#3f4756"/>
      <g data-part="earL"><circle cx="29" cy="20" r="7.5" fill="#3f4756"/></g>
      <g data-part="earR"><circle cx="71" cy="20" r="7.5" fill="#3f4756"/></g>
      <circle cx="50" cy="42" r="25" fill="#fff" stroke="#3f4756" stroke-width="2"/>
      <ellipse cx="35" cy="38" rx="9" ry="11" fill="#3f4756" transform="rotate(-14 35 38)"/>
      <ellipse cx="65" cy="38" rx="9" ry="11" fill="#3f4756" transform="rotate(14 65 38)"/>
      ${_eyes(50, 40, look)}
      <ellipse cx="50" cy="49" rx="3.4" ry="2.6" fill="#26263a"/>
      ${_mouth(50, 53, 12)}
      ${_blush(29, 50)}${_blush(71, 50)}
      <ellipse cx="37" cy="90" rx="8" ry="4.5" fill="#3f4756"/>
      <ellipse cx="63" cy="90" rx="8" ry="4.5" fill="#3f4756"/>
    </g>`,
  /* ---- Pip the squirrel ---- */
  pip: (look) => `
    <g data-part="tail"><path d="M80 82 Q 104 74 96 46 Q 92 32 80 36 Q 92 44 88 60 Q 84 72 74 76 Z" fill="#c1613b" stroke="#96451f" stroke-width="2"/></g>
    <g data-part="body">
      <ellipse cx="48" cy="72" rx="21" ry="17" fill="#d97b4a" stroke="#96451f" stroke-width="2"/>
      <ellipse cx="48" cy="76" rx="11" ry="8" fill="#ffe3c2"/>
      <g data-part="earL"><path d="M32 24 Q 26 8 38 14 Q 40 20 40 26 Z" fill="#d97b4a" stroke="#96451f" stroke-width="2"/></g>
      <g data-part="earR"><path d="M60 24 Q 62 8 70 15 Q 66 20 66 26 Z" fill="#d97b4a" stroke="#96451f" stroke-width="2"/></g>
      <circle cx="48" cy="41" r="23" fill="#d97b4a" stroke="#96451f" stroke-width="2"/>
      <ellipse cx="48" cy="50" rx="12" ry="8.5" fill="#ffe3c2"/>
      ${_eyes(48, 38, look)}
      <ellipse cx="48" cy="46" rx="3" ry="2.4" fill="#5b3317"/>
      ${_mouth(48, 51, 11)}
      ${_blush(30, 47)}${_blush(66, 47)}
      <path d="M30 20 Q 36 12 44 16" fill="none" stroke="#7a3c17" stroke-width="2" stroke-linecap="round"/>
      <path d="M58 16 Q 66 12 68 20" fill="none" stroke="#7a3c17" stroke-width="2" stroke-linecap="round"/>
      <ellipse cx="37" cy="89" rx="7" ry="4" fill="#ffe3c2" stroke="#96451f" stroke-width="1.5"/>
      <ellipse cx="59" cy="89" rx="7" ry="4" fill="#ffe3c2" stroke="#96451f" stroke-width="1.5"/>
    </g>`,
  /* ---- Chintu the elephant ---- */
  chintu: (look) => `
    <g data-part="tail"><path d="M78 76 Q 92 74 90 62" fill="none" stroke="#8f95a8" stroke-width="4" stroke-linecap="round"/></g>
    <g data-part="body">
      <ellipse cx="50" cy="72" rx="26" ry="19" fill="#aab3c9" stroke="#7b849e" stroke-width="2"/>
      <g data-part="earL"><ellipse cx="24" cy="34" rx="11" ry="14" fill="#aab3c9" stroke="#7b849e" stroke-width="2"/><ellipse cx="24" cy="34" rx="6" ry="8.5" fill="#ffc9d4"/></g>
      <g data-part="earR"><ellipse cx="76" cy="34" rx="11" ry="14" fill="#aab3c9" stroke="#7b849e" stroke-width="2"/><ellipse cx="76" cy="34" rx="6" ry="8.5" fill="#ffc9d4"/></g>
      <circle cx="50" cy="42" r="24" fill="#aab3c9" stroke="#7b849e" stroke-width="2"/>
      <path d="M50 52 Q 48 68 54 80 Q 57 85 62 83" fill="none" stroke="#8f95a8" stroke-width="9" stroke-linecap="round"/>
      <path d="M50 52 Q 48 68 54 80 Q 57 85 62 83" fill="none" stroke="#aab3c9" stroke-width="5.5" stroke-linecap="round"/>
      ${_eyes(50, 40, look)}
      ${_mouth(52, 51, 10)}
      ${_blush(31, 50)}${_blush(70, 50)}
      <ellipse cx="38" cy="90" rx="8.5" ry="4.5" fill="#aab3c9" stroke="#7b849e" stroke-width="1.5"/>
      <ellipse cx="62" cy="90" rx="8.5" ry="4.5" fill="#aab3c9" stroke="#7b849e" stroke-width="1.5"/>
    </g>`,
  /* ---- Zara the fox ---- */
  zara: (look) => `
    <g data-part="tail"><path d="M80 80 Q 102 74 98 52 Q 96 42 86 46 Q 94 56 88 68 Q 84 76 76 78 Z" fill="#e8703a" stroke="#b34e1e" stroke-width="2"/>
      <path d="M92 50 Q 98 44 94 54 Q 90 60 86 56 Z" fill="#fff"/></g>
    <g data-part="body">
      <ellipse cx="50" cy="72" rx="22" ry="17" fill="#f08a4b" stroke="#b34e1e" stroke-width="2"/>
      <ellipse cx="50" cy="77" rx="11" ry="7.5" fill="#fff4e8"/>
      <g data-part="earL"><path d="M31 26 L 27 8 L 43 18 Z" fill="#f08a4b" stroke="#b34e1e" stroke-width="2"/><path d="M33 22 L 31 13 L 39 18 Z" fill="#3a3a4a"/></g>
      <g data-part="earR"><path d="M69 26 L 73 8 L 57 18 Z" fill="#f08a4b" stroke="#b34e1e" stroke-width="2"/><path d="M67 22 L 69 13 L 61 18 Z" fill="#3a3a4a"/></g>
      <circle cx="50" cy="42" r="23" fill="#f08a4b" stroke="#b34e1e" stroke-width="2"/>
      <path d="M38 52 Q 50 62 62 52 L 58 58 Q 50 63 42 58 Z" fill="#fff4e8"/>
      ${_eyes(50, 39, look)}
      <path d="M50 46 l-3 -2.6 h6 z" fill="#6e3612"/>
      ${_mouth(50, 51, 11)}
      ${_blush(31, 47)}${_blush(69, 47)}
      <ellipse cx="38" cy="89" rx="7" ry="4" fill="#fff4e8" stroke="#b34e1e" stroke-width="1.5"/>
      <ellipse cx="62" cy="89" rx="7" ry="4" fill="#fff4e8" stroke="#b34e1e" stroke-width="1.5"/>
    </g>`,
  /* ---- Toko the parrot ---- */
  toko: (look) => `
    <g data-part="tail"><path d="M76 76 Q 98 70 100 50 L 90 58 Q 92 68 74 72 Z" fill="#2fae6b" stroke="#1c7c49" stroke-width="2"/>
      <path d="M78 78 Q 96 76 98 62 L 88 68 Q 88 74 76 76 Z" fill="#ffd23f" stroke="#d9a616" stroke-width="1.6"/></g>
    <g data-part="body">
      <ellipse cx="48" cy="70" rx="21" ry="18" fill="#35c07a" stroke="#1c7c49" stroke-width="2"/>
      <ellipse cx="48" cy="73" rx="11" ry="9" fill="#eafbf0"/>
      <g data-part="earL"><path d="M30 22 Q 22 12 34 10 Q 40 14 40 24 Z" fill="#2fae6b" stroke="#1c7c49" stroke-width="2"/></g>
      <g data-part="earR"><path d="M62 20 Q 64 10 74 12 Q 74 20 68 26 Z" fill="#ffd23f" stroke="#d9a616" stroke-width="2"/></g>
      <circle cx="49" cy="40" r="22" fill="#35c07a" stroke="#1c7c49" stroke-width="2"/>
      <circle cx="49" cy="40" r="15" fill="#eafbf0" opacity=".35"/>
      <path d="M28 34 Q 40 22 58 26 Q 44 30 36 40 Z" fill="#e63946"/>
      ${_eyes(49, 38, look)}
      <g data-part="beak"><path d="M49 46 Q 60 46 58 54 Q 54 58 49 54 Q 52 50 49 46" fill="#ffb703" stroke="#d97706" stroke-width="1.6"/></g>
      ${_blush(31, 47)}
      <ellipse cx="40" cy="88" rx="6" ry="3.5" fill="#ffb703" stroke="#d97706" stroke-width="1.5"/>
      <ellipse cx="56" cy="88" rx="6" ry="3.5" fill="#ffb703" stroke="#d97706" stroke-width="1.5"/>
    </g>`,
  /* ---- Kiko the dolphin ---- */
  kiko: (look) => `
    <g data-part="tail"><path d="M78 72 Q 98 62 94 46 Q 104 58 96 74 Q 88 82 78 80 Z" fill="#4aa8d8" stroke="#2b7cab" stroke-width="2"/></g>
    <g data-part="body">
      <path d="M26 74 Q 22 46 48 40 Q 74 44 76 66 Q 74 82 50 84 Q 30 84 26 74 Z" fill="#5cbbe9" stroke="#2b7cab" stroke-width="2"/>
      <path d="M50 44 Q 54 30 66 26 Q 60 40 58 46 Z" fill="#4aa8d8" stroke="#2b7cab" stroke-width="2"/>
      <path d="M40 58 Q 50 52 60 58 Q 50 64 40 58" fill="#a8dcf2" opacity=".8"/>
      ${_eyes(50, 56, look)}
      ${_mouth(50, 66, 12)}
      ${_blush(33, 63)}
      <g data-part="fin"><path d="M40 74 Q 34 84 26 82 Q 32 74 38 70 Z" fill="#4aa8d8" stroke="#2b7cab" stroke-width="2"/></g>
      <ellipse cx="34" cy="50" rx="4" ry="6" fill="#fff" opacity=".5" transform="rotate(-24 34 50)"/>
    </g>`,
  /* ---- Bip the robot ---- */
  bip: (look) => `
    <g data-part="tail"><path d="M78 78 h10 M88 74 v8" stroke="#64748b" stroke-width="3" stroke-linecap="round"/></g>
    <g data-part="body">
      <rect x="30" y="58" width="40" height="30" rx="10" fill="#cbd5e1" stroke="#64748b" stroke-width="2"/>
      <circle cx="50" cy="73" r="7" fill="#38bdf8" opacity=".85"><animate attributeName="opacity" values=".4;.9;.4" dur="2.2s" repeatCount="indefinite"/></circle>
      <g data-part="earL"><rect x="22" y="36" width="8" height="14" rx="3" fill="#94a3b8"/></g>
      <g data-part="earR"><rect x="70" y="36" width="8" height="14" rx="3" fill="#94a3b8"/></g>
      <line x1="50" y1="18" x2="50" y2="12" stroke="#64748b" stroke-width="2.5"/><circle cx="50" cy="10" r="3.5" fill="#f43f5e"><animate attributeName="opacity" values="1;.2;1" dur="1.1s" repeatCount="indefinite"/></circle>
      <rect x="27" y="22" width="46" height="38" rx="13" fill="#e2e8f0" stroke="#64748b" stroke-width="2"/>
      <rect x="34" y="30" width="32" height="17" rx="8" fill="#312e46"/>
      ${look ? `<g data-part="eyes"><rect x="${38 + look}" y="35" width="6" height="7" rx="2.5" fill="#7ef29a"/><rect x="${54 + look}" y="35" width="6" height="7" rx="2.5" fill="#7ef29a"/></g>`
             : `<g data-part="eyes"><rect x="38" y="35" width="6" height="7" rx="2.5" fill="#7ef29a"/><rect x="54" y="35" width="6" height="7" rx="2.5" fill="#7ef29a"/></g>`}
      ${_mouth(50, 53, 12)}
      ${_blush(32, 52)}${_blush(68, 52)}
      <ellipse cx="40" cy="89" rx="7.5" ry="4" fill="#94a3b8"/>
      <ellipse cx="60" cy="89" rx="7.5" ry="4" fill="#94a3b8"/>
    </g>`,
  /* ---- Dodo the baby dragon ---- */
  dodo: (look) => `
    <g data-part="tail"><path d="M78 78 Q 98 72 96 54 L 88 62 Q 90 72 76 74 Z" fill="#9d5ce8" stroke="#6d3bb8" stroke-width="2"/></g>
    <g data-part="body">
      <ellipse cx="50" cy="72" rx="24" ry="18" fill="#b57bf0" stroke="#6d3bb8" stroke-width="2"/>
      <ellipse cx="50" cy="77" rx="12" ry="8" fill="#f3e3ff"/>
      <g data-part="earL"><path d="M30 22 Q 24 10 38 14 Q 40 20 40 25 Z" fill="#b57bf0" stroke="#6d3bb8" stroke-width="2"/></g>
      <g data-part="earR"><path d="M70 22 Q 76 10 62 14 Q 60 20 60 25 Z" fill="#b57bf0" stroke="#6d3bb8" stroke-width="2"/></g>
      <circle cx="50" cy="42" r="24" fill="#b57bf0" stroke="#6d3bb8" stroke-width="2"/>
      <path d="M34 26 Q 40 18 50 18 Q 60 18 66 26" fill="none" stroke="#8b5cf6" stroke-width="3" stroke-linecap="round"/>
      ${_eyes(50, 39, look)}
      <path d="M50 45 l-3 -2.6 h6 z" fill="#4c2a85"/>
      <g><path d="M42 50 q8 6 16 0 l-2 5 q-6 4 -12 0 z" fill="#ff7b54" opacity=".9"/></g>
      ${_mouth(50, 55, 11)}
      ${_blush(30, 48)}${_blush(70, 48)}
      <ellipse cx="38" cy="90" rx="8" ry="4.2" fill="#f3e3ff" stroke="#6d3bb8" stroke-width="1.5"/>
      <ellipse cx="62" cy="90" rx="8" ry="4.2" fill="#f3e3ff" stroke="#6d3bb8" stroke-width="1.5"/>
      <g data-part="wing"><path d="M28 62 Q 12 58 14 44 Q 24 52 30 56 Z" fill="#9d5ce8" stroke="#6d3bb8" stroke-width="2"/></g>
    </g>`,
  /* ---- Professor Nova the owl ---- */
  nova: (look) => `
    <g data-part="tail"><path d="M74 80 L 90 74 L 84 84 Z" fill="#8b5cf6" stroke="#5b3fa8" stroke-width="2"/></g>
    <g data-part="body">
      <ellipse cx="50" cy="68" rx="23" ry="21" fill="#a78bfa" stroke="#5b3fa8" stroke-width="2"/>
      <ellipse cx="50" cy="74" rx="13" ry="10" fill="#efe7ff"/>
      <path d="M38 60 l6 5 -6 5 -3 -5 z M62 60 l-6 5 6 5 3 -5 z" fill="#c4b5fd"/>
      <g data-part="earL"><path d="M30 24 L 28 10 L 42 18 Z" fill="#a78bfa" stroke="#5b3fa8" stroke-width="2"/></g>
      <g data-part="earR"><path d="M70 24 L 72 10 L 58 18 Z" fill="#a78bfa" stroke="#5b3fa8" stroke-width="2"/></g>
      <circle cx="50" cy="38" r="22" fill="#a78bfa" stroke="#5b3fa8" stroke-width="2"/>
      <circle cx="40" cy="36" r="9.5" fill="#f5f0ff"/><circle cx="60" cy="36" r="9.5" fill="#f5f0ff"/>
      <g data-part="eyes">
        <circle cx="40" cy="36" r="4.6" fill="#26263a"/><circle cx="38.4" cy="34.4" r="1.5" fill="#fff"/>
        <circle cx="60" cy="36" r="4.6" fill="#26263a"/><circle cx="58.4" cy="34.4" r="1.5" fill="#fff"/>
      </g>
      <path d="M50 42 l-4 4 h8 z" fill="#ffb703" stroke="#d97706" stroke-width="1.4"/>
      ${_mouth(50, 52, 10)}
      <ellipse cx="36" cy="88" rx="6" ry="3.5" fill="#ffb703" stroke="#d97706" stroke-width="1.5"/>
      <ellipse cx="64" cy="88" rx="6" ry="3.5" fill="#ffb703" stroke="#d97706" stroke-width="1.5"/>
    </g>`,
};

function animalSVG(buddyId, look = 0) {
  const fn = ANIMALS[buddyId] || ANIMALS.leo;
  return `<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">${fn(look)}</svg>`;
}
