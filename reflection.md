# PawPal+ Project Reflection

## 1. System Design
My uML has four classes: Owner, Pet, Task, and Scheduler. Owner manages a list of pets. Pet holds the pet's basic info and a list of its tasks. Task holds the details for one task like time, priority, and how often it repeats. Scheduler pulls tasks from the owner's pets and figures out the best daily schedule.
Owner: manages the list of pets and can pull all their tasks together
Pet: stores its own info and manages its list of tasks
Task: represents one task's details like time, priority, and frequency, and tracks if it's done
Scheduler: takes all the tasks and builds the daily plan

**a. Initial design**

My initial UML had four classes. **Owner** stores a name and a list of Pets, and can add pets and gather all their tasks. **Pet** stores a name, species, and a list of Tasks, and can add tasks. **Task** holds one task's details — description, time, duration, priority, frequency, and a completed flag — and can mark itself complete. **Scheduler** takes an Owner and produces a daily plan, plus an explanation of its reasoning. Relationships: Owner aggregates many Pets, Pet composes many Tasks, and Scheduler depends on the Owner to reach the tasks.

**b. Design changes**

Yes. Reviewing the skeleton revealed three problems and I changed the design:

1. **Lost pet context.** `get_all_tasks()` originally returned a flat `list[Task]`, so once tasks were flattened the Scheduler couldn't tell which pet a task belonged to — making a useful explanation ("Feed Rex at 8am") impossible. I changed it to return `list[tuple[Pet, Task]]` so the pet stays attached without adding a two-way Task→Pet dependency.
2. **Untyped scheduling data.** `time` and `frequency` were plain strings, but strings don't sort by time (`"10am" < "8am"`) and can't be reasoned about. I switched `time` to `datetime.time` and `frequency` to a `Frequency` enum so `generate_plan()` can actually order and expand tasks.
3. **Scheduler flexibility + state.** I widened the constructor to accept `Owner | list[Task]` (matching the original "Owner or list of tasks" idea) and added a cached `_plan` field so `explain_reasoning()` explains the plan `generate_plan()` produced instead of recomputing it.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
