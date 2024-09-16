import argparse
import os
import random
from dataclasses import dataclass
from enum import StrEnum
from typing import override


class Action(StrEnum):
    LIST = "LIST"
    REVIEW = "REVIEW"
    pass


class TaskStatus(StrEnum):
    TODO = "TODO"
    DONE = "DONE"


@dataclass
class Task:
    id: int
    elo: int
    title: str
    status: TaskStatus

    @override
    def __repr__(self) -> str:
        return f"[id: {self.id}, elo:{self.elo}, title:{self.title}, status:{self.status.value}]"


@dataclass
class TaskStore:
    tasks: dict[int, Task]

    def persist(self) -> None:
        storage_dir = "storage"
        os.makedirs(storage_dir, exist_ok=True)

        for task_id, task in self.tasks.items():
            file_path = os.path.join(storage_dir, f"{task_id}.tt")
            with open(file_path, "w") as file:
                _ = file.write(f"elo:{task.elo}\n")
                _ = file.write(f"title:{task.title}\n")
                _ = file.write(f"status:{task.status.value}")


def read_tasks() -> TaskStore:
    tasks: dict[int, Task] = {}
    storage_dir = "storage"

    for filename in os.listdir(storage_dir):
        id, extension = filename.split(".")
        if extension != "tt":
            continue

        file_path = os.path.join(storage_dir, filename)
        with open(file_path, "r") as file:
            id = int(id)
            elo = int(file.readline().strip().split(":")[1])
            title = file.readline().strip().split(":")[1]
            status = TaskStatus(file.readline().strip().split(":")[1])
            tasks[id] = Task(id=id, elo=elo, title=title, status=status)

    return TaskStore(tasks=tasks)


def list_tasks() -> None:
    task_store = read_tasks()
    for task in sorted(list(task_store.tasks.values()), key=lambda x: -x.elo):
        print(task)


def review_tasks() -> None:
    task_store = read_tasks()

    if len(task_store.tasks) < 1:
        # Nothing to do!
        return

    incomplete_task_store = TaskStore(
        tasks=dict(
            filter(lambda x: x[1].status != TaskStatus.DONE, task_store.tasks.items()),
        )
    )

    for _ in range(0, 5):
        task_items = list(incomplete_task_store.tasks.items())
        id1, task1 = random.choice(task_items)
        while True:
            id2, task2 = random.choice(task_items)

            if task1 != task2:
                break

        while True:
            print(f"1: {task1}")
            print(f"2: {task2}")

            winner = input("> ")
            try:
                winner_int = int(winner)
                assert winner_int == 1 or winner_int == 2
                break
            except AssertionError:
                print("Input must be either '1' or '2'.")

        # Update the elos.
        task1, task2 = update_elo(task1, task2, winner_int)
        task_store.tasks[id1] = task1
        task_store.tasks[id2] = task2

    task_store.persist()
    return


def update_elo(task1: Task, task2: Task, winner: int) -> tuple[Task, Task]:
    k = 32  # ELO factor, can be adjusted
    expected_score1 = 1 / (1 + 10 ** ((task2.elo - task1.elo) / 400))
    expected_score2 = 1 - expected_score1

    if winner == 1:
        actual_score1, actual_score2 = 1, 0
    elif winner == 2:
        actual_score1, actual_score2 = 0, 1
    else:
        raise Exception("Something went wrong!")

    new_elo1 = task1.elo + k * (actual_score1 - expected_score1)
    new_elo2 = task2.elo + k * (actual_score2 - expected_score2)

    return (
        Task(id=task1.id, elo=int(new_elo1), title=task1.title, status=task1.status),
        Task(id=task2.id, elo=int(new_elo2), title=task2.title, status=task2.status),
    )


def create_task(title: str) -> None:
    task_store = read_tasks()
    new_id = max(task_store.tasks.keys(), default=0) + 1
    new_task = Task(id=new_id, elo=1000, title=title, status=TaskStatus.TODO)
    task_store.tasks[new_id] = new_task
    task_store.persist()
    print(f"Created new task: {new_task}")


def complete_task(task_id: int) -> None:
    task_store = read_tasks()
    if task_id in task_store.tasks:
        task = task_store.tasks[task_id]
        task.status = TaskStatus.DONE
        task_store.persist()
        print(f"Completed task: {task}")
    else:
        print(f"Task with ID {task_id} not found.")


def main_cli():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="action", required=False)

    list_parser = subparsers.add_parser("list", help="List all tasks")
    review_parser = subparsers.add_parser("review", help="Review tasks")

    add_parser = subparsers.add_parser("add", help="Add a new task")
    add_parser.add_argument("task_title", type=str, help="Title of the new task")

    complete_parser = subparsers.add_parser("complete", help="Complete a task")
    complete_parser.add_argument("id", type=int, help="ID of the task to complete")

    args = parser.parse_args()
    if args.action is None:
        list_tasks()
    else:
        match args.action:
            case "list":
                list_tasks()
            case "review":
                review_tasks()
            case "add":
                create_task(args.task_title)
            case "complete":
                complete_task(args.id)
