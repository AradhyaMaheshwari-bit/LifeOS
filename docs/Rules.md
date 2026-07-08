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

**If:**

- Lunch time is known.
- No activity is recorded afterward.
- Sleep ends at a known time.

**Then:**

Infer the sleep start time approximately **2 hours after lunch**.

Add the following to `summary.notes`:

> "Sleep start time inferred using the agreed LifeOS inference rule."

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

**If:**

- A workout is briefly interrupted.
- The workout resumes afterward.

**Then:**

Treat it as **the same workout session**.

Only create another workout session if the user clearly states it became a separate workout.

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

- **Sleep:** Infer sleep start time using the agreed sleep inference rule.
- **Study:** Treat uninterrupted study as one continuous study session.
- **Workout:** Treat brief interruptions as part of the same workout session.
- **Meals:** Infer meal end time as **30 minutes after the recorded start time** when no end time is provided.
