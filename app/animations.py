"""Character animation system for EduSphere AI.

Every buddy has a set of human-like actions (idle, talk, celebrate, think,
shy, wave, jump, spin, sad, sneeze, wink). The frontend renders these as
CSS keyframe animations using the action data returned here.

Each action provides:
  - css_class: the CSS class to apply to the character element
  - duration_ms: how long the animation runs
  - sound: optional sound effect key (frontend maps to audio)
  - particles: optional particle system to spawn (stars, confetti, hearts, etc.)
  - speech_bubble: optional ephemeral text to show above the character

Context-to-action mapping:
  on_greet → wave then idle
  on_correct → celebrate (character-specific: backflip, trumpet, etc.)
  on_wrong → shy then encourage
  on_thinking → think
  on_talking → talk (lip-sync shimmer)
  on_story → storyteller pose
  on_quiz → quiz host pose
  on_sleep → sleepy (Miko only)
  on_party → special celebration with particles
"""
from __future__ import annotations

# ── Action catalog ─────────────────────────────────────────────────────────────
# Each action dict is safe to send directly to the frontend.

_ACTIONS: dict[str, dict] = {
    "idle":        {"css": "anim-idle",        "duration": 0,    "loop": True},
    "talk":        {"css": "anim-talk",        "duration": 0,    "loop": True},
    "think":       {"css": "anim-think",       "duration": 2500, "loop": False},
    "wave":        {"css": "anim-wave",        "duration": 1800, "loop": False},
    "celebrate":   {"css": "anim-celebrate",   "duration": 2000, "loop": False},
    "jump":        {"css": "anim-jump",        "duration": 1000, "loop": False},
    "backflip":    {"css": "anim-backflip",    "duration": 900,  "loop": False},
    "shy":         {"css": "anim-shy",         "duration": 2000, "loop": False},
    "sad":         {"css": "anim-sad",         "duration": 2200, "loop": False},
    "spin":        {"css": "anim-spin",        "duration": 800,  "loop": False},
    "wink":        {"css": "anim-wink",        "duration": 700,  "loop": False},
    "nod":         {"css": "anim-nod",         "duration": 1200, "loop": False},
    "shake_head":  {"css": "anim-shake-head",  "duration": 900,  "loop": False},
    "clap":        {"css": "anim-clap",        "duration": 2500, "loop": False},
    "trumpet":     {"css": "anim-trumpet",     "duration": 2000, "loop": False},
    "sneeze":      {"css": "anim-sneeze",      "duration": 1200, "loop": False},
    "flip":        {"css": "anim-flip",        "duration": 1000, "loop": False},
    "storyteller": {"css": "anim-storyteller", "duration": 0,    "loop": True},
    "quiz_host":   {"css": "anim-quiz-host",   "duration": 0,    "loop": True},
    "sleep":       {"css": "anim-sleep",       "duration": 0,    "loop": True},
    "run":         {"css": "anim-run",         "duration": 0,    "loop": True},
}

# ── Per-buddy action overrides ────────────────────────────────────────────────
# "on_correct" / "on_wrong" / "on_greet" / "on_thinking" / "on_party"
# map to specific actions. Defaults apply when no override is present.

_BUDDY_ACTIONS: dict[str, dict] = {
    "leo": {
        "on_greet":    ["wave", "jump"],
        "on_correct":  ["backflip", "celebrate"],      # big happy roar + backflip
        "on_wrong":    ["shy", "nod"],                 # 'let's try again'
        "on_thinking": ["think"],
        "on_party":    ["backflip", "celebrate", "jump"],
        "on_talking":  ["talk"],
        "particles": {
            "on_correct": "stars_gold",
            "on_party":   "confetti_rainbow",
        },
        "sounds": {
            "on_correct": "roar",
            "on_party":   "roar_big",
        },
    },
    "miko": {
        "on_greet":    ["wave"],
        "on_correct":  ["nod", "clap"],
        "on_wrong":    ["shake_head", "nod"],
        "on_thinking": ["sleep"],                      # Miko dozes mid-thought
        "on_party":    ["spin", "clap"],
        "on_talking":  ["talk"],
        "on_story":    ["storyteller"],
        "particles": {
            "on_correct": "hearts_soft",
            "on_party":   "stars_blue",
        },
    },
    "pip": {
        "on_greet":    ["jump", "wave", "jump"],
        "on_correct":  ["jump", "spin", "clap"],
        "on_wrong":    ["shy"],                        # Pip trips, laughs
        "on_thinking": ["run"],                        # scurrying
        "on_party":    ["jump", "flip", "jump"],
        "on_talking":  ["talk"],
        "particles": {
            "on_correct": "acorns_bounce",
            "on_party":   "confetti_rainbow",
        },
        "sounds": {
            "on_correct": "squirrel_giggle",
        },
    },
    "chintu": {
        "on_greet":    ["trumpet", "wave"],
        "on_correct":  ["trumpet", "celebrate"],
        "on_wrong":    ["shake_head", "nod"],
        "on_thinking": ["think"],
        "on_party":    ["trumpet", "celebrate"],
        "on_talking":  ["talk"],
        "particles": {
            "on_correct": "water_confetti",
            "on_party":   "stars_gold",
        },
        "sounds": {
            "on_correct": "elephant_trumpet",
        },
    },
    "zara": {
        "on_greet":    ["wink", "wave"],
        "on_correct":  ["spin", "wink"],
        "on_wrong":    ["shake_head", "wink"],         # 'you almost had me'
        "on_thinking": ["think"],
        "on_party":    ["spin", "celebrate", "wink"],
        "on_talking":  ["talk"],
        "particles": {
            "on_correct": "stars_red",
            "on_party":   "confetti_orange",
        },
    },
    "toko": {
        "on_greet":    ["flip", "wave"],
        "on_correct":  ["clap", "jump"],
        "on_wrong":    ["shake_head", "nod"],
        "on_thinking": ["think"],
        "on_party":    ["flip", "spin", "clap"],
        "on_talking":  ["talk"],
        "particles": {
            "on_correct": "feathers_rainbow",
            "on_party":   "confetti_rainbow",
        },
        "sounds": {
            "on_correct": "parrot_squawk",
        },
    },
    "kiko": {
        "on_greet":    ["flip", "wave"],
        "on_correct":  ["flip", "jump"],               # joyful dolphin flip
        "on_wrong":    ["shy", "nod"],
        "on_thinking": ["think"],
        "on_party":    ["flip", "flip", "celebrate"],
        "on_talking":  ["talk"],
        "particles": {
            "on_correct": "bubbles_blue",
            "on_party":   "stars_blue",
        },
        "sounds": {
            "on_correct": "dolphin_click",
        },
    },
    "bip": {
        "on_greet":    ["wave"],
        "on_correct":  ["celebrate"],                  # tries high-five, misses, tries again
        "on_wrong":    ["shake_head"],                 # 'Error. Acceptable.'
        "on_thinking": ["think"],
        "on_party":    ["spin", "celebrate"],
        "on_talking":  ["talk"],
        "particles": {
            "on_correct": "binary_bits",
            "on_party":   "stars_silver",
        },
        "sounds": {
            "on_correct": "robot_beep",
        },
    },
    "dodo": {
        "on_greet":    ["jump", "wave", "sneeze"],
        "on_correct":  ["sneeze", "celebrate"],        # burps a star smoke ring
        "on_wrong":    ["sad", "jump"],                # dramatic gasp then rallies
        "on_thinking": ["think"],
        "on_party":    ["jump", "sneeze", "celebrate"],
        "on_talking":  ["talk"],
        "particles": {
            "on_correct": "smoke_star",
            "on_party":   "fire_confetti",
        },
        "sounds": {
            "on_correct": "dragon_sneeze",
            "on_party":   "dragon_roar",
        },
    },
    "nova": {
        "on_greet":    ["wave", "nod"],
        "on_correct":  ["nod", "clap"],
        "on_wrong":    ["shake_head", "nod"],          # 'classic mistake, here's the trick'
        "on_thinking": ["think"],
        "on_party":    ["clap", "celebrate"],
        "on_talking":  ["talk"],
        "on_quiz":     ["quiz_host"],
        "particles": {
            "on_correct": "stars_purple",
            "on_party":   "confetti_purple",
        },
        "sounds": {
            "on_correct": "owl_hoot",
        },
    },
}

# ── Particle effect catalog ────────────────────────────────────────────────────
PARTICLES: dict[str, dict] = {
    "stars_gold":       {"type": "stars", "color": "#fde047", "count": 20},
    "stars_blue":       {"type": "stars", "color": "#38bdf8", "count": 18},
    "stars_red":        {"type": "stars", "color": "#ef4444", "count": 18},
    "stars_purple":     {"type": "stars", "color": "#a855f7", "count": 18},
    "stars_silver":     {"type": "stars", "color": "#94a3b8", "count": 18},
    "confetti_rainbow": {"type": "confetti", "colors": ["#f59e0b","#10b981","#3b82f6","#ec4899","#8b5cf6"], "count": 50},
    "confetti_orange":  {"type": "confetti", "colors": ["#fb923c","#fbbf24"], "count": 40},
    "confetti_purple":  {"type": "confetti", "colors": ["#c084fc","#818cf8"], "count": 40},
    "hearts_soft":      {"type": "hearts", "color": "#f9a8d4", "count": 15},
    "water_confetti":   {"type": "drops", "color": "#38bdf8", "count": 30},
    "acorns_bounce":    {"type": "emoji", "emoji": "🌰", "count": 10},
    "feathers_rainbow": {"type": "emoji", "emoji": "🪶", "count": 12},
    "bubbles_blue":     {"type": "bubbles", "color": "#bae6fd", "count": 25},
    "binary_bits":      {"type": "text", "chars": ["0","1"], "color": "#94a3b8", "count": 30},
    "smoke_star":       {"type": "emoji", "emoji": "⭐💨", "count": 8},
    "fire_confetti":    {"type": "emoji", "emoji": "🔥✨", "count": 12},
}


# ── Context detection ──────────────────────────────────────────────────────────

def context_actions(buddy_id: str, context: str) -> dict:
    """Return the animation sequence + particles + sounds for this context.

    context: 'on_greet' | 'on_correct' | 'on_wrong' | 'on_thinking' |
             'on_talking' | 'on_story' | 'on_quiz' | 'on_party' | 'idle'
    """
    cfg = _BUDDY_ACTIONS.get(buddy_id, _BUDDY_ACTIONS["leo"])
    actions = cfg.get(context, cfg.get("on_talking", ["talk"]))
    particle_key = (cfg.get("particles") or {}).get(context)
    sound_key = (cfg.get("sounds") or {}).get(context)

    sequence = []
    for act in actions:
        a = _ACTIONS.get(act, _ACTIONS["idle"])
        sequence.append({"action": act, **a})

    return {
        "buddy": buddy_id,
        "context": context,
        "sequence": sequence,
        "particles": PARTICLES.get(particle_key) if particle_key else None,
        "sound": sound_key,
    }


def idle_action() -> dict:
    return _ACTIONS["idle"]


def all_actions() -> list[str]:
    return list(_ACTIONS.keys())


def buddy_contexts(buddy_id: str) -> list[str]:
    """All contexts this buddy has defined animations for."""
    cfg = _BUDDY_ACTIONS.get(buddy_id, {})
    return [k for k in cfg if k.startswith("on_")]
