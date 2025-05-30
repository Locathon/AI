import json
from datetime import datetime
import os

LOG_FILE = "model/style_log.json"

def save_transform_log(original: str, transformed: str):
    log_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "original": original,
        "transformed": transformed
    }

    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            logs = json.load(f)
    else:
        logs = []

    logs.append(log_entry)

    with open(LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(logs, f, ensure_ascii=False, indent=2)
def load_transform_log():
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []