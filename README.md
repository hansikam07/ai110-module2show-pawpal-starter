# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## ✨ Features

PawPal+ implements the followinPawPal+ implements the following scheduling algorithms (see pawpal_system.py):
Sorting by time. Scheduler.sort_by_time() returns every (pet, task) pair in order of time of day, no matter what order the tasks were added in.
Filtering by pet or completion status. Scheduler.filter_tasks(pet_name, completed) narrows the task list to a specific pet, a completion status, or both. Both filters are optional.
Conflict detection. Scheduler.detect_conflicts() flags tasks that land on the exact same time. Tasks are grouped by time instead of compared pairwise, so if three or more tasks clash at once, you get a single combined warning instead of several repeated ones.
Daily, weekly, and monthly recurrence. Completing a recurring task through Task.mark_complete() automatically generates the next occurrence via Task.next_occurrence(), pushing the due date forward by 1 day, 1 week, or 30 days depending on frequency. One-off tasks (ONE_TIME) don't recur and just return None when completed.
Priority-aware daily planning. Scheduler.generate_plan(max_minutes) greedily picks tasks by priority within a set time budget, and explain_reasoning() walks through why each decision was made.

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

Paste a sample of your app's CLI or Streamlit output here so a reader can see what a generated plan looks like:

============================================
  Today's Schedule for Alex  (budget: 120 min)
============================================
  1. 07:30  Morning walk  (40 min, priority 6)
  2. 08:00  Feed breakfast  (10 min, priority 8)
  3. 15:00  Vet appointment  (60 min, priority 9)

--------------------------------------------
  Why this plan?
--------------------------------------------
Daily plan: 110/120 minutes scheduled across 3 task(s).

Selection (highest priority first, fit by remaining time):
  ✓ 'Vet appointment' for Rex [priority 9, 60 min] — fits (60/120 min used)
  ✓ 'Feed breakfast' for Luna [priority 8, 10 min] — fits (70/120 min used)
  ✓ 'Morning walk' for Rex [priority 6, 40 min] — fits (110/120 min used)
  ✗ 'Play & grooming' for Luna [priority 4, 45 min] — needs 45 min but only 10 left

Final order (by time of day):
  07:30  'Morning walk' for Rex (40 min, priority 6)
  08:00  'Feed breakfast' for Luna (10 min, priority 8)
  15:00  'Vet appointment' for Rex (60 min, priority 9)

## 🧪 Testing PawPal+

Run the test suite with:

```bash
python -m pytest
```

Tests cover:
- Task completion (`mark_complete()` correctly flips the completed flag)
- Task addition (adding a task increases a pet's task count)
- Sorting correctness (`sort_by_time()` returns tasks in chronological order regardless of insertion order)
- Recurrence logic (completing a DAILY task auto-generates the next occurrence with `due_date` advanced by 1 day)
- Conflict detection (`detect_conflicts()` flags tasks scheduled at the exact same time, and returns an empty list when there are none)

Sample test output:

```
======================== test session starts ========================
platform darwin -- Python 3.14.5, pytest-9.1.1, pluggy-1.6.0
collected 5 items                                                   
tests/test_pawpal.py::test_mark_complete PASSED               [ 20%]
tests/test_pawpal.py::test_add_task_increases_count PASSED    [ 40%]
tests/test_pawpal.py::test_sort_by_time_chronological PASSED  [ 60%]
tests/test_pawpal.py::test_recurring_task_creates_next_occurrence PASSED [ 80%]
tests/test_pawpal.py::test_detect_conflicts_flags_duplicate_times PASSED [100%]
========================= 5 passed in 0.02s =========================
```

**Confidence Level:** ⭐⭐⭐ (3/5) — Core scheduling, sorting, recurrence, and conflict detection are all verified. Known limitation: conflict detection only checks exact time matches, not overlapping durations (documented in reflection.md).

## 📐 Smarter Scheduling

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | `Scheduler.sort_by_time()` | Returns all (pet, task) pairs sorted by time ascending |
| Filtering | `Scheduler.filter_tasks(pet_name=None, completed=None)` | Filters by pet name and/or completion status, either optional |
| Conflict handling | `Scheduler.detect_conflicts()` | Groups tasks by exact time match, returns one consolidated warning per shared time slot (O(n)) |
| Recurring tasks | `Task.next_occurrence()`, `Task.mark_complete()` | Completing a DAILY/WEEKLY/MONTHLY task auto-generates the next occurrence with due_date advanced accordingly |

## 📸 Demo Walkthrough

### What you can do in the app

Launch the Streamlit UI with `streamlit run app.py`. From there you can:

- **Add a pet** — enter a name and species, then click **Add pet**. Pets persist across interactions via Streamlit session state.
- **Add tasks** — pick a pet, then set a task title, duration, priority (low/medium/high), time of day, and frequency (one-time / daily / weekly / monthly), and click **Add task**.
- **Filter and sort the task table** — use *Filter by pet* and *Show only incomplete tasks* to narrow the list, and toggle *Sort tasks by time* to view it chronologically. These are backed by `Scheduler.filter_tasks()` and `Scheduler.sort_by_time()`.
- **Generate a daily schedule** — set a time budget (in minutes) and click **Generate schedule** to see the plan and the scheduler's reasoning.
- **See conflict warnings** — after generating a schedule, any tasks sharing the exact same time are surfaced as warnings via `Scheduler.detect_conflicts()`.

### Example workflow

1. Add a pet named **Mochi** (dog).
2. Add a task: *Morning walk*, 20 min, high priority, 07:30, daily.
3. Add a second task at the same time for a different pet to see a conflict warning.
4. Set a time budget (e.g. 120 minutes) and click **Generate schedule**.
5. Read *Today's Schedule* and the *Why this plan?* explanation; toggle *Sort tasks by time* to reorder the task table.

### Key Scheduler behaviors demonstrated

- **Sorting** — tasks added out of order are displayed chronologically.
- **Conflict warnings** — two tasks at the same time (e.g. 09:00) produce a single consolidated warning.
- **Recurrence** — completing a daily task advances its `due_date` by one day and produces the next occurrence.

### Sample CLI output

Running `python main.py` produces the full end-to-end demo below (scheduling, sorting, filtering, recurrence, and conflict detection):

```
============================================
  Today's Schedule for Alex  (budget: 120 min)
============================================
  1. 07:30  Morning walk  (40 min, priority 6)
  2. 08:00  Feed breakfast  (10 min, priority 8)
  3. 15:00  Vet appointment  (60 min, priority 9)

--------------------------------------------
  Why this plan?
--------------------------------------------
Daily plan: 110/120 minutes scheduled across 3 task(s).

Selection (highest priority first, fit by remaining time):
  ✓ 'Vet appointment' for Rex [priority 9, 60 min] — fits (60/120 min used)
  ✓ 'Feed breakfast' for Luna [priority 8, 10 min] — fits (70/120 min used)
  ✓ 'Morning walk' for Rex [priority 6, 40 min] — fits (110/120 min used)
  ✗ 'Play & grooming' for Luna [priority 4, 45 min] — needs 45 min but only 10 left

Final order (by time of day):
  07:30  'Morning walk' for Rex (40 min, priority 6)
  08:00  'Feed breakfast' for Luna (10 min, priority 8)
  15:00  'Vet appointment' for Rex (60 min, priority 9)

--------------------------------------------
  Sorted by time
--------------------------------------------
  06:45  Litter cleanup  (Luna)
  07:30  Morning walk  (Rex)
  08:00  Feed breakfast  (Luna)
  12:00  Midday water refill  (Rex)
  15:00  Vet appointment  (Rex)
  18:30  Play & grooming  (Luna)
  20:00  Evening walk  (Rex)

--------------------------------------------
  Filtered: incomplete tasks for Luna
--------------------------------------------
  18:30  Play & grooming  (Luna)
  06:45  Litter cleanup  (Luna)

--------------------------------------------
  Recurring task demo
--------------------------------------------
  Original: due 2026-07-08, completed=True
  Next up:  due 2026-07-09, completed=False

--------------------------------------------
  Conflict detection demo
--------------------------------------------
  Conflict at 09:00: 'Brush teeth' (Rex), 'Morning meds' (Luna)
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
