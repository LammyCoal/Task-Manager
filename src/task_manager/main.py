from enum import Enum
import typer
from typing import Optional
from datetime import date
from .models import Task
from .storage import load_tasks, save_tasks
from rich.console import Console
from rich.table import Table

class Priority(str, Enum):
    LOW = 'low'
    MEDIUM = 'medium'
    HIGH = 'high'

PRIORITY_COLORS = {
    Priority.LOW: 'red',
    Priority.MEDIUM: 'yellow',
    Priority.HIGH: 'green'
}

app = typer.Typer(help="CLI Task Manager")
console = Console()

@app.command()
def add(title: str, priority: Priority= Priority.MEDIUM , due: Optional[str] = None):
    """Adds a new task."""
    try:
        due_date = date.fromisoformat(due) if due else None
    except ValueError:
        console.print("[red]Invalid date format[/red] Use YYYY-MM-DD")
        return

    task = load_tasks()
    new_task = (Task(title,priority.value, due_date))
    task.append(new_task)
    save_tasks(task)

    console.print(f"[green]Task:[/green] {new_task.title}")
    console.print(f"[green]Priority:[/green] {priority.value} and [green]Due:[/green] {due_date}")


@app.command()
def lists (
        pending: bool = typer.Option(False, "--pending", "-p", help="show only task that are pending"),
        done: bool = typer.Option(False, "--done",help="show only task that are done"),
        high: bool = typer.Option(False, "--high",help="show only task that are has high priority"),
        today: bool = typer.Option(False, "--today", help="show tasks due today"),
        overdue: bool = typer.Option(False, "--overdue",help="shows overdue tasks"),
        sort_by: str = typer.Option("priority", "--sort",help="sort by: priority, due")
):
    """list of tasks with good formatting(accepts priority or due as inputs)"""
    tasks = load_tasks()

    if pending:
        tasks = [t for t in tasks if not t.completed]
    if done:
        tasks = [t for t in tasks if t.completed]
    if high:
        tasks = [t for t in tasks if t.priority == "high"]
    if today:
        tasks = [t for t in tasks if t.due_date == date.today()]
    if overdue:
        tasks = [t for t in tasks if t.due_date and t.due_date < date.today() and not t.completed]

    if sort_by == 'priority':
        priority_level={"high": 0, "medium": 1, "low": 2}
        tasks.sort(key=lambda t: priority_level.get(t.priority, 1))

    elif sort_by == 'due':
        tasks.sort(key=lambda t: t.due_date or date.max)

    if not tasks:
        console.print("[italic dim] No tasks yet!, add some with : add 'Do something'[/italic dim]")
        return

    table = Table(show_header=True, header_style="bold magenta")
    table.add_column('#', style="dim", width=4)
    table.add_column("Task", justify="center")
    table.add_column("Priority", justify="center")
    table.add_column("Due", justify="right")
    table.add_column("Status")

    for i, task in enumerate(tasks, 1):
        status = "[green]✓ Done[/green]" if task.completed else "[red]Pending[/red]"
        due = task.due_date.strftime("%Y-%m-%d") if task.due_date else "-"
        priority_color = f"[{PRIORITY_COLORS.get(task.priority, 'white')}] {task.priority.upper()}[/{PRIORITY_COLORS.get(task.priority, 'white')}]"

        table.add_row(
                str(i),
                task.title,
                priority_color,
                due,
                status,
            )
    console.print(table)

@app.command()
def done_task(num: int):
    """Mark tasks as completed by number"""
    task = load_tasks()
    if not 1 <= num <= len(task):
        console.print(f"[red]Error[/red] Task {num} does not exist")
        return

    task[num-1].mark_completed()
    save_tasks(task)
    console.print(f"[green] ✓ [/green] Task {num} is done")

@app.command()
def delete(num: int):
    """ Deletes Task by its index"""
    task = load_tasks()
    if not 1 <= num <= len(task):
        console.print(f"[red]Error[/red] Task {num} does not exist")
        return

    task_num = task.pop(num - 1)
    save_tasks(task)
    console.print(f"[red]Deleted:[/red] Task{task_num} from database ")

@app.command()
def edit(
        index: int,
        title: Optional[str]=None,
        priority: str = None,
        due: Optional[str] = None,
):
    """Edits Task by its index"""
    task = load_tasks()
    if not (1 <= index <= len(task)):
        console.print(f"[red] {index} is not a valid task number [/red]")
        return

    real_task = task[index - 1]

    if title:
        real_task.title = title

    if priority:
        real_task.priority = priority

    if due:
        real_task.due_date = date.fromisoformat(due)

    save_tasks(task)
    console.print(f"[bold green]{real_task.title} is edited[/bold green]  ")

if __name__ == "__main__":
    app()

