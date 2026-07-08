# LifeOS Rules

These rules define how daily logs are generated and maintained.

---

## Rule — Schema Stability

The LifeOS JSON schema is considered stable.

Do not add, remove, or rename fields unless there is a genuine functional requirement.

Application code should adapt to the schema, not the other way around.

---

# 1. Core Principles

## Rule 1 — Never invent data

Only record information that is either:

- Explicitly provided
- Confirmed by the user
- Inferred using an agreed LifeOS inference rule

---

## Rule 2 — Prefer explicit data

If exact information is available, always use it.

Example:

Workout:
07:50–08:50

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

"I know you had breakfast.
Do you remember approximately what time?"

---

## Rule 4 — Use inference only when appropriate

If the user does not know the answer, apply an agreed LifeOS inference rule.

All inferred values must be documented in the `notes` field.

---

# 2. Inference Rules

## Sleep

If:

- Lunch time is known
- No activity is recorded afterward
- Sleep ends at a known time

Then:

Infer sleep start approximately 2–3 hours after lunch.

---

## Study

If:

- Study begins
- No interruption is mentioned
- Study ends at a known time

Treat it as one continuous study session.

---

## Workout

If:

- Workout is briefly interrupted
- Workout resumes afterward

Treat it as one workout session.

Only create another session if a completely separate workout is performed.

---

## Meals

If the user says:

Egg Curry and Rice

Store:

```json
"food": [
    "Egg Curry",
    "Rice"
]
```

---

# 3. Data Standards

- Use ISO 8601 datetime format everywhere.
- Sleep belongs to the day the user wakes up.
- Do not store derived values.
- Do not invent ratings.
- Keep the schema minimal and consistent.
- Record inferred values inside `notes`.

---

# 4. Inference Priority

Always follow this order:

1. Explicit information
2. Clarifying question
3. Agreed inference rule
4. `null`

---

# 5. Daily JSON Workflow

1. Gather information throughout the day.
2. Identify important missing information.
3. Ask concise clarification questions.
4. Apply agreed inference rules.
5. Generate the final JSON.
