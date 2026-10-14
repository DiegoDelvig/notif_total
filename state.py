import json
from src import config

def load() -> dict:
    try:
        return json.loads(config.STATE_FILE.read_text())
    except (FileNotFoundError, ValueError):
        return {}

def save(state: dict):
    config.STATE_FILE.write_text(json.dumps(state))
