from storage import save, load_task_manager
import typer

app = typer.Typer()


@app.command(help="Добавить задачу")
def add(description: str):
    tracker = load_task_manager()
    tracker.add(description)
    save(tracker)
    typer.echo("Задача добавлена")


@app.command(help="Обновить задачу")
def update(tracker, task_id: str, new_description: str):
    tracker = load_task_manager()
    tracker.update(task_id, new_description)
    save(tracker)
    typer.echo(f"Задача {task_id} обновлена")


@app.command(help="Удалить задачу")
def delete(task_id: str):
    tracker = load_task_manager()
    tracker.delete(task_id)
    save(tracker)
    typer.echo(f"Задача {task_id} удалена")


@app.command(help="Поменять статус задачи")
def mark(tracker, status: str, task_id: str):
    tracker.change_status(task_id, status)
    typer.echo(f"Статус задачи {task_id} изменён")


@app.command(help="Вывести задачи")
def show(status: str = typer.Argument("")):
    tracker = load_task_manager()
    tracker.show(status)


if __name__ == "__main__":
    app()
