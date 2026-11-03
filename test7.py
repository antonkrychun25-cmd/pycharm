from datetime import datetime
import unittest
from unittest.mock import patch
from uuid import uuid4

from model import TaskManager, TaskStatus
import lab7


class TestTaskManagerModel(unittest.TestCase):


    def setUp(self):
        self.manager = TaskManager()
        self.now = datetime.now()

    def test_model_methods(self):

        task = self.manager.add_task("Test task", self.now)
        self.assertEqual(self.manager.get_task(task.id), task)
        self.assertEqual(len(self.manager.get_tasks()), 1)


        self.manager.update_task(task.id, description="New desc", status=TaskStatus.COMPLETED)
        self.assertEqual(task.status, TaskStatus.COMPLETED)
        self.assertEqual(len(self.manager.filter_by_status(TaskStatus.COMPLETED)), 1)


        self.assertTrue(self.manager.delete_task(task.id))
        self.assertFalse(self.manager.delete_task(uuid4()))
        self.assertIsNone(self.manager.update_task(uuid4(), description="None"))

        with self.assertRaises(ValueError):
            self.manager.get_task(uuid4())


class TestFullAppScenario(unittest.TestCase):


    def test_complete_menu_flow(self):

        fake_id = "11111111-1111-1111-1111-111111111111"

        user_inputs = [
            "1", "Купити хліб", "2026-12-31 15:00",
            "5",
            "6", "1",
            "6", "2",
            "6", "3",
            "6", "99",
            "7", fake_id,
            "2", fake_id,
            "3", fake_id,
            "4", fake_id,
            "99",
            "0",
        ]

        with patch("builtins.input", side_effect=user_inputs):
            lab7.main()


if __name__ == "__main__":
    unittest.main()