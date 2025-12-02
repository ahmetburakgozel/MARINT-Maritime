import pandas as pd
import os
import sys

# Proje dizinini yola ekle (src modülünü bulabilmesi için)
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.processor import DataProcessor
from src.visualizer import MapVisualizer

# --- CONFIGURATION ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "data", "raw", "AIS_UNACORN_Seatracks_past12-hours.csv")
OUTPUT_DIR = os.path.join(BASE_DIR, "outputs")
REPORT_FILE = os.path.join(OUTPUT_DIR, "suspicious_targets_report.csv")
MAP_FILE = os.path.join(OUTPUT_DIR, "marint_intelligence_map.html")


def ensure_directories():
    """Creates output directories if they don't exist."""
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)


def load_data(path):
    if not os.path.exists(path):
        print(f"--- [ERROR] Data file not found at: {path} ---")
        print("Please check 'data/raw' folder.")
        return None
    print(f"--- [INFO] Loading data from: {path} ---")
    return pd.read_csv(path)


def export_report(df, path):
    print(f"\n--- [INFO] Exporting Target List... ---")
    targets = df[df['is_spoofing']].copy()

    if targets.empty:
        print("--- [INFO] No targets found. ---")
        return

    cols = ['mmsi', 'name', 'callsign', 'navstatus', 'sog', 'timestamp', 'latitude', 'longitude']
    existing_cols = [c for c in cols if c in targets.columns]

    targets[existing_cols].sort_values(by='sog', ascending=False).to_csv(path, index=False)
    print(f"--- [SUCCESS] Report saved to: {path} ---")


def main():
    ensure_directories()

    # 1. Load
    df = load_data(DATA_PATH)
    if df is None: return

    df.columns = [c.lower() for c in df.columns]

    # 2. Process (Logic)
    processor = DataProcessor(df)
    df = processor.clean_data()
    df = processor.engineer_features()

    # 3. Summary
    summary = processor.get_summary()
    print(f"\n--- [INTELLIGENCE SUMMARY] ---")
    print(f"[*] Total Vessels: {summary['total_ships']}")
    print(f"[*] Spoofing Alerts: {summary['spoofing_anomalies_detected']}")
    print(f"[*] Gap Anomalies:   {summary['gap_anomalies_detected']}")

    # 4. Outputs
    export_report(df, REPORT_FILE)

    # 5. Visualize (Presentation)
    viz = MapVisualizer(df)
    viz.generate_map(MAP_FILE)


if __name__ == "__main__":
    main()