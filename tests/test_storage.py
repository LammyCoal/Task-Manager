from datetime import date
from src.task_manager.models import Task
from src.task_manager.storage import load_tasks,save_tasks

def test_save_and_load_tasks(tmp_path):
    data_file = tmp_path / "tasks.json"
