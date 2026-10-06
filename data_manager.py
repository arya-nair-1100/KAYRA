# ── Quick Notes & Exams ──────────────────────────────────────────────────────
NOTES_FILE = os.path.join(_DATA_DIR, "notes.txt")
EXAMS_FILE = os.path.join(_DATA_DIR, "exams.json")

def load_notes() -> str:
    """Load scratchpad text from notes.txt."""
    _ensure_data_dir()
    if not os.path.exists(NOTES_FILE):
        return ""
    with open(NOTES_FILE, "r", encoding="utf-8") as f:
        return f.read()

def save_notes(content: str) -> None:
    """Save scratchpad text to notes.txt."""
    _ensure_data_dir()
    with open(NOTES_FILE, "w", encoding="utf-8") as f:
        f.write(content)

def load_exams() -> List[Dict[str, Any]]:
    """Load upcoming exams or major deadlines."""
    _ensure_data_dir()
    if not os.path.exists(EXAMS_FILE):
        # Default sample exam
        return [{"title": "Computer Science Midterm", "date": "2026-10-15"}]
    with open(EXAMS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def get_closest_exam() -> Dict[str, Any]:
    """Return the nearest upcoming exam with days left."""
    exams = load_exams()
    today = date.today()
    valid_exams = []
    
    for exam in exams:
        try:
            exam_date = datetime.strptime(exam["date"], "%Y-%m-%d").date()
            delta = (exam_date - today).days
            if delta >= 0:
                valid_exams.append({"title": exam["title"], "days_left": delta})
        except (KeyError, ValueError):
            continue
            
    if not valid_exams:
        return {"title": "No upcoming exams", "days_left": 999}
        
    valid_exams.sort(key=lambda x: x["days_left"])
    return valid_exams[0]
