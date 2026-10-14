import argparse
import time
from src import monitor, config

def main():
    ap = argparse.ArgumentParser(description="Surveille la dispo de carburants.")
    ap.add_argument("--once", action="store_true", help="Un seul passage (cron, CI)")
    args = ap.parse_args()

    while True:
        try:
            monitor.check()
        except Exception as e:
            monitor.log("Erreur critique inattendue :", e)
        
        if args.once:
            break
        time.sleep(config.INTERVAL)

if __name__ == "__main__":
    main()
