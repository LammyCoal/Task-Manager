import json
from pathlib import Path
from .models import Task
from datetime import date
from typing import List

DATA_FILE = Path(__file__).parent.parent.parent / "data" / "tasks.json"

def load_tasks() -> List[Task]:
    if not DATA_FILE.exists():
        return []
    with open(DATA_FILE, 'r') as file:
        json_data = json.load(file)

    tasks = []
    for task in json_data:
        due = 