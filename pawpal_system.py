"""PawPal+ system skeleton.

Skeleton classes generated from the UML class diagram (see diagrams/uml.mmd).
No logic yet — attributes and empty method stubs only.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Task:
    description: str
    time: str
    duration: int
    priority: int
    frequency: str
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

    def get_all_tasks(self) -> list[Task]:
        ...


class Scheduler:
    def __init__(self, owner: Owner) -> None:
        self.owner: Owner = owner

    def generate_plan(self) -> list[Task]:
        ...

    def explain_reasoning(self) -> str:
        ...
