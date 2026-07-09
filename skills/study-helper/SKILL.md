---
name: study-helper
description: "Generate flashcards, quizzes, and track student learning progress for EduSphere AI."
version: 1.0.0
author: EduSphere AI
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [education, study, flashcards, quizzes, learning, cbse, ncert]
---

# Study Helper Skill

Tools for generating flashcards, running quizzes, and tracking student progress.

## When to Use

- Use **flashcard generation** when a student finishes a topic and wants revision material.
- Use **quiz generation** when starting a review session or testing active recall.
- Use **progress tracking** at the end of every study session.
- Use **note creation** when summarizing a newly taught concept.

## Commands

### Generate Flashcards
```
study_helper.py flashcards --subject <subject> --topic <topic> [--source <file_or_text>] [--count 10]
```
Parses study material and creates structured flashcards (Q&A pairs) in JSON format.

### Run Quiz
```
study_helper.py quiz --subject <subject> --topic <topic> [--count 5] [--difficulty easy|medium|hard]
```
Generates a multiple-choice quiz and tracks results.

### Track Progress
```
study_helper.py progress --add-topic <topic> --score <0-100> --notes <notes>
```
Updates the student's learning profile with session results.

### View Profile
```
study_helper.py profile [--subject <subject>]
```
Shows current student profile, weak areas, and recommended review topics.

### Create Notes
```
study_helper.py notes --subject <subject> --topic <topic> --content <markdown_content>
```
Saves structured study notes as Markdown files organized by subject.

## Workspace Directories

All data is stored relative to the EduSphere workspace (`C:\Users\user\student-ai-helper`):

| Directory | Purpose |
|-----------|---------|
| `flashcards/` | JSON flashcard decks by subject |
| `quizzes/` | Quiz results history |
| `notes/` | Markdown study notes by subject |
| `profile/` | Student learning profile data |

## Usage Pattern

1. After teaching a topic, call `flashcards` to generate revision cards.
2. During review, call `quiz` to test retention.
3. After the session, call `progress` to update the student's learning profile.
4. At session start, call `profile` to see weak areas and suggest review topics.

## Integration with EduSphere

This skill works with the EduSphere AI workspace and profile. The agent should:
- Call these scripts via `terminal()` from the workspace directory.
- Read output JSON to track scores and suggest follow-ups.
- Use results to update persistent memory about weak areas.
