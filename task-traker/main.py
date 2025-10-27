import dataclasses
import datetime
import typer
import json
import time


@dataclasses.dataclass()
class Task:
    description: str
    task_id: int = dataclasses.field(default=0)
    status: str = dataclasses.field(default="todo")
    created_at: str = dataclasses.field(
        default_factory=lambda: (str(datetime.datetime.now().replace(microsecond=0)))
    )
    updated_at: str = dataclasses.field(init=False)

    def __post_init__(self):
        self.updated_at = self.created_at


@dataclasses.dataclass
class Tracker:
    tasks_list: dict[int, Task]

    def add(self, task: Task):
        while True:
            if task.task_id in self.tasks_list:
                task.task_id += 1
            break
        self.tasks_list[task.task_id] = task


app = typer.Typer()


# @app.command()
def add(description):
    print("something")


# @app.command()
def update():
    print("something")


# @app.command()
def delete():
    print("something")


def main():
    with open(r"JSON-FOLDER\tasks.json", "r") as file:
        try:
            data = json.load(file)
        except json.decoder.JSONDecodeError:
            data = {}
    tracker = Tracker(data)
    x = Task("sdfkslkdf")
    print(x)
    # with open(r"JSON-FOLDER\new_tasks.json", "w") as file:
    #     json.dump(data, file)


if __name__ == "__main__":
    main()
