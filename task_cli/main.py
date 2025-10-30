import typer
from storage import save, load_task_manager
from classes import TaskNotFoundError

app = typer.Typer()


@app.command(help="Добавить задачу")
def add(description: str):
    tracker = load_task_manager()
    tracker.add(description)
    save(tracker)
    typer.secho("Задача добавлена", fg=typer.colors.GREEN)


@app.command(help="Обновить задачу")
def update(task_id: str, new_description: str):
    tracker = load_task_manager()
    safe_action(
        lambda: tracker.update(task_id, new_description), f"Задача {task_id} обновлена"
    )
    save(tracker)


@app.command(help="Удалить задачу")
def delete(task_id: str):
    tracker = load_task_manager()
    safe_action(lambda: tracker.delete(task_id), f"Задача {task_id} удалена")
    save(tracker)


@app.command(help="Поменять статус задачи")
def mark(task_id: str, status: str):
    tracker = load_task_manager()
    safe_action(
        lambda: tracker.change_status(task_id, status),
        f"Статус задачи {task_id} изменён",
    )
    save(tracker)


@app.command(help="Вывести задачи")
def show(status: str = typer.Option(None, help="Фильтр по статусу")):
    tracker = load_task_manager()
    for t in tracker.get_list(status or ""):
        typer.secho(t)


def safe_action(action, message: str):
    try:
        action()
        typer.secho(message, fg=typer.colors.GREEN)
    except TaskNotFoundError as error:
        typer.secho(error, fg=typer.colors.RED)
        raise typer.Exit()
    except Exception as error:
        typer.secho(f"Непредвиденная ошибка {error}", fg=typer.colors.RED)
        raise typer.Exit()


if __name__ == "__main__":
    app()
