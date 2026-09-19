#!/usr/bin/env python3
"""
main.py — Kayra Assistant entry point
======================================
Run:
    python main.py            # full briefing (print + speak)
    python main.py --text     # print only, no TTS
    python main.py --add-task # interactive task-add prompt
    python main.py --done <id># mark a task as done
    python main.py --help     # show help
"""

import argparse
import sys
import textwrap

from assistant import build_briefing, fetch_weather, print_briefing, speak
from data_manager import add_task, mark_task_done


# ── Argument parsing ──────────────────────────────────────────────────────────

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="kayra",
        description="Kayra — your personal desktop assistant.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent(
            """\
            Examples:
              python main.py                   Run full morning briefing
              python main.py --text            Print briefing, skip TTS
              python main.py --add-task        Add a new task interactively
              python main.py --done 2          Mark task #2 as done
            """
        ),
    )
    parser.add_argument(
        "--text", action="store_true",
        help="Print the briefing to the terminal without speaking it."
    )
    parser.add_argument(
        "--add-task", action="store_true", dest="add_task",
        help="Interactively add a new task."
    )
    parser.add_argument(
        "--done", metavar="ID", type=int,
        help="Mark the task with the given ID as done."
    )
    parser.add_argument(
        "--lat", type=float, default=None,
        help="Override latitude for weather (decimal degrees)."
    )
    parser.add_argument(
        "--lon", type=float, default=None,
        help="Override longitude for weather (decimal degrees)."
    )
    return parser.parse_args()


# ── Sub-commands ──────────────────────────────────────────────────────────────

def cmd_add_task() -> None:
    """Prompt the user to enter a new task interactively."""
    print("\n── Add New Task ──────────────────────────────")
    title = input("  Task title    : ").strip()
    subject = input("  Subject/Course: ").strip()
    deadline = input("  Deadline (YYYY-MM-DD): ").strip()
    priority = input("  Priority [high/medium/low] (default: medium): ").strip().lower()
    if priority not in ("high", "medium", "low"):
        priority = "medium"

    task = add_task(title=title, subject=subject,
                    deadline=deadline, priority=priority)
    print(f"\n  ✓ Task #{task['id']} saved: \"{task['title']}\" due {task['deadline']}.\n")


def cmd_mark_done(task_id: int) -> None:
    """Mark a task as done by ID."""
    if mark_task_done(task_id):
        print(f"  ✓ Task #{task_id} marked as done.\n")
    else:
        print(f"  ✗ No task with ID {task_id} found.\n", file=sys.stderr)
        sys.exit(1)


def cmd_briefing(text_only: bool, lat=None, lon=None) -> None:
    """Fetch weather, build briefing, print it, and optionally speak it."""
    print("\n[Kayra] Fetching weather data…")

    weather_kwargs: dict = {}
    if lat is not None:
        weather_kwargs["lat"] = lat
    if lon is not None:
        weather_kwargs["lon"] = lon

    weather = fetch_weather(**weather_kwargs)
    briefing = build_briefing(weather=weather)

    print_briefing(briefing)

    if not text_only:
        print("[Kayra] Speaking briefing… (use --text to skip TTS)\n")
        speak(briefing)


# ── Entry point ───────────────────────────────────────────────────────────────


def main() -> None:
    args = parse_args()

    if args.add_task:
        cmd_add_task()
    elif args.done is not None:
        cmd_mark_done(args.done)
    else:
        cmd_briefing(text_only=args.text, lat=args.lat, lon=args.lon)


if __name__ == "__main__":
    main()
