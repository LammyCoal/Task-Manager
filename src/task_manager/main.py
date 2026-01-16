from asyncio import tasks
from enum import Enum

import typer
from typing import Optional
from datetime import date
from .models import Task
from .storage import load_tasks, save_tasks
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="CLI Task Manager")

@app.command()
def add(title: str, priority: str= 'medium', due: Optional[str] = None):
    task = load_tasks()
    due_date = date.fromisoformat(due) if due else None
    task.append(Task(title,priority, due_date))
    save_tasks(task)
    typer.echo(f"{title} is added")

console = Console()

class Priority(str, Enum):
    LOW = 'low'
    MEDIUM = 'medium'
    HIGH = 'high'

PRIORITY_COLORS = {
    Priority.LOW: 'red',
    Priority.MEDIUM: 'yellow',
    Priority.HIGH: 'green'
}

@app.command()
def lists (sort_by: str = 'priority'):
    tasks = load_tasks()

    if not tasks:
        console.print("[italic dim] No tasks yet!, add some with : add 'Do something'[/italic dim]")
        return

    if sort_by == 'priority':
        priority_level={"high": 0, "medium": 1, "low": 2}
        tasks.sort(key=lambda t: priority_level.get(t.priority, 1))

    elif sort_by == 'due':
        tasks.sort(key=lambda t: t.due_date or date.max)

table = Table(show_header=True, header_style="bold magenta")
table.add_column('#', style="dim", width=4)
table.add_column("Task", justify="center")
table.add_column("Priority", justify="center")
table.add_column("Due", justify="right")
table.add_column("Status")

for i, task in enumerate(tasks):
    status = "[green]✓ Done[/green]" if task.completed else "[red]Pending[/red]"
@app.command()
def done(num: int):
    task = load_tasks()
    if 1 <= num <= len(task):
        task[num-1].mark_completed()
        typer.echo(f"{num} is marked as completed")
        save_tasks(task)

    else:
        typer.echo(f"{num} is not a valid number")

@app.command()
def delete(num: int):
    task = load_tasks()
    if 1 <= num <= len(task):
        task_num = task.pop(num - 1)
        save_tasks(task)
        typer.echo(f"{num}. {task_num.title} is deleted")

    else:
        typer.echo(f"{num} is not a valid task number")

@app.command()
def edit(
        index: int,
        title: Optional[str]=None,
        priority: str = None,
        due_date: Optional[str] = None,
):
    task = load_tasks()
    if not (1 <= index <= len(task)):
        typer.echo(f"{index} is not a valid task number")
        return

    real_task = task[index - 1]

    if title:
        real_task.title = title

    if priority:
        real_task.priority = priority

    if due_date:
        real_task.due_date = date.fromisoformat(due_date)

    save_tasks(task)
    typer.echo(f"{real_task.title} is edited")

if __name__ == "__main__":
    app()

