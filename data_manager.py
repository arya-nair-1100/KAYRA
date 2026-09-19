"""
data_manager.py
---------------
Handles loading and saving tasks and timetable data
from JSON files stored in the /data directory.

All paths are relative to this file so the project
works on Windows, macOS, and Linux without changes.
"""

import json
import os
from datetime import datetime, date
from typing import List, Dict, Any

# ── Path helpers ─────────────────────────────────────────────────────────────
_BASE_DIR = os.path.dirname(os.path.abspath(__file__))
_DATA_DIR = os.path.join(_BASE_DIR, "data")
TASKS_FILE = os.path.join(_DATA_DIR, "tasks.json")
TIMETABLE_FILE = os.path.join(_DATA_DIR, "timetable.json")


def _ensure_data_dir() -> None:
    """Create the data directory if it doesn't already exist."""
    os.makedirs(_DATA_DIR, exist_ok=True)


# ── Tasks ────────────────────────────────────────────────────────────────────

def load_tasks() -> List[Dict[str, Any]]:
    """Load all tasks from tasks.json. Returns an empty list if the file is missing."""
    _ensure_data_dir()
    if not os.path.exists(TASKS_FILE):
        return []
    with open(TASKS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_tasks(tasks: List[Dict[str, Any]]) -> None:
    """Persist the tasks list back to tasks.json."""
    _ensure_data_dir()
    with open(TASKS_FILE, "w", encoding="utf-8") as f:
        json.dump(tasks, f, indent=2, ensure_ascii=False)


def get_upcoming_tasks(days_ahead: int = 7) -> List[Dict[str, Any]]:
    """
    Return tasks that are:
    - not yet done
    - due within the next ``days_ahead`` days (inclusive of today)

    Results are sorted by deadline (soonest first), then priority.
    """
    priority_order = {"high": 0, "medium": 1, "low": 2}
    today = date.today()
    upcoming = []

    for task in load_tasks():
        if task.get("done"):
            continue
        try:
            deadline = datetime.strptime(task["deadline"], "%Y-%m-%d").date()
        except (KeyError, ValueError):
            continue
        delta = (deadline - today).days
        if 0 <= delta <= days_ahead:
            task = dict(task)           # shallow copy – don't mutate original
            task["days_left"] = delta
            upcoming.append(task)

    upcoming.sort(
        key=lambda t: (
            t["days_left"],
            priority_order.get(t.get("priority", "low"), 2),
        )
    )
    return upcoming


def add_task(title: str, subject: str, deadline: str,
             priority: str = "medium") -> Dict[str, Any]:
    """
    Add a new task and persist it.

    Parameters
    ----------
    title    : Short description of the task.
    subject  : Related subject / course.
    deadline : ISO 8601 date string, e.g. ``"2026-10-01"``.
    priority : ``"high"``, ``"medium"``, or ``"low"``.

    Returns the newly created task dict.
    """
    tasks = load_tasks()
    new_id = max((t.get("id", 0) for t in tasks), default=0) + 1
    task: Dict[str, Any] = {
        "id": new_id,
        "title": title,
        "subject": subject,
        "deadline": deadline,
        "priority": priority,
        "done": False,
    }
    tasks.append(task)
    save_tasks(tasks)
    return task


def mark_task_done(task_id: int) -> bool:
    """
    Mark a task as done by its ``id``.

    Returns ``True`` if the task was found and updated, ``False`` otherwise.
    """
    tasks = load_tasks()
    for task in tasks:
        if task.get("id") == task_id:
            task["done"] = True
            save_tasks(tasks)
            return True
    return False


# ── Timetable ────────────────────────────────────────────────────────────────

def load_timetable() -> Dict[str, List[Dict[str, str]]]:
    """Load the weekly timetable from timetable.json."""
    _ensure_data_dir()
    if not os.path.exists(TIMETABLE_FILE):
        return {}
    with open(TIMETABLE_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def get_todays_classes() -> List[Dict[str, str]]:
    """
    Return the list of classes scheduled for today, sorted by time.

    Each item is a dict with keys: ``time``, ``subject``, ``room``.
    """
    timetable = load_timetable()
    day_name = datetime.now().strftime("%A")   # e.g. "Monday"
    classes = timetable.get(day_name, [])
    return sorted(classes, key=lambda c: c.get("time", ""))


def get_remaining_classes() -> List[Dict[str, str]]:
    """
    Return today's classes that haven't started yet (start time > now).
    """
    now_str = datetime.now().strftime("%H:%M")
    return [c for c in get_todays_classes() if c.get("time", "") > now_str]
