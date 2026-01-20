from datetime import date
from src.task_manager.models import Task

def test_create_task():
    task = Task("task testing", priority='high', due_date=date(2026,1,20))
    assert task.title == "task testing"
    assert task.priority == 'high'
    assert task.due_date == date(2026,1,20)
    assert task.completed == False

def test_mark_completed():
    task = Task("task testing")
    task.mark_completed()
    assert task.completed is True

def test_task_string():
    task = Task("task testing", due_date=date(2026,1,20))
    assert "task testing" in str(task)
    assert "Pending" in str(task)
    assert '✓' not in str(task)
    assert  '2026-01-20' in str(task)

    task.mark_completed()
    assert "✓" in str(task)
