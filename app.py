import webview
import json
import os
from data_manager import load_tasks, add_task, mark_task_done, load_timetable
from assistant import fetch_weather, build_briefing, speak

class Api:
    def get_data(self):
        """Fetch tasks, timetable, and weather for the dashboard."""
        tasks = load_tasks()
        timetable = load_timetable()
        weather = fetch_weather()
        return {
            "tasks": tasks,
            "timetable": timetable,
            "weather": weather
        }

    def add_new_task(self, title, subject, deadline, priority):
        """Add a task from the UI."""
        add_task(title, subject, deadline, priority)
        return {"status": "success"}

    def complete_task(self, task_id):
        """Mark a task as done from the UI."""
        mark_task_done(int(task_id))
        return {"status": "success"}

    def trigger_briefing(self):
        """Play the audio briefing."""
        weather = fetch_weather()
        briefing = build_briefing(weather)
        speak(briefing)
        return {"status": "spoken"}

if __name__ == '__main__':
    api = Api()
    # Create the native desktop window pointing to your HTML file
    window = webview.create_window(
        'Kayra — Personal Assistant', 
        'index.html', 
        js_api=api, 
        width=1000, 
        height=700,
        min_size=(800, 600)
    )
    webview.start()
