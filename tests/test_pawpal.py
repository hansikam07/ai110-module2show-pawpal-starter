"""Tests for the PawPal+ system."""

from datetime import date, time, timedelta

from pawpal_system import Frequency, Owner, Pet, Scheduler, Task


def test_mark_complete():
    task = Task("Morning walk", time(7, 30), 40, 6, Frequency.DAILY)
    assert task.completed is False
    task.mark_complete()
    assert task.completed is True


def test_add_task_increases_count():
    pet = Pet("Rex", "dog")
    assert len(pet.tasks) == 0
    pet.add_task(Task("Feed breakfast", time(8, 0), 10, 8, Frequency.DAILY))
    assert len(pet.tasks) == 1


def test_sort_by_time_chronological():
    pet = Pet("Rex", "dog")
    # Added deliberately out of chronological order.
    pet.add_task(Task("Evening walk", time(20, 0), 30, 5, Frequency.DAILY))
    pet.add_task(Task("Morning walk", time(7, 30), 40, 6, Frequency.DAILY))
    pet.add_task(Task("Midday water", time(12, 0), 5, 7, Frequency.DAILY))
    owner = Owner("Alex")
    owner.add_pet(pet)

    scheduler = Scheduler(owner)
    times = [task.time for _pet, task in scheduler.sort_by_time()]

    assert times == [time(7, 30), time(12, 0), time(20, 0)]


def test_recurring_task_creates_next_occurrence():
    task = Task("Morning walk", time(7, 30), 40, 6, Frequency.DAILY, due_date=date(2026, 7, 8))
    next_task = task.mark_complete()

    assert task.completed is True
    assert next_task is not None
    assert next_task.completed is False
    assert next_task.due_date == task.due_date + timedelta(days=1)


def test_detect_conflicts_flags_duplicate_times():
    rex = Pet("Rex", "dog")
    luna = Pet("Luna", "cat")
    rex.add_task(Task("Brush teeth", time(9, 0), 5, 4, Frequency.DAILY))
    luna.add_task(Task("Morning meds", time(9, 0), 5, 9, Frequency.DAILY))
    owner = Owner("Alex")
    owner.add_pet(rex)
    owner.add_pet(luna)

    conflicts = Scheduler(owner).detect_conflicts()
    assert len(conflicts) == 1
    assert "Brush teeth" in conflicts[0]
    assert "Morning meds" in conflicts[0]

    # No two tasks share a time -> no conflicts.
    calm = Pet("Milo", "dog")
    calm.add_task(Task("Feed breakfast", time(8, 0), 10, 8, Frequency.DAILY))
    calm.add_task(Task("Evening walk", time(20, 0), 30, 5, Frequency.DAILY))
    calm_owner = Owner("Sam")
    calm_owner.add_pet(calm)
    assert Scheduler(calm_owner).detect_conflicts() == []
