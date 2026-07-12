# 🎓 EduSphere AI

> **Self-improving AI study companion** built on the [Hermes Agent](https://github.com/NousResearch/hermes-agent) framework.
> Specialized in **CBSE/NCERT**, AP, IB, GCSE, and global school curricula.

[![Hermes Profile](https://img.shields.io/badge/Hermes-Profile-edusphere-blue)](#)
[![Python](https://img.shields.io/badge/Python-3.11-green)](#)
[![License](https://img.shields.io/badge/License-MIT-yellow)](#)

---

## 🚀 Quick Start

```bash
# Clone the workspace
git clone https://github.com/kaakash400114-star/edusphere-ai.git
cd edusphere-ai

# Launch EduSphere (requires Hermes Agent)
hermes -p edusphere
```

> **First interaction?** EduSphere will ask your name, grade, curriculum, subjects, and target exam — then remembers you forever.

---

## ✨ Features

### 🧠 Self-Improving Memory
- Remembers your name, grade, curriculum, learning style across sessions
- Tracks weak areas and proactively suggests review topics
- Builds a learning profile over time — gets better at helping you

### 📚 Multi-Curriculum Coverage
| Curriculum | Classes | Subjects |
|------------|---------|----------|
| **CBSE / NCERT** | 6–12 | Physics, Chemistry, Biology, Maths, CS, Economics |
| **AP** | 11–12 | Calculus, Physics C, Chemistry, Biology, CS A |
| **IB** | HL/SL | All Groups 1–6 |
| **GCSE / A-Levels** | 10–13 | Full UK national curriculum |

### 🎯 Teaching Methods
- **Feynman Technique** — complex concepts explained in simple language
- **Socratic Method** — guided questions that lead you to the answer
- **Active Recall** — quiz after every topic to cement understanding

### 📝 Study Tools
- **Flashcards** — auto-generated from any topic, spaced repetition
- **Quizzes** — MCQ with difficulty levels, tracked scores
- **Notes** — structured markdown notes organized by subject
- **Progress Tracker** — strengths, weak areas, session history

---

## 📂 Project Structure

```
edusphere-ai/
├── AGENTS.md                # Session flow rules & response formatting
├── config.yaml              # Model & workspace configuration
├── skills/
│   └── study-helper/
│       ├── SKILL.md         # Skill documentation
│       └── scripts/
│           └── study_helper.py   # Flashcards, quizzes, progress CLI
├── flashcards/              # Generated flashcard decks (gitignored)
├── quizzes/                 # Quiz session results (gitignored)
├── notes/                   # Study notes by subject (gitignored)
└── profile/                 # Student learning profile (gitignored)
```

---

## 🖥️ Live Demo

### Example 1 — Feynman Technique Explanation
> *"Explain Photosynthesis according to the Class 10 CBSE NCERT Biology syllabus."*

EduSphere explains using a **"solar-powered kitchen" analogy**:

| Kitchen | Plant's Version |
|---------|----------------|
| Ingredients | CO₂ from air + Water from soil |
| Energy | Sunlight ☀️ |
| Oven / Chef | Chlorophyll (green pigment in leaves) |

Then covers Light Reaction ⚡ vs Dark Reaction 🌙, and ends with active recall questions.

### Example 2 — Auto-Generated Quiz
> *"Quiz me on Newton's Laws of Motion."*

EduSphere auto-generates a tracked MCQ quiz covering all 3 laws, saves results to disk:

```
══════════════════════════════════════════════
  📋 QUIZ — Newton's Laws of Motion
  Class 11 CBSE Physics | Difficulty: Medium
══════════════════════════════════════════════

Q1: A passenger lurches forward when brakes are applied.
    Which law explains this?
    A. Second Law  B. First Law ✅  C. Third Law  D. Gravitation

Q2: 2 kg block, 10 N force, frictionless. Acceleration?
    A. 20 m/s²  B. 5 m/s² ✅  C. 0.2 m/s²  D. 10 m/s²

Q3: Horse pulls cart — why does the system still accelerate?
    A. Smaller force  B. Action-reaction on different bodies ✅
    C. Third Law doesn't apply  D. Cart has less mass
```

### Example 3 — Persistent Memory
> *"My name is Aakash, CBSE Class 11, JEE Main 2027, visual learner."*

Next session, EduSphere greets by name and personalizes every explanation.

---

## 🔧 How It Works

EduSphere is a **Hermes Agent profile** with:

1. **Custom SOUL.md** — Defines the tutor persona, teaching philosophy, and behavioral rules
2. **AGENTS.md** — Workspace-level instructions for session structure, curriculum coverage, and tool usage
3. **study-helper skill** — Python CLI tool for flashcards, quizzes, notes, and progress tracking
4. **Hermes native tools** — Web search for NCERT/c curriculum verification, persistent memory, file management

### Architecture

```
┌─────────────────────────────────┐
│         Student User            │
└──────────────┬──────────────────┘
               │ "Explain topic X"
               ▼
┌─────────────────────────────────┐
│     Hermes Agent (edusphere)    │
│  ┌──────────┐ ┌──────────────┐  │
│  │ SOUL.md  │ │  AGENTS.md   │  │
│  │ (persona)│ │  (rules)     │  │
│  └──────────┘ └──────────────┘  │
│  ┌──────────┐ ┌──────────────┐  │
│  │ Memory   │ │ Web Search   │  │
│  │ (profile)│ │ (NCERT/CBSE) │  │
│  └──────────┘ └──────────────┘  │
│  ┌──────────────────────────┐   │
│  │   study-helper skill     │   │
│  │  flashcards | quizzes    │   │
│  │  notes | progress track  │   │
│  └──────────────────────────┘   │
└─────────────────────────────────┘
```

---

## ⚙️ Configuration

### study_helper.py Commands

```bash
# Generate flashcards
python skills/study-helper/scripts/study_helper.py flashcards \
  --subject "Biology" --topic "Photosynthesis" --count 10

# Create quiz session
python skills/study-helper/scripts/study_helper.py quiz \
  --subject "Physics" --topic "Newton's Laws" --count 5 --difficulty medium

# Update progress
python skills/study-helper/scripts/study_helper.py progress \
  --add-topic "Photosynthesis" --score 85 --notes "Understood light and dark reactions"

# View student profile
python skills/study-helper/scripts/study_helper.py profile

# Save study notes
python skills/study-helper/scripts/study_helper.py notes \
  --subject "Chemistry" --topic "Periodic Table" --content "# Notes here..."
```

### Profile Setup

After creating the Hermes profile, copy your API keys:

```bash
# Copy API keys from your main Hermes config
cp ~/.hermes/.env ~/.hermes/profiles/edusphere/.env

# Or configure fresh
edusphere setup
```

---

## 🛠️ Requirements

- [Hermes Agent](https://github.com/NousResearch/hermes-agent) installed
- Python 3.11+
- API key for an LLM provider (Z.AI, OpenRouter, Anthropic, etc.)
- Web access (for NCERT/curriculum search verification)

---

## 📄 License

MIT — built with ❤️ by [Aakash](https://github.com/kaakash400114-star)

---

*Powered by [Hermes Agent](https://hermes-agent.nousresearch.com) by Nous Research*
