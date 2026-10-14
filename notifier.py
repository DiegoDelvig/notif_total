import requests
import unicodedata
from src import config

def ascii_only(s: str) -> str:
    return unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode("ascii")

def notify(msg: str, title: str = "Carburant", priority: str = "default"):
    r = requests.post(
        f"https://ntfy.sh/{config.NTFY_TOPIC}",
        data=ascii_only(msg).encode("ascii"),
        headers={"Title": ascii_only(title), "Priority": priority, "Tags": "fuelpump"},
        timeout=20
    )
    r.raise_for_status()
