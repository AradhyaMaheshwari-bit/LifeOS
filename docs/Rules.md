# LifeOS Rules

These rules define how daily logs are generated and maintained.

---

# Rule — Schema Stability

The LifeOS JSON schema is considered stable.

Do not add, remove, or rename fields unless there is a genuine functional requirement.

Application code should adapt to the schema, not the other way around.

---

# 1. Core Principles

## Rule 1 — Never invent data

Only record information that is either:

- Explicitly provided
- Confirmed by the user
- Inferred using an agreed LifeOS inference rule.
- Prefer conventions over adding new JSON fields whenever the same information can be represented consistently.

---

## Rule 2 — Prefer explicit data

If exact information is available, always use it.

Example:

Workout:

```
07:50–08:50
```

Store:

```json
{
    "start": "2026-07-07T07:50",
    "end": "2026-07-07T08:50"
}
```

---

## Rule 3 — Ask before assuming

If important information is missing but the user is likely to know it, ask concise questions before generating the final JSON.

Example:

> "I know you had breakfast. Do you remember approximately what time?"

---

## Rule 4 — Use inference only when appropriate

If information is missing:

1. Prefer asking the user if they are likely to know the answer.
2. If the user does not know, apply an agreed LifeOS inference rule.
3. Every inferred value must be documented in `summary.notes`.

---

# 2. Inference Rules

## Sleep

### Main Sleep

**If:**

- Lunch time is known.
- No activity is recorded afterward.
- Sleep ends at a known time.

**Then:**

Infer the sleep start time approximately **2 hours after lunch**.

Add the following to `summary.notes`:

> "Sleep start time inferred using the agreed LifeOS inference rule."

---

### Naps

**If:**

- The user says they are going to sleep (or indicates they are about to take a nap).
- No sleep end time is provided at that moment.

**Then:**

Do **not** create a sleep session immediately.

Wait until the user later sends a wake-up message, such as:

> "Just woke up."

Then:

- Use the timestamp of the message indicating they were going to sleep as the sleep start time.
- Use the timestamp of the wake-up message as the sleep end time.
- Create a single sleep session automatically.

Add the following to `summary.notes`:

> "Sleep session created using the agreed LifeOS nap inference rule based on conversation timestamps."

If the user explicitly provides the sleep start time or wake-up time, always use the user's values instead of the inferred timestamps.

---

## Study

**If:**

- Study start time is known.
- No interruption is mentioned.
- Study end time is known.

**Then:**

Treat it as **one continuous study session**.

Only create multiple study sessions if the user explicitly indicates they stopped and started again.

---

## Workout

### Interrupted Workouts

**If:**

- A workout is briefly interrupted.
- The workout resumes afterward.

**Then:**

Treat it as **the same workout session**.

Only create another workout session if the user clearly states it became a separate workout.

---

### Workout Status

LifeOS tracks workout adherence as part of the 90-Day Transformation.

Unlike other activity categories, the workout section should always indicate whether the planned workout was completed or intentionally skipped.

#### Completed Workout

```json
{
    "status": "Completed",
    "type": "Leg Day",
    "start": "2026-07-07T07:50",
    "end": "2026-07-07T08:50",
    "exercises": [],
    "notes": ""
}
```

#### Skipped Workout

```json
{
    "status": "Skipped",
    "reason": "Calf muscle soreness from previous leg workout.",
    "notes": ""
}
```

The `status` field represents what happened to the planned workout.

Current supported values are:

- `Completed`
- `Skipped`

Future versions may introduce additional statuses if needed (for example `Modified`).

Whenever a workout is intentionally skipped, record the reason if it is known.

Do not leave the workout array empty when the user explicitly states they skipped the workout.

---

## Meals

### Food Structure

If the user says:

> Egg Curry and Rice

Store:

```json
"food": [
    "Egg Curry",
    "Rice"
]
```

### Meal Duration

**If:**

- Meal start time is known.
- Meal end time is not provided.

**Then:**

Infer:

```
end_time = start_time + 30 minutes
```

Add the following to `summary.notes`:

> "Meal end time inferred using the agreed LifeOS inference rule (30-minute meal duration)."

If the user explicitly provides an end time, always use the user's value instead.

---

# 3. Data Standards

- Use ISO 8601 date and datetime formats.
- Sleep belongs to the day the user wakes up.
- Do not store derived values.
- Do not invent ratings or missing information.
- Keep the JSON schema minimal and consistent.
- Every inferred value must be documented in `summary.notes`.

## Activity Recording Rules

### Study

Only record study sessions that actually occurred.

```json
"study": []
```

means no study session was completed or recorded.

---

### Walks

Only record walks that actually occurred.

```json
"walks": []
```

means no walk was completed or recorded.

---

### Meals

Only record meals that were actually eaten.

If a meal was skipped, do not create an empty meal object.

Example:

If lunch was skipped:

```json
"meals": []
```

or simply omit the lunch entry.

---

### Sleep

Only record completed sleep sessions.

---

### Workout (Exception)

Workout tracking is different because LifeOS tracks adherence to the 90-Day Transformation.

Therefore:

- A completed workout must be recorded using:

```json
{
    "status": "Completed",
    ...
}
```

- An intentionally skipped workout must be recorded using:

```json
{
    "status": "Skipped",
    "reason": "...",
    "notes": ""
}
```

An empty workout array

```json
"workout": []
```

means workout information has not yet been recorded.

## Field Definitions

The following definitions describe the purpose of each field in the daily JSON.

### Study Session

```json
{
    "subject": "",
    "topic": "",
    "start": "",
    "end": "",
    "notes": "",
    "key_learnings": [],
    "review_topics": []
}
```

| Field | Purpose |
|--------|---------|
| `subject` | Broad category of study (e.g., Python, Git, SQL, BCA, Data Structures). |
| `topic` | Specific lesson, chapter, project, or concept studied. |
| `start` | ISO 8601 timestamp indicating when the study session began. |
| `end` | ISO 8601 timestamp indicating when the study session ended. |
| `notes` | Context, observations, challenges, or additional information that doesn't fit elsewhere. |
| `key_learnings` | Concepts, skills, or ideas successfully understood during the session. |
| `review_topics` | Concepts that require further revision or were not fully understood. |

### Guidelines

- `subject` should remain broad and consistent across sessions.
- `topic` should be as specific as possible.
- `notes` should provide context rather than duplicate information stored elsewhere.
- `key_learnings` should only contain concepts that were genuinely learned.
- `review_topics` should contain concepts that need to be revisited in future study sessions.

### Session and Module Convention

LifeOS distinguishes between a **study session** and a **module**.

- **Session** → One uninterrupted period of study.
- **Module** → A larger unit of learning (course chapter, project phase, or topic) that may span multiple study sessions.

No additional JSON field should be introduced for modules.

Instead, use the `notes` field to indicate module or project progress.

Examples:

```
Module: Version Control: Git (Part 1 of 2).
```

```
Module: Version Control: Git (Part 2 of 2). Module completed.
```

Projects, internships, and long-term work follow the same convention.

Examples:

```
Project: Simple Calculator (Session 2). Implemented calculator operations.
```

```
Project: Simple Calculator (Final Session). Project completed and pushed to GitHub.
```

```
Project: ApexPlanet Task 3 (Session 1).
```

```
Project: ApexPlanet Task 3 (Final Session). Task completed.
```

This convention allows long-running learning modules and projects to span multiple study sessions without introducing additional JSON fields.

---

### Consistency Rule

Use consistent names for recurring subjects.

Examples:

- Python
- Git
- SQL
- Power BI
- BCA
- Machine Learning

Avoid using multiple names for the same subject unless they genuinely refer to different subjects.

For example, always use:

```
Python
```

instead of mixing:

```
Python
Python Programming
Py
CWH Python
```

This ensures long-term analytics remain accurate.

### Consistency Rule

Use consistent names for recurring subjects.

Examples:

- Python
- Git
- SQL
- Power BI
- BCA
- Machine Learning

Avoid using multiple names for the same subject unless they genuinely refer to different subjects.

For example, always use:

```
Python
```

instead of mixing:

```
Python
Python Programming
Py
CWH Python
```

This ensures long-term analytics remain accurate.

---

# 4. Inference Priority

Always follow this order:

1. Explicit user information.
2. Clarifying question.
3. Agreed LifeOS inference rule.
4. `null`

---

# 5. Daily JSON Workflow

1. Gather information throughout the day.
2. Identify important missing information.
3. Ask concise clarification questions when appropriate.
4. Apply agreed LifeOS inference rules when necessary.
5. Generate the final daily JSON.

---

# Current LifeOS Inference Rules

LifeOS currently supports the following inference rules:

- **Sleep (Main Sleep):** Infer sleep start time using the agreed sleep inference rule when the required conditions are met.
- **Sleep (Naps):** Create nap sessions automatically using conversation timestamps when the user later reports waking up.
- **Study:** Treat uninterrupted study as one continuous study session.
- **Workout:** Treat brief interruptions as part of the same workout session.
- **Meals:** Infer meal end time as **30 minutes after the recorded start time** when no end time is provided.

---

# Design Philosophy

LifeOS follows these principles:

- The daily JSON is the single source of truth.
- Generated reports should be derived from the daily JSON, not stored as independent data.
- The JSON schema is considered stable and should only change when a genuine functional requirement exists.
- Store facts rather than derived values.
- Prefer explicit user information over inference.
- Every module should have a single responsibility.
- Application code adapts to the data model, not the other way around.
