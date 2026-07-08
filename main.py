"""Demo driver for the PawPal+ system.

Builds a small owner/pet/task setup, generates a daily plan under a time
budget, and prints the schedule with the scheduler's reasoning.
"""

from datetime import date, time

from pawpal_system import Frequency, Owner, Pet, Scheduler, Task


def main() -> None:
    # Owner and pets.
    alex = Owner("Alex")
    rex = Pet("Rex", "dog")
    luna = Pet("Luna", "cat")
    alex.add_pet(rex)
    alex.add_pet(luna)

    # Tasks across both pets — varied times, priorities, and durations.
    rex.add_task(Task("Morning walk", time(7, 30), 40, 6, Frequency.DAILY))
    rex.add_task(Task("Vet appointment", time(15, 0), 60, 9, Frequency.MONTHLY))
    luna.add_task(Task("Feed breakfast", time(8, 0), 10, 8, Frequency.DAILY))
    luna.add_task(Task("Play & grooming", time(18, 30), 45, 4, Frequency.DAILY))

    # Build the plan under a 2-hour budget.
    budget = 120
    scheduler = Scheduler(alex)
    plan = scheduler.generate_plan(max_minutes=budget)

    # Present the schedule readably.
    print("=" * 44)
    print(f"  Today's Schedule for {alex.name}  (budget: {budget} min)")
    print("=" * 44)

    if plan:
        for slot, task in enumerate(plan, start=1):
            print(
                f"  {slot}. {task.time.strftime('%H:%M')}  "
                f"{task.description}  "
                f"({task.duration} min, priority {task.priority})"
            )
    else:
        print("  No tasks fit within today's time budget.")

    print()
    print("-" * 44)
    print("  Why this plan?")
    print("-" * 44)
    print(scheduler.explain_reasoning())

    # Add a few more tasks deliberately out of chronological order so that
    # sort_by_time() has something visible to reorder. Rebuild the scheduler
    # afterwards so it sees the newly added tasks.
    rex.add_task(Task("Evening walk", time(20, 0), 30, 5, Frequency.DAILY))
    rex.add_task(Task("Midday water refill", time(12, 0), 5, 7, Frequency.DAILY))
    luna.add_task(Task("Litter cleanup", time(6, 45), 10, 8, Frequency.DAILY))
    luna.tasks[0].mark_complete()  # Feed breakfast is done for today.
    scheduler = Scheduler(alex)

    print()
    print("-" * 44)
    print("  Sorted by time")
    print("-" * 44)
    for pet, task in scheduler.sort_by_time():
        who = pet.name if pet is not None else "unassigned"
        print(f"  {task.time.strftime('%H:%M')}  {task.description}  ({who})")

    print()
    print("-" * 44)
    print("  Filtered: incomplete tasks for Luna")
    print("-" * 44)
    luna_todo = scheduler.filter_tasks(pet_name="Luna", completed=False)
    if luna_todo:
        for pet, task in luna_todo:
            print(f"  {task.time.strftime('%H:%M')}  {task.description}  ({pet.name})")
    else:
        print("  Nothing left to do for Luna.")

    print()
    print("-" * 44)
    print("  Recurring task demo")
    print("-" * 44)
    recurring = Task("Feed dinner", time(18, 0), 15, 8, Frequency.DAILY, due_date=date.today())
    upcoming = recurring.mark_complete()
    print(f"  Original: due {recurring.due_date}, completed={recurring.completed}")
    print(f"  Next up:  due {upcoming.due_date}, completed={upcoming.completed}")

    # Add two tasks at the same time (across both pets) to trigger a conflict,
    # then rebuild the scheduler so it sees them.
    rex.add_task(Task("Brush teeth", time(9, 0), 5, 4, Frequency.DAILY))
    luna.add_task(Task("Morning meds", time(9, 0), 5, 9, Frequency.DAILY))
    scheduler = Scheduler(alex)

    print()
    print("-" * 44)
    print("  Conflict detection demo")
    print("-" * 44)
    conflicts = scheduler.detect_conflicts()
    if conflicts:
        for warning in conflicts:
            print(f"  {warning}")
    else:
        print("  No conflicts found")


if __name__ == "__main__":
    main()
