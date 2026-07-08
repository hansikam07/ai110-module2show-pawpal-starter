"""Tests for the PawPal+ system."""

from datetime import time

from pawpal_system import Frequency, Pet, Task


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
