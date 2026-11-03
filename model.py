from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from uuid import UUID, uuid4


class TaskStatus(Enum):
    TODO = "Todo"
    IN_PROGRESS = "In Progress"
    COMPLETED = "Completed"


@dataclass
class Task:
    description: str
    scheduled_at: datetime
    id: UUID = field(default_factory=uuid4)
    created_at: datetime = field(default_factory=datetime.now)
    status: TaskStatus = TaskStatus.TODO

    def change_status(self, new_status: TaskStatus) -> None:
        self.status = new_status


class TaskManager:
    def __init__(self):
        self.tasks: dict[UUID, Task] = {}

    def add_task(self, description: str, scheduled_at: datetime) -> Task:
        task = Task(description=description, scheduled_at=scheduled_at)
        self.tasks[task.id] = task
        return task

    def get_task(self, task_id: UUID) -> Task | None:
        if task_id not in self.tasks:
            raise ValueError("Task with such ID does not exist.")
        return self.tasks.get(task_id)

    def get_tasks(self) -> list[Task]:
        return list(self.tasks.values())

    def update_task(
        self,
        task_id: UUID,
        description: str = None,
        scheduled_at: datetime = None,
        status: TaskStatus = None,
    ) -> Task | None:
        try:
            task = self.get_task(task_id)
        except ValueError:
            return None

        if not task:
            return None
        if description is not None:
            task.description = description
        if scheduled_at is not None:
            task.scheduled_at = scheduled_at
        if status is not None:
            task.change_status(status)
        return task

    def delete_task(self, task_id: UUID) -> bool:
        try:
            task = self.get_task(task_id)
        except ValueError:
            return False

        if task:
            self.tasks.pop(task_id)
            return True
        return False

    def filter_by_status(self, status: TaskStatus) -> list[Task]:
        return [t for t in self.tasks.values() if t.status == status]