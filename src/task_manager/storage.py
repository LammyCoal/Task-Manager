import json
from pathlib import Path
from .models import Task
from datetime import date
from typing import List

DATA_FILE = Path(__file__).parent.parent.parent / "data" / "tasks.json"

