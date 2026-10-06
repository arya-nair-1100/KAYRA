import webview
import json
import os
from data_manager import (
    load_tasks, add_task, mark_task_done, load_timetable,
    load_notes, save_notes, get_closest_exam
)
from assistant import fetch_weather, build_briefing, speak

class Api:
    def get_data(self):
        """Fetch tasks, timetable, weather, notes, and exam countdown for the dashboard."""
        return {
            "tasks": load_tasks(),
            "timetable": load_timetable(),
            "weather": fetch_weather(),
            "notes": load_notes(),
            "exam": get_closest_exam()
        }

    def add_new_task(self, title, subject, deadline, priority):
        add_task(title, subject, deadline, priority)
        return {"status": "success"}

    def complete_task(self, task_id):
        mark_task_done(int(task_id))
        return {"status": "success"}

    def save_scratchpad(self, content):
        """Auto-save quick notes from the frontend UI drawer."""
        save_notes(content)
        return {"status": "saved"}

    def trigger_briefing(self):
        weather = fetch_weather()
        briefing = build_briefing(weather)
        speak(briefing)
        return {"status": "spoken"}

if __name__ == '__main__':
    api = Api()
    window = webview.create_window(
        'Kayra — Personal Assistant', 
        'index.html', 
        js_api=api, 
        width=1100, 
        height=750,
        min_size=(900, 650)
    )
    webview.start()
