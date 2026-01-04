from datetime import date
from typing import Optional

class Task:
    def __init__(self, title: str, priority:  str = 'medium', due_date: Optional[date] = None):
        self.title = title
        self.priority = priority.lower()
        self.due_date = due_date
        self.completed = False

    def mark_completed(self):
        self.completed = True

    def __str__(self):
        status = '✓' if self.completed else ' '
        due = f" Due: {self.due_date}" if self.due_date else ' '
        return f" {status} {self.title} - Priority: {self.priority}{due}"