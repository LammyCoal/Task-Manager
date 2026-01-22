import json
from pathlib import Path
from .models import Task
from datetime import date
from typing import List

DATA_FILE = Path(__file__).parent.parent.parent / "data" / "tasks.json"

def load_tasks(path: Path = DATA_FILE) -> List[Task]:
    if not path.exists():
        return []

    with open(path, "r", encoding="utf8") as f:
        json_data = json.load(f)

    tasks = []
    for elements in json_data:
        due = date.fromisoformat(elements["due_date"]) if elements["due_date"] else None
        task = Task(elements["title"], elements["priority"], due)
        if elements.get('completed'):
            task.mark_completed()
        tasks.append(task)
    return tasks


def save_tasks(tasks: List[Task], path: Path = DATA_FILE):
    path.parent.mkdir(exist_ok=True)

    data = []
    for items in tasks:
        data.append({
        'title': items.title,
        'priority': items.priority,
        "due_date": items.due_date.isoformat() if items.due_date else None,
        "completed": items.completed,
    }
    )
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)