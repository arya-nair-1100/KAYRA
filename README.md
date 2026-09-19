# 🤖 Kayra Assistant

> A cross-platform desktop personal secretary built in Python — free for everyone.

Kayra delivers a spoken morning briefing that covers:

- 📅 Current date & time with a greeting
- 🌤️ Live local weather via [Open-Meteo](https://open-meteo.com/) (no API key needed)
- 🏫 Today's class schedule from your timetable
- 📝 Upcoming task deadlines (next 7 days, sorted by urgency)

All speech is synthesised **offline** using `pyttsx3` — no internet required for TTS.

---

## 📁 Project Structure

```
KAYRA/
├── main.py           # Entry point & CLI
├── assistant.py      # Weather, briefing, TTS
├── data_manager.py   # JSON I/O for tasks & timetable
├── requirements.txt  # Python dependencies
├── README.md         # This file
└── data/
    ├── tasks.json      # Your task deadlines
    └── timetable.json  # Your weekly class schedule
```

---

## 🚀 Quick Start

### 1. Prerequisites

- **Python 3.10+** — [python.org/downloads](https://www.python.org/downloads/)
- **pip** (bundled with Python)

> **Windows users:** The installer already includes pip.  
> **macOS/Linux users:** Run `python3 -m ensurepip --upgrade` if pip is missing.

### 2. Clone the Repository

```bash
git clone https://github.com/your-username/kayra-assistant.git
cd kayra-assistant
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

> **Linux extra step:** pyttsx3 needs `espeak` and `ffmpeg`:
> ```bash
> sudo apt-get install espeak ffmpeg libespeak1   # Debian/Ubuntu
> sudo dnf install espeak                          # Fedora
> ```

### 4. Customise Your Data

#### `data/timetable.json`

Edit the weekly schedule. Each day is an array of classes:

```json
{
  "Monday": [
    {"time": "09:00", "subject": "Mathematics", "room": "A101"},
    {"time": "11:00", "subject": "Physics",     "room": "B204"}
  ],
  "Tuesday": []
}
```

#### `data/tasks.json`

Edit your tasks manually or use the `--add-task` CLI flag (see below).
Each task looks like:

```json
{
  "id": 1,
  "title": "Submit Assignment 1",
  "subject": "Mathematics",
  "deadline": "2026-09-25",
  "priority": "high",
  "done": false
}
```

---

## 🖥️ Usage

### Full Briefing (print + spoken TTS)

```bash
python main.py
```

### Text-only Mode (no TTS)

```bash
python main.py --text
```

### Add a New Task (interactive)

```bash
python main.py --add-task
```

### Mark a Task as Done

```bash
python main.py --done 2    # marks task with id=2 as done
```

### Custom Location for Weather

```bash
python main.py --lat 28.6139 --lon 77.2090   # New Delhi
```

Or set environment variables permanently:

```bash
export KAYRA_LAT=51.5074
export KAYRA_LON=-0.1278   # London
```

---

## 🌍 Setting Your Location

Kayra defaults to **Bengaluru, India** (lat 12.9716, lon 77.5946).  
Find your coordinates at [latlong.net](https://www.latlong.net/) and either:

1. Pass `--lat` and `--lon` flags each time, or
2. Set `KAYRA_LAT` / `KAYRA_LON` environment variables.

---

## 📦 Packaging as a Standalone Desktop App

You can bundle Kayra into a single executable (no Python installation needed on the end-user machine) using **PyInstaller**.

### Install PyInstaller

```bash
pip install pyinstaller
```

### Build

```bash
# macOS / Linux
pyinstaller --onefile --name kayra main.py

# Windows
pyinstaller --onefile --name kayra.exe main.py
```

The executable and the `data/` folder will need to sit together.  
After building, copy your `data/` directory next to the generated executable:

```
dist/
├── kayra          (or kayra.exe on Windows)
└── data/
    ├── tasks.json
    └── timetable.json
```

Run it:

```bash
./dist/kayra          # macOS/Linux
dist\kayra.exe        # Windows
```

### Build with bundled data (advanced)

Add a `--add-data` flag to bundle `data/` inside the executable:

```bash
# macOS / Linux
pyinstaller --onefile --name kayra \
    --add-data "data:data" \
    main.py

# Windows (semicolon separator)
pyinstaller --onefile --name kayra ^
    --add-data "data;data" ^
    main.py
```

---

## 🔧 Troubleshooting

| Problem | Solution |
|---|---|
| `ModuleNotFoundError: pyttsx3` | Run `pip install -r requirements.txt` |
| No sound on Linux | Install `espeak`: `sudo apt-get install espeak` |
| Weather returns "unavailable" | Check your internet connection |
| Wrong weather location | Use `--lat` / `--lon` flags or set env vars |
| `pyinstaller` command not found | Run `pip install pyinstaller` |

---

## 📄 License

MIT — free to use, modify, and distribute. See `LICENSE` for details.

---

## 🙏 Acknowledgements

- [Open-Meteo](https://open-meteo.com/) for the free, no-key weather API
- [pyttsx3](https://github.com/nateshmbhat/pyttsx3) for cross-platform offline TTS
- [Requests](https://docs.python-requests.org/) for clean HTTP handling
