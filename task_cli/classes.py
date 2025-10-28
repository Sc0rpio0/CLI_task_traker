import dataclasses
import datetime
from json import JSONEncoder


@dataclasses.dataclass()
class Task:
    description: str
    task_id: int = dataclasses.field(default=1)
    status: str = dataclasses.field(default="todo")
    created_at: str = dataclasses.field(
        default_factory=lambda: (str(datetime.datetime.now().replace(microsecond=0)))
    )
    updated_at: str = dataclasses.field(default="")

    def change_status(self, status):
        self.status = status
        self._update_time()

    def update_description(self, new_description):
        self.description = new_description
        self._update_time()

    def _update_time(self):
        self.updated_at = str(datetime.datetime.now().replace(microsecond=0))

    def __post_init__(self):
        if not self.updated_at:
            self.updated_at = self.created_at

    def __json__(self):
        return dataclasses.asdict(self)


class Singleton:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance


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
        task = Task(description)
        while True:
            if str(task.task_id) in self.tasks:
                task.task_id += 1
            else:
                break
        self.tasks[task.task_id] = task

    def update(self, task_id, new_description):
        if task_id not in self.tasks:
            pass
        self.tasks[task_id].update_description(new_description)

    def delete(self, task_id):
        if task_id not in self.tasks:
            pass
        else:
            del self.tasks[task_id]

    def show(self, status):
        tasks = dict(sorted(self.tasks.items()))
        for x in tasks:
            if status and tasks[x].status != status:
                continue
            print(
                f"Задача {x}: {tasks[x].description}, статус: {tasks[x].status}, создана {tasks[x].created_at}, последнее обновление {tasks[x].updated_at}"
            )

    def change_status(self, task_id, status):
        if task_id not in self.tasks:
            pass
        self.tasks[task_id].change_status(status)


class DataclassEncoder(JSONEncoder):
    def default(self, o):
        if hasattr(o, "__json__"):
            return o.__json__()
        return super().default(o)
