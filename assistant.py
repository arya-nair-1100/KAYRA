"""
assistant.py
------------
Core intelligence of Kayra: weather fetching, briefing
composition, and text-to-speech delivery.
"""

import sys
import textwrap
from datetime import datetime
from typing import Optional

import requests
import pyttsx3

from data_manager import get_todays_classes, get_upcoming_tasks

# ── Open-Meteo configuration ──────────────────────────────────────────────────
# Default coordinates (Bengaluru, India). Override via environment variables
# KAYRA_LAT and KAYRA_LON, or pass them directly to fetch_weather().
import os
DEFAULT_LAT = float(os.getenv("KAYRA_LAT", "12.9716"))
DEFAULT_LON = float(os.getenv("KAYRA_LON", "77.5946"))
WEATHER_URL = "https://api.open-meteo.com/v1/forecast"

# WMO weather interpretation codes → human-readable description
_WMO_CODES: dict[int, str] = {
    0: "clear sky",
    1: "mainly clear", 2: "partly cloudy", 3: "overcast",
    45: "foggy", 48: "icy fog",
    51: "light drizzle", 53: "moderate drizzle", 55: "dense drizzle",
    61: "slight rain", 63: "moderate rain", 65: "heavy rain",
    71: "slight snow", 73: "moderate snow", 75: "heavy snow",
    80: "slight rain showers", 81: "moderate rain showers", 82: "violent rain showers",
    95: "thunderstorm", 96: "thunderstorm with slight hail", 99: "thunderstorm with heavy hail",
}


# ── Weather ───────────────────────────────────────────────────────────────────

def fetch_weather(lat: float = DEFAULT_LAT, lon: float = DEFAULT_LON) -> Optional[dict]:
    """
    Fetch current weather from the Open-Meteo API (no API key required).

    Returns a dict with keys:
        temperature_c  : float  – current temperature in °C
        apparent_temp  : float  – feels-like temperature in °C
        humidity       : int    – relative humidity in %
        condition      : str    – human-readable weather description
        wind_speed     : float  – wind speed in km/h

    Returns ``None`` on any network or parsing error.
    """
    params = {
        "latitude": lat,
        "longitude": lon,
        "current": [
            "temperature_2m",
            "apparent_temperature",
            "relative_humidity_2m",
            "weather_code",
            "wind_speed_10m",
        ],
        "timezone": "auto",
    }
    try:
        resp = requests.get(WEATHER_URL, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        current = data["current"]
        code = int(current.get("weather_code", 0))
        return {
            "temperature_c": current["temperature_2m"],
            "apparent_temp": current["apparent_temperature"],
            "humidity": current["relative_humidity_2m"],
            "condition": _WMO_CODES.get(code, "unknown conditions"),
            "wind_speed": current["wind_speed_10m"],
        }
    except Exception as exc:
        print(f"[Kayra] Weather fetch failed: {exc}", file=sys.stderr)
        return None


# ── Briefing composition ──────────────────────────────────────────────────────

def _greeting() -> str:
    """Return a time-appropriate greeting."""
    hour = datetime.now().hour
    if hour < 12:
        return "Good morning"
    elif hour < 17:
        return "Good afternoon"
    else:
        return "Good evening"


def build_briefing(weather: Optional[dict] = None) -> str:
    """
    Compose the full startup briefing as a plain-text string.

    Sections:
    1. Greeting + date & time
    2. Weather summary
    3. Today's class schedule
    4. Upcoming task deadlines (next 7 days)
    """
    now = datetime.now()
    lines: list[str] = []

    # ── 1. Greeting ────────────────────────────────────────────────────────
    greeting = _greeting()
    date_str = now.strftime("%A, %B %d, %Y")
    time_str = now.strftime("%I:%M %p")
    lines.append(f"{greeting}! Today is {date_str}, and the time is {time_str}.")
    lines.append("")

    # ── 2. Weather ────────────────────────────────────────────────────────
    if weather:
        lines.append(
            f"Current weather: {weather['condition'].capitalize()}, "
            f"{weather['temperature_c']:.1f}°C "
            f"(feels like {weather['apparent_temp']:.1f}°C). "
            f"Humidity is {weather['humidity']}% "
            f"and wind speed is {weather['wind_speed']:.1f} km/h."
        )
    else:
        lines.append("Weather information is currently unavailable.")
    lines.append("")

    # ── 3. Timetable ──────────────────────────────────────────────────────
    classes = get_todays_classes()
    if classes:
        lines.append(f"You have {len(classes)} class(es) today:")
        for cls in classes:
            lines.append(f"  • {cls['time']} — {cls['subject']} in room {cls['room']}")
    else:
        lines.append("You have no classes scheduled today. Enjoy your free day!")
    lines.append("")

    # ── 4. Tasks ──────────────────────────────────────────────────────────
    upcoming = get_upcoming_tasks(days_ahead=7)
    if upcoming:
        lines.append(f"You have {len(upcoming)} upcoming deadline(s) in the next 7 days:")
        for task in upcoming:
            days_left = task["days_left"]
            if days_left == 0:
                due_label = "due TODAY"
            elif days_left == 1:
                due_label = "due tomorrow"
            else:
                due_label = f"due in {days_left} days"
            priority_tag = f"[{task.get('priority', 'medium').upper()}]"
            lines.append(
                f"  • {priority_tag} {task['title']} ({task['subject']}) — {due_label}"
            )
    else:
        lines.append("No tasks due in the next 7 days. Great job staying on top of things!")
    lines.append("")
    lines.append("That's your briefing for today. Have a productive day!")

    return "\n".join(lines)


# ── Text-to-speech ────────────────────────────────────────────────────────────

def speak(text: str, rate: int = 165, volume: float = 1.0) -> None:
    """
    Read ``text`` aloud using pyttsx3 (fully offline).

    Parameters
    ----------
    text   : The string to speak.
    rate   : Words per minute (default 165).
    volume : Volume level 0.0–1.0 (default 1.0).
    """
    try:
        engine = pyttsx3.init()
        engine.setProperty("rate", rate)
        engine.setProperty("volume", volume)

        # Prefer a female voice when available
        voices = engine.getProperty("voices")
        for voice in voices:
            if "female" in voice.name.lower() or "zira" in voice.id.lower():
                engine.setProperty("voice", voice.id)
                break

        engine.say(text)
        engine.runAndWait()
    except Exception as exc:
        print(f"[Kayra] TTS error: {exc}", file=sys.stderr)
        print("[Kayra] Printing briefing to console instead.\n")
        print(text)


# ── Pretty-print helper ───────────────────────────────────────────────────────

def print_briefing(briefing: str) -> None:
    """Print the briefing with a decorative border."""
    width = 70
    border = "─" * width
    print(f"\n┌{border}┐")
    print(f"│{'  KAYRA ASSISTANT — DAILY BRIEFING':^{width}}│")
    print(f"└{border}┘\n")
    for line in briefing.splitlines():
        if line:
            # Wrap long lines neatly
            for wrapped in textwrap.wrap(line, width=width) or [line]:
                print(f"  {wrapped}")
        else:
            print()
    print(f"{'─' * (width + 2)}\n")
