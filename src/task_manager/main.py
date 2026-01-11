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
def lists():
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
        due: Optional[str] = None,
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

    if due:
        real_task.due = date.fromisoformat(due)

    save_tasks(task)
    typer.echo(f"{real_task.title} is edited")

if __name__ == "__main__":
    app()

