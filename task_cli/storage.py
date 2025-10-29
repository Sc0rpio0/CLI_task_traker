from pathlib import Path
from json import load, dump, JSONDecodeError
from classes import TaskManager, DataclassEncoder

STORAGE_DIR = Path(__file__).parent / "storage"
STORAGE_DIR.mkdir(parents=True, exist_ok=True)
TASKS_FILE = STORAGE_DIR / "tasks.json"


def load_task_manager():
    try:
        with TASKS_FILE.open("r", encoding="UTF-8") as file:
            return TaskManager(load(file))
    except (FileNotFoundError, JSONDecodeError):
        return TaskManager()


def save(tracker):
    with TASKS_FILE.open("w", encoding="UTF-8") as file:
        dump(tracker, file, cls=DataclassEncoder, ensure_ascii=False)
