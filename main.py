"""Demo driver for the PawPal+ system.

Builds a small owner/pet/task setup, generates a daily plan under a time
budget, and prints the schedule with the scheduler's reasoning.
"""

from datetime import time

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


if __name__ == "__main__":
    main()
