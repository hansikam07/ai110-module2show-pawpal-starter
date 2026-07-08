# PawPal+ Project Reflection

## 1. System Design
My uML has four classes: Owner, Pet, Task, and Scheduler. Owner manages a list of pets. Pet holds the pet's basic info and a list of its tasks. Task holds the details for one task like time, priority, and how often it repeats. Scheduler pulls tasks from the owner's pets and figures out the best daily schedule.
Owner: manages the list of pets and can pull all their tasks together
Pet: stores its own info and manages its list of tasks
Task: represents one task's details like time, priority, and frequency, and tracks if it's done
Scheduler: takes all the tasks and builds the daily plan

**a. Initial design**
I have four classes. Owner just holds a name and a list of Pets, and can add pets or grab all their tasks in one go. Pet holds name, species, and its own list of Tasks, plus a way to add tasks. Task is the actual data, description, time, duration, priority, frequency, and whether it's done, and it can mark itself complete. Then Scheduler takes an Owner and spits out a daily plan along with an explanation of why it made those choices. As for how they connect, Owner has many Pets, Pet has many Tasks, and Scheduler needs the Owner to actually get at the tasks.

**b. Design changes**

Yes. Reviewing the skeleton surfaced three issues, which led to the following design changes:

1. Loss of pet context. get_all_tasks() originally returned a flat list[Task], so once tasks were flattened there was no way to tell which pet a given task belonged to. This made it impossible to generate a meaningful explanation such as "Feed Rex at 8am." I changed the return type to list[tuple[Pet, Task]] so each task retains a reference to its pet, without introducing a two way dependency between Task and Pet.
2. Untyped scheduling data. The time and frequency fields were originally plain strings, but strings do not sort correctly by time (for example, "10am" is less than "8am" as a string) and cannot be reasoned about programmatically. I

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?
My conflict detection only checks for exact time matches (task.time equality) rather than overlapping durations. This means a 07:30–08:10 walk and an 08:00 vet visit wouldn't be flagged as a conflict even though they overlap. I chose exact-match detection because it's simple and covers the most common real-world case (two tasks accidentally scheduled at the identical time), but a more robust version would compare time ranges using start/end times instead of a single timestamp.

I also switched detect_conflicts() from a pairwise O(n²) comparison to a group-by-time O(n) approach after reviewing both with my AI assistant. Beyond the performance difference (irrelevant at this scale), the group-by-time version produces a single consolidated warning when 3+ tasks clash at the same time, instead of redundant pairwise warnings — a better tradeoff for readability from a pet owner's perspective.

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
