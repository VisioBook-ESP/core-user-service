import subprocess


def run(cmd: list[str]) -> None:
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print(res.stdout)
        print(res.stderr)
    assert res.returncode == 0, f"Command {' '.join(cmd)} failed"


def test_black():
    run(["black", "--check", "app", ".tests"])


def test_isort():
    run(["isort", "--check-only", "app", ".tests"])


def test_pylint():
    run(["pylint", "app"])


def test_mypy():
    run(["mypy", "app"])
