import pytest
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from database8 import Base
from model8 import TaskRepository, TaskState


TEST_DATABASE_URL = "sqlite:///:memory:"

@pytest.fixture
def test_repo():
    engine = create_engine(
        TEST_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)

    repo = TaskRepository(session_factory=TestingSessionLocal)
    yield repo

    Base.metadata.drop_all(bind=engine)

def test_create_and_get_task(test_repo):
    now = datetime.now()
    task = test_repo.create("Test Task", now)
    assert task.id is not None
    assert task.content == "Test Task"
    assert task.state == TaskState.PENDING

    tasks = test_repo.get_all()
    assert len(tasks) == 1

def test_update_state(test_repo):
    task = test_repo.create("Task for update", datetime.now())
    updated = test_repo.update_state(task.id, TaskState.DONE)
    assert updated is True

    fetched = test_repo.get_by_id(task.id)
    assert fetched.state == TaskState.DONE

def test_delete_task(test_repo):
    task = test_repo.create("Task to delete", datetime.now())
    deleted = test_repo.delete(task.id)
    assert deleted is True

    fetched = test_repo.get_by_id(task.id)
    assert fetched is None