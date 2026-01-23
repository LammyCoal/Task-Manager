from datetime import date

import pytest
from src.task_manager.models import Task
from src.task_manager.storage import load_tasks,save_tasks

def test_storage(tmp_path):
    data_file = tmp_path / "tasks.json"

    tasks = [Task("Test storage.py", "high",date(2026,1,24)),
             Task("finish project",due_date=date(2026,1,25)),
             Task("celebrate birthday","high", date(2026,2,22))
             ]

    save_tasks(tasks, path=data_file)
    loaded_tasks = load_tasks(path=data_file)

    assert len(loaded_tasks) == 3
    assert loaded_tasks[0].due_date == date(2026,1,24)
    assert loaded_tasks[2].due_date == date(2026,2,22)
    assert loaded_tasks[1].due_date == date(2026,1,25)
    assert loaded_tasks[0].title == "Test storage.py"
    assert loaded_tasks[1].title == "finish project"
    assert loaded_tasks[2].title == "celebrate birthday"
    assert loaded_tasks[0].priority == "high"
    assert loaded_tasks[1].priority == "medium"
    assert loaded_tasks[2].priority == "high"
    assert loaded_tasks[0].completed == False
    assert loaded_tasks[1].completed == False

def test_missing_file(tmp_path):
    """Used to test if loading from missing file returns an empty list"""
    data_file = tmp_path / "missed file"

    tasks = load_tasks(path=data_file)
    assert tasks == []

def test_completed_tasks(tmp_path):
    """Used to test if completed tasks survives loading and saving stage"""
    data_file = tmp_path / "tasks.json"

    tasks = Task("Testing completed tasks")
    tasks.mark_completed()
    save_tasks([tasks], path=data_file)

    loaded = load_tasks(path=data_file)

    assert loaded[0].completed == True

""" using pytest fixture"""
@pytest.fixture
def data_file(tmp_path):
    return tmp_path / "tasks.json"

@pytest.fixture
def sample_data():
    return  [Task("Testing using pytest fixture", "high",date(2026,1,24)),
             Task("Watch chelsea", "medium")
             ]

def test_load_and_save_tasks(data_file,sample_data):
    save_tasks(sample_data, path=data_file)
    loaded_tasks = load_tasks(path=data_file)

    assert loaded_tasks[0].title == "Testing using pytest fixture"
    assert loaded_tasks[1].title == "Watch chelsea"
    assert loaded_tasks[1].priority == "medium"
    assert len(loaded_tasks) == 2

def test_mark_completed_tasks(data_file,sample_data):
    sample_data[0].mark_completed()
    sample_data[1].mark_completed()

    save_tasks(sample_data, path=data_file)
    loaded_tasks = load_tasks(path=data_file)

    assert loaded_tasks[0].completed is True
    assert loaded_tasks[1].completed is True