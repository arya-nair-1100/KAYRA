# Kayra — Personal Desktop Assistant 🚀

Kayra is a lightweight, cross-platform personal desktop assistant designed to help you stay on top of your daily schedule, weather conditions, and task deadlines. Featuring a modern Google Tasks-inspired graphical user interface, text-to-speech briefings, and full offline-first local data persistence, Kayra works seamlessly across macOS, Windows, and Linux.

---

## ✨ Features

* **Modern GUI Dashboard**: A clean, responsive web-based interface powered by `pywebview` and styled with Tailwind CSS, offering a Google Tasks-style checklist experience.
* **Smart Voice Briefings**: Fully offline text-to-speech integration (`pyttsx3`) that greets you, reads out current weather conditions, outlines your daily classes, and reminds you of upcoming deadlines.
* **Dynamic Task & Timetable Management**: Add, view, check off, and manage your tasks and weekly schedule with JSON-based persistence.
* **Live Weather Integration**: Real-time weather forecasting powered by the Open-Meteo API (no API key required).
* **Cross-Platform Compatibility**: Built natively with modular Python architecture, ensuring smooth execution on macOS, Windows, and Linux.

---

## 📂 Project Structure

```text
KAYRA/
├── app.py              # Native desktop GUI bridge (pywebview)
├── main.py             # Core CLI entry point and execution handler
├── assistant.py        # TTS engine and weather/briefing intelligence
├── data_manager.py     # JSON data handler for tasks and timetables
├── index.html          # Frontend dashboard UI (Tailwind CSS & JavaScript)
└── data/
    ├── tasks.json      # Local task storage database
    └── timetable.json  # Weekly class schedule configuration
