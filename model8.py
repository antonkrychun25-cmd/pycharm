from datetime import datetime
from enum import Enum
from sqlalchemy import Column, Integer, String, DateTime, Enum as SQLEnum
from database8 import Base, SessionLocal

class TaskState(str, Enum):
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    DONE = "DONE"

class TodoItem(Base):
    __tablename__ = "todo_items"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String, nullable=False)
    target_time = Column(DateTime, nullable=False)
    state = Column(SQLEnum(TaskState), default=TaskState.PENDING, nullable=False)

class TaskRepository:
    def __init__(self, session_factory=SessionLocal):
        self.session_factory = session_factory

    def create(self, content: str, target_time: datetime) -> TodoItem:
        session = self.session_factory()
        try:
            item = TodoItem(content=content, target_time=target_time, state=TaskState.PENDING)
            session.add(item)
            session.commit()
            session.refresh(item)
            return item
        finally:
            session.close()

    def get_all(self):
        session = self.session_factory()
        try:
            return session.query(TodoItem).order_by(TodoItem.id).all()
        finally:
            session.close()

    def get_by_id(self, item_id: int):
        session = self.session_factory()
        try:
            return session.query(TodoItem).filter(TodoItem.id == item_id).first()
        finally:
            session.close()

    def update_state(self, item_id: int, new_state: TaskState) -> bool:
        session = self.session_factory()
        try:
            item = session.query(TodoItem).filter(TodoItem.id == item_id).first()
            if item:
                item.state = new_state
                session.commit()
                return True
            return False
        finally:
            session.close()

    def update_content(self, item_id: int, new_content: str) -> bool:
        session = self.session_factory()
        try:
            item = session.query(TodoItem).filter(TodoItem.id == item_id).first()
            if item:
                item.content = new_content
                session.commit()
                return True
            return False
        finally:
            session.close()

    def delete(self, item_id: int) -> bool:
        session = self.session_factory()
        try:
            item = session.query(TodoItem).filter(TodoItem.id == item_id).first()
            if item:
                session.delete(item)
                session.commit()
                return True
            return False
        finally:
            session.close()

    def filter_by_state(self, state: TaskState):
        session = self.session_factory()
        try:
            return session.query(TodoItem).filter(TodoItem.state == state).all()
        finally:
            session.close()