import dataclasses
from datetime import datetime
from json import JSONEncoder


@dataclasses.dataclass()
class Task:
    description: str
    task_id: str
    status: str = dataclasses.field(default="todo")
    created_at: str = dataclasses.field(
        default_factory=lambda: (str(datetime.now().replace(microsecond=0)))
    )
    updated_at: str = dataclasses.field(default="")

    def change_status(self, status):
        self.status = status
        self._touch()

    def update_description(self, new_description):
        self.description = new_description
        self._touch()

    def _touch(self):
        self.updated_at = str(datetime.now().replace(microsecond=0))

    def __post_init__(self):
        if not self.updated_at:
            self.updated_at = self.created_at

    def __json__(self):
        return dataclasses.asdict(self)


class Singleton:
    _instance = None
    _initialazed = False

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        if self._initialazed:
            return
        self._initialazed = True


@dataclasses.dataclass
class TaskManager(Singleton):
    tasks: dict = dataclasses.field(default_factory=dict)

    def __post_init__(self):
        for x in self.tasks:
            if isinstance(self.tasks[x], dict):
                self.tasks[x] = Task(**self.tasks[x])

    def __json__(self):
        return self.tasks

    def add(self, description):
        task = Task(description, task_id=self._get_id())
        self.tasks[task.task_id] = task

    def update(self, task_id, new_description):
        self._get_task(task_id).update_description(new_description)

    def delete(self, task_id):
        self.tasks.pop(self._get_task(task_id).task_id)

    def change_status(self, task_id, status):
        self._get_task(task_id).change_status(status)

    def _get_task(self, task_id: str):
        try:
            return self.tasks[task_id]
        except KeyError:
            raise TaskNotFoundError(f"Задачи {task_id} не существует")

    def get_list(self, status):
        tasks = dict(sorted(self.tasks.items()))
        return [
            f"Задача {x}: {tasks[x].description}, статус: {tasks[x].status}, создана {tasks[x].created_at}, последнее обновление {tasks[x].updated_at}"
            for x in tasks
            if not status or tasks[x].status == status
        ]

    def _get_id(self):
        task_id = 1
        while str(task_id) in self.tasks:
            task_id += 1
        return str(task_id)


class DataclassEncoder(JSONEncoder):
    def default(self, o: TaskManager):
        if hasattr(o, "__json__"):
            return o.__json__()
        return super().default(o)


class TaskNotFoundError(Exception):
    pass
