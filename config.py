import os
import pathlib
from dotenv import load_dotenv

load_dotenv()

API_URL = "https://data.economie.gouv.fr/api/explore/v2.1/catalog/datasets/prix-des-carburants-en-france-flux-instantane-v2/records"
STATION_ID = int(os.environ.get("STATION_ID", "78570001"))
NTFY_TOPIC = os.environ.get("NTFY_TOPIC", "default_topic") 
WATCH = [c.strip() for c in os.environ.get("WATCH", "SP98").split(",")]
INTERVAL = int(os.environ.get("INTERVAL", "600"))
STATE_FILE = pathlib.Path(os.environ.get("STATE_FILE", "state.json"))
STALE_DAYS = 3
FAIL_ALERT = 6
