import pandas as pd
import numpy as np


class DataProcessor:
    def __init__(self, df):
        self.df = df

    def clean_data(self):
        """
        Performs basic data cleaning: removing artifacts and formatting dates.
        """
        print("--- [PROCESS] Starting Data Cleaning... ---")

        # 1. Drop the artifact index column if it exists
        if 'Unnamed: 0' in self.df.columns:
            self.df.drop(columns=['Unnamed: 0'], inplace=True)

        # 2. Convert 'timeoffix' (Unix epoch) to readable datetime
        # We assume timeoffix is in seconds.
        self.df['timestamp'] = pd.to_datetime(self.df['timeoffix'], unit='s')

        # 3. Sort data by Ship ID (mmsi) and Time.
        # CRITICAL: We cannot calculate trajectories if data isn't sorted by time for each ship.
        self.df = self.df.sort_values(by=['mmsi', 'timestamp']).reset_index(drop=True)

        print("--- [SUCCESS] Data cleaned and sorted by MMSI and Time. ---")
        return self.df

    def engineer_features(self):
        """
        Derives features for:
        1. 'Going Dark' (Long Signal Gaps > 4 hours)
        2. 'Spoofing' (NavStatus vs Speed Mismatch)
        """
        print("--- [PROCESS] Starting Feature Engineering (Level 2)... ---")

        # 1. Time Difference calculation per ship
        self.df['dt_seconds'] = self.df.groupby('mmsi')['timestamp'].diff().dt.total_seconds()

        # --- ANOMALY TYPE 1: GOING DARK ---
        # We increase threshold to 4 hours (14400 seconds) to reduce false positives (noise).
        # 1 hour was too sensitive; 4 hours indicates a deliberate action or major failure.
        gap_threshold = 14400
        self.df['is_gap_anomaly'] = self.df['dt_seconds'] > gap_threshold

        # --- ANOMALY TYPE 2: SPOOFING (SPEED MISMATCH) ---
        # Logic: If a ship claims status 'Anchored' or 'Moored' but Speed > 3.0 knots.
        # This suggests the crew is trying to hide movement while appearing stationary in logs.

        # Create a boolean mask for declared static status (Case insensitive)
        is_static_declared = self.df['navstatus'].str.contains('Anchored|Moored', case=False, na=False)

        # Create a boolean mask for actual movement (> 3 knots)
        is_moving_actually = self.df['sog'] > 3.0

        self.df['is_spoofing'] = is_static_declared & is_moving_actually

        # Clean up NaNs created by shifting
        self.df = self.df.dropna(subset=['dt_seconds'])

        print("--- [SUCCESS] Features engineered. Gap & Spoofing anomalies marked. ---")
        return self.df

    def get_summary(self):
        """
        Returns a high-level summary of the processed data.
        """
        unique_ships = self.df['mmsi'].nunique()
        gap_count = self.df['is_gap_anomaly'].sum()
        spoofing_count = self.df['is_spoofing'].sum()

        return {
            "total_ships": unique_ships,
            "gap_anomalies_detected": gap_count,
            "spoofing_anomalies_detected": spoofing_count
        }