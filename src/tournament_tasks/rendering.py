from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from . import Task

MAX_COL_LENGTH = 100


@dataclass
class ColumnWidths:
    id: int
    elo: int
    title: int
    status: int


def clamp_string(s: str) -> str:
    if len(s) >= MAX_COL_LENGTH:
        s = s[MAX_COL_LENGTH - 3] + "..."

    return s


def calculate_column_lengths(tasks: list["Task"]) -> ColumnWidths:
    max_widths = ColumnWidths(
        id=len("id"), elo=len("elo"), title=len("title"), status=len("status")
    )

    for task in tasks:
        if (id_len := len(str(task.id))) > max_widths.id:
            max_widths.id = id_len if id_len <= MAX_COL_LENGTH else MAX_COL_LENGTH

        if (elo_len := len(str(task.elo))) > max_widths.elo:
            max_widths.elo = elo_len if elo_len <= MAX_COL_LENGTH else MAX_COL_LENGTH

        if (title_len := len(str(task.title))) > max_widths.title:
            max_widths.title = (
                title_len if title_len <= MAX_COL_LENGTH else MAX_COL_LENGTH
            )

        if (status_len := len(str(task.status))) > max_widths.status:
            max_widths.status = (
                status_len if status_len <= MAX_COL_LENGTH else MAX_COL_LENGTH
            )

    return max_widths


def render_tasks(tasks: list["Task"]) -> str:
    max_widths = calculate_column_lengths(tasks)

    strs: list[str] = []

    headers = "| {} | {} | {} | {} |".format(
        "id".ljust(max_widths.id),
        "elo".ljust(max_widths.elo),
        "title".ljust(max_widths.title),
        "status".ljust(max_widths.status),
    )
    strs.append(headers)
    strs.append("-" * len(headers))

    for task in tasks:
        strs.append(render_task(task, max_widths))

    return "\n".join(strs)


def render_task(task: "Task", max_widths: ColumnWidths) -> str:
    return "| {} | {} | {} | {} |".format(
        clamp_string(str(task.id)).ljust(max_widths.id),
        clamp_string(str(task.elo)).ljust(max_widths.elo),
        clamp_string(str(task.title)).ljust(max_widths.title),
        clamp_string(str(task.status)).ljust(max_widths.status),
    )
