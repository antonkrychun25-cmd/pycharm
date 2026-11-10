from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from uuid import UUID, uuid4


class TaskState(Enum):
    PENDING = "Pending"
    IN_PROGRESS = "In Progress"
    DONE = "Done"


@dataclass
class TodoItem:
    content: str
    target_time: datetime
    uid: UUID = field(default_factory=uuid4)
    timestamp: datetime = field(default_factory=datetime.now)
    state: TaskState = TaskState.PENDING

    def set_state(self, new_state: TaskState) -> None:
        self.state = new_state


class TaskRepository:

    def __init__(self):
        self.repository: dict[UUID, TodoItem] = {}

    def create_item(self, content: str, target_time: datetime) -> TodoItem:
        item = TodoItem(content=content, target_time=target_time)
        self.repository[item.uid] = item
        return item

    def fetch_by_id(self, item_id: UUID) -> TodoItem | None:
        if item_id not in self.repository:
            raise ValueError("Item with specified UUID does not exist.")
        return self.repository.get(item_id)

    def fetch_all(self) -> list[TodoItem]:
        return list(self.repository.values())

    def modify_item(
        self,
        item_id: UUID,
        content: str = None,
        target_time: datetime = None,
        state: TaskState = None,
    ) -> TodoItem | None:
        try:
            item = self.fetch_by_id(item_id)
        except ValueError:
            return None

        if not item:
            return None
        if content is not None:
            item.content = content
        if target_time is not None:
            item.target_time = target_time
        if state is not None:
            item.set_state(state)
        return item

    def remove_item(self, item_id: UUID) -> bool:
        try:
            item = self.fetch_by_id(item_id)
        except ValueError:
            return False

        if item:
            self.repository.pop(item_id)
            return True
        return False

    def filter_by_state(self, state: TaskState) -> list[TodoItem]:
        return [itm for itm in self.repository.values() if itm.state == state]