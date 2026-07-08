"""PawPal+ system implementation.

Classes generated from the UML class diagram (see diagrams/uml.mmd) and
implemented per the design decisions recorded in reflection.md:
  - pet context is preserved by returning (Pet, Task) pairs,
  - time/frequency are typed (datetime.time / Frequency enum),
  - the Scheduler caches its plan so explain_reasoning() stays consistent.

Priority convention: a HIGHER priority number means MORE important.
"""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field
from datetime import date, time, timedelta
from enum import Enum


class Frequency(Enum):
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"


@dataclass
class Task:
    description: str
    time: time
    duration: int  # minutes
    priority: int
    frequency: Frequency
    completed: bool = False
    due_date: date = field(default_factory=date.today)

    def next_occurrence(self) -> Task:
        """Return a fresh, incomplete copy of this task with due_date advanced by its frequency."""
        step = {
            Frequency.DAILY: timedelta(days=1),
            Frequency.WEEKLY: timedelta(weeks=1),
            Frequency.MONTHLY: timedelta(days=30),
        }[self.frequency]
        return Task(
            self.description,
            self.time,
            self.duration,
            self.priority,
            self.frequency,
            completed=False,
            due_date=self.due_date + step,
        )

    def mark_complete(self) -> Task | None:
        """Mark this task complete; return the next occurrence for recurring tasks, else None."""
        self.completed = True
        if self.frequency in (Frequency.DAILY, Frequency.WEEKLY, Frequency.MONTHLY):
            return self.next_occurrence()
        return None


@dataclass
class Pet:
    name: str
    species: str
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a task to this pet's task list."""
        self.tasks.append(task)


class Owner:
    def __init__(self, name: str) -> None:
        """Create an owner with a name and an empty list of pets."""
        self.name: str = name
        self.pets: list[Pet] = []

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner."""
        self.pets.append(pet)

    def get_all_tasks(self) -> list[tuple[Pet, Task]]:
        """Return every pet's tasks as (pet, task) pairs."""
        # Returns (pet, task) pairs so callers keep track of which pet
        # each task belongs to after flattening.
        return [(pet, task) for pet in self.pets for task in pet.tasks]


class Scheduler:
    def __init__(self, source: Owner | list[Task]) -> None:
        """Create a scheduler from an owner or a standalone list of tasks."""
        # Accepts either an Owner (schedule all its pets' tasks) or a
        # standalone list of tasks (ad-hoc scheduling). Normalize both to
        # (pet, task) pairs so downstream logic is uniform; pet is None
        # when scheduling a bare task list.
        self.source: Owner | list[Task] = source
        if isinstance(source, Owner):
            self._pairs: list[tuple[Pet | None, Task]] = list(source.get_all_tasks())
        else:
            self._pairs = [(None, task) for task in source]

        self._plan: list[Task] = []
        self._plan_pairs: list[tuple[Pet | None, Task]] = []
        self._log: list[tuple[str, Pet | None, Task, str]] = []
        self._max_minutes: int = 0
        self._used_minutes: int = 0
        self._generated: bool = False

    def sort_by_time(self) -> list[tuple[Pet | None, Task]]:
        """Return all (pet, task) pairs sorted by task.time ascending."""
        return sorted(self._pairs, key=lambda pt: pt[1].time)

    def filter_tasks(
        self, pet_name: str | None = None, completed: bool | None = None
    ) -> list[tuple[Pet | None, Task]]:
        """Return (pet, task) pairs filtered by pet name and/or completion status."""
        return [
            (pet, task)
            for pet, task in self._pairs
            if (pet_name is None or (pet is not None and pet.name == pet_name))
            and (completed is None or task.completed == completed)
        ]

    def detect_conflicts(self) -> list[str]:
        """Return warning strings for any tasks that share the exact same time."""
        by_time: dict[time, list[tuple[Pet | None, Task]]] = defaultdict(list)
        for pet, task in self._pairs:
            by_time[task.time].append((pet, task))

        warnings: list[str] = []
        for t, group in by_time.items():
            if len(group) > 1:
                names = ", ".join(
                    f"'{task.description}' ({pet.name if pet is not None else 'unassigned'})"
                    for pet, task in group
                )
                warnings.append(f"Conflict at {t.strftime('%H:%M')}: {names}")
        return warnings

    def generate_plan(self, max_minutes: int) -> list[Task]:
        """Build a daily plan constrained to ``max_minutes`` of total time.

        Selection is greedy by importance: consider tasks from highest to
        lowest priority (ties broken by shorter duration first, then earlier
        time) and include each one whose duration still fits in the remaining
        budget. Already-completed tasks are skipped. The chosen tasks are then
        ordered by time of day to read as a daily schedule.
        """
        # Decision order: priority desc, then shorter first, then earlier time.
        candidates = sorted(
            self._pairs,
            key=lambda pt: (-pt[1].priority, pt[1].duration, pt[1].time),
        )

        used = 0
        selected: list[tuple[Pet | None, Task]] = []
        log: list[tuple[str, Pet | None, Task, str]] = []

        for pet, task in candidates:
            if task.completed:
                log.append(("skip", pet, task, "already completed"))
                continue
            remaining = max_minutes - used
            if task.duration <= remaining:
                selected.append((pet, task))
                used += task.duration
                log.append(
                    ("include", pet, task, f"fits ({used}/{max_minutes} min used)")
                )
            else:
                log.append(
                    (
                        "exclude",
                        pet,
                        task,
                        f"needs {task.duration} min but only {remaining} left",
                    )
                )

        # Final schedule is ordered by time of day.
        ordered = sorted(selected, key=lambda pt: pt[1].time)

        self._plan_pairs = ordered
        self._plan = [task for _pet, task in ordered]
        self._log = log
        self._max_minutes = max_minutes
        self._used_minutes = used
        self._generated = True
        return self._plan

    def explain_reasoning(self) -> str:
        """Return a human-readable explanation of the cached plan."""
        if not self._generated:
            return "No plan generated yet. Call generate_plan(max_minutes) first."

        def label(pet: Pet | None, task: Task) -> str:
            who = pet.name if pet is not None else "unassigned"
            return f"'{task.description}' for {who}"

        lines: list[str] = []
        lines.append(
            f"Daily plan: {self._used_minutes}/{self._max_minutes} minutes scheduled "
            f"across {len(self._plan)} task(s)."
        )
        lines.append("")
        lines.append("Selection (highest priority first, fit by remaining time):")
        for action, pet, task, reason in self._log:
            mark = {"include": "✓", "exclude": "✗", "skip": "–"}[action]
            lines.append(
                f"  {mark} {label(pet, task)} "
                f"[priority {task.priority}, {task.duration} min] — {reason}"
            )

        lines.append("")
        if self._plan_pairs:
            lines.append("Final order (by time of day):")
            for pet, task in self._plan_pairs:
                lines.append(
                    f"  {task.time.strftime('%H:%M')}  {label(pet, task)} "
                    f"({task.duration} min, priority {task.priority})"
                )
        else:
            lines.append("Final order: no tasks fit within the time budget.")

        return "\n".join(lines)
