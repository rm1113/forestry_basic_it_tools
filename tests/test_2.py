from pathlib import Path
import subprocess
import os

ROOT = Path(__file__).resolve().parents[1]
INITIAL_COMMIT_NUMBER = 3

def _git(*args: str) -> str:
    completed = subprocess.run(
        ["git", *args],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=True,
    )
    return completed.stdout.strip()


def test_commits_added():
    log_subjects = _git("log", "--oneline").splitlines()
    assert len(log_subjects) > INITIAL_COMMIT_NUMBER, "Новые коммиты не найдены!"


def test_revert_commit():
    log_subjects = _git("log", "--oneline").splitlines()
    log_subjects = list(reversed(log_subjects))
    assert len(log_subjects) >= INITIAL_COMMIT_NUMBER + 3, "Недостаточно коммитов для тестирования Revert!"
    last_commit = log_subjects[-1]
    previous_commit = log_subjects[-3]
    assert "Revert" in last_commit, "Последний коммит не является revert-коммитом!"

    last_hash = last_commit.split()[0]
    previous_hash = previous_commit.split()[0]
    diff = _git("diff", f"{last_hash}..{previous_hash}")
    assert len(diff) == 0, "Результат diff между последним и предыдущим коммитом не пустой!"
