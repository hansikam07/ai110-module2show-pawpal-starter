"""PawPal+ system skeleton.

Skeleton classes generated from the UML class diagram (see diagrams/uml.mmd).
No logic yet — attributes and empty method stubs only.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import time
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
    # NOTE: a single bool can't track "done today but due again tomorrow"
    # for recurring tasks — revisit once recurrence logic is added.
    completed: bool = False

    def mark_complete(self) -> None:
        ...


@dataclass
class Pet:
    name: str
    species: str
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        ...


class Owner:
    def __init__(self, name: str) -> None:
        self.name: str = name
        self.pets: list[Pet] = []

    def add_pet(self, pet: Pet) -> None:
        ...

    def get_all_tasks(self) -> list[tuple[Pet, Task]]:
        # Returns (pet, task) pairs so callers keep track of which pet
        # each task belongs to after flattening.
        ...


class Scheduler:
    def __init__(self, source: Owner | list[Task]) -> None:
        # Accepts either an Owner (schedule all its pets' tasks) or a
        # standalone list of tasks (ad-hoc scheduling).
        self.source: Owner | list[Task] = source
        self._plan: list[Task] = []

    def generate_plan(self) -> list[Task]:
        ...

    def explain_reasoning(self) -> str:
        # Explains self._plan produced by generate_plan().
        ...
