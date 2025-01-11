# **T**ournament **T**asks

I never know how to prioritise different tasks, I only know which tasks are more important than others. We should make them compete. The idea here is that if you put the tasks through some kind of elo scoring system you will get an accurate representation of the highest priority tasks. If the tasks are reviewed often enough then their ratings should represent their priority accruately.

## Usage

`tt review` will iterate through a subset of all stored tasks and ask you to compare which is more important.

`tt` & `tt list` will list the `10` highest rated tasks in your backlog.

`tt add <string>` will create a new task with a title `<string>`

`tt complete <id>` will mark the corresponding task with `id=<id>` as `DONE`.
