from datetime import datetime
import unittest
from unittest.mock import patch
from uuid import uuid4

from model import TaskRepository, TaskState
import lab7


class TestRepositoryCore(unittest.TestCase):

    def setUp(self):
        self.repo = TaskRepository()
        self.current_dt = datetime.now()

    def test_repository_actions(self):
        item = self.repo.create_item("Test content", self.current_dt)
        self.assertEqual(self.repo.fetch_by_id(item.uid), item)
        self.assertEqual(len(self.repo.fetch_all()), 1)

        self.repo.modify_item(
            item.uid, content="Updated", state=TaskState.DONE
        )
        self.assertEqual(item.state, TaskState.DONE)
        self.assertEqual(len(self.repo.filter_by_state(TaskState.DONE)), 1)

        self.assertTrue(self.repo.remove_item(item.uid))
        self.assertFalse(self.repo.remove_item(uuid4()))
        self.assertIsNone(self.repo.modify_item(uuid4(), content="None"))

        with self.assertRaises(ValueError):
            self.repo.fetch_by_id(uuid4())


class TestApplicationFlow(unittest.TestCase):

    def test_full_menu_execution(self):
        dummy_uuid = "22222222-2222-2222-2222-222222222222"

        simulated_inputs = [
            "1", "Buy groceries", "2026-12-31 18:00",
            "5",
            "6", "1",
            "6", "2",
            "6", "3",
            "6", "99",
            "7", dummy_uuid,
            "2", dummy_uuid,
            "3", dummy_uuid,
            "4", dummy_uuid,
            "99",
            "0",
        ]

        with patch("builtins.input", side_effect=simulated_inputs):
            lab7.run_app()


if __name__ == "__main__":
    unittest.main()