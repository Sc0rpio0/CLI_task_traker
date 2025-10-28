from .classes import TaskManager, DataclassEncoder
import typer
import json
from pathlib import Path

STORAGE_DIR = Path(__file__).parent / "storage"
STORAGE_DIR.mkdir(parents=True, exist_ok=True)
TASKS_FILE = STORAGE_DIR / "tasks.json"

app = typer.Typer()
try:
    with TASKS_FILE.open("r", encoding="UTF-8") as file:
        tracker = TaskManager(json.load(file))
except (FileNotFoundError, json.JSONDecodeError):
    tracker = TaskManager()


@app.command()
def add(description: str):
    tracker.add(description)
    save(tracker)


@app.command()
def update(task_id: int, new_description: str):
    tracker.update(task_id, new_description)
    save(tracker)


@app.command()
def delete(task_id: int):
    tracker.delete(task_id)
    save(tracker)


@app.command()
def mark(status: str, task_id: int):
    tracker.change_status(task_id, status)
    save(tracker)


@app.command()
def show(status: str = typer.Argument("")):
    tracker.show(status)


def save(tracker):
    with TASKS_FILE.open("w+", encoding="UTF-8") as file:
        json.dump(tracker, file, cls=DataclassEncoder, ensure_ascii=False)


if __name__ == "__main__":
    app()
