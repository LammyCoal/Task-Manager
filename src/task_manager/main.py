from asyncio import tasks

import typer
from typing import Optional
from datetime import date
from .models import Task
from .storage import load_tasks, save_tasks

app = typer.Typer(help="CLI Task Manager")

@app.command()
def add(title: str, priority: str= 'medium', due: Optional[str] = None):
    task = load_tasks()
    due_date = date.fromisoformat(due) if due else None
    task.append(Task(title,priority, due_date))
    save_tasks(task)
    typer.echo(f"{title} is added")


@app.command()
def list():
    load = load_tasks()
    if not load:
        typer.echo("No tasks yet")
        return
    for i, task in enumerate(load, 1):
        typer.echo(f"{i}. {task.title}")

@app.command()
def done(num: int):
    task = load_tasks()
    if 1 <= num <= len(task):
        task[num-1].mark_completed()
        typer.echo(f"{num} is marked as completed")

    else:
        typer.echo(f"{num} is not a valid number")

if __name__ == "__main__":
    app()

