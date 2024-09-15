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


@dataclass
class Task:
    elo: int
    title: str

    @override
    def __repr__(self) -> str:
        return f"[elo:{self.elo}, title:{self.title}]"


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
            tasks[id] = Task(elo=elo, title=title)

    return TaskStore(tasks=tasks)


def list_tasks() -> None:
    task_store = read_tasks()
    for task in task_store.tasks.values():
        print(task)


def review_tasks() -> None:
    task_store = read_tasks()

    if len(task_store.tasks) < 1:
        # Nothing to do!
        return

    for _ in range(0, 5):
        task_items = list(task_store.tasks.items())
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
        Task(elo=int(new_elo1), title=task1.title),
        Task(elo=int(new_elo2), title=task2.title),
    )


def main_cli():
    parser = argparse.ArgumentParser()
    _ = parser.add_argument(
        "action", type=str, choices=[str(val).lower() for val in Action], nargs="?"
    )

    args = parser.parse_args()
    if args.action is None:
        list_tasks()
    elif args.action is not None:
        action = Action(args.action.upper())
        match action:
            case Action.LIST:
                list_tasks()
            case Action.REVIEW:
                review_tasks()
