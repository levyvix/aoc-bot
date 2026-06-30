from __future__ import annotations

import subprocess


def _run_git(*args: str) -> None:
    subprocess.run(["git", *args], check=True)


def push_solutions(year: int, day: int) -> int:
    _run_git("config", "user.name", "github-actions[bot]")
    _run_git("config", "user.email", "41898282+github-actions[bot]@users.noreply.github.com")

    _discard_aoc_artifacts()
    branch = subprocess.check_output(
        ["git", "rev-parse", "--abbrev-ref", "HEAD"], text=True
    ).strip()
    _run_git("pull", "--rebase", "--autostash", "origin", branch)

    _run_git("add", f"solutions/{year}/{day}/")
    staged = subprocess.run(["git", "diff", "--staged", "--quiet"])
    if staged.returncode == 0:
        print(f"No solution changes to commit for {year} day {day}")
        return 0

    _run_git("commit", "-m", f"aoc: {year} day {day} solutions")
    _run_git("pull", "--rebase", "--autostash", "origin", branch)
    _run_git("push", "origin", f"HEAD:{branch}")
    return 0


def _discard_aoc_artifacts() -> None:
    """Drop ephemeral .aoc files so git pull/push is not blocked."""
    subprocess.run(["git", "clean", "-fd", "--", ".aoc"], check=False)


def pull_rebase() -> int:
    try:
        _discard_aoc_artifacts()
        branch = subprocess.check_output(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"], text=True
        ).strip()
        _run_git("pull", "--rebase", "--autostash", "origin", branch)
        return 0
    except subprocess.CalledProcessError:
        return 1
