import folium
from folium.plugins import FastMarkerCluster
import os


class MapVisualizer:
    def __init__(self, df):
        self.df = df

    def generate_map(self, output_path):
        """
        Generates the interactive map and saves it to the specified path.
        """
        print("\n--- [VISUALIZER] Generating Interactive Map... ---")

        center_lat = self.df['latitude'].mean()
        center_lon = self.df['longitude'].mean()

        # Base Map
        m = folium.Map(location=[center_lat, center_lon], zoom_start=5, tiles='CartoDB dark_matter')

        # Filter Data
        anomalies_gap = self.df[self.df['is_gap_anomaly']]
        anomalies_spoof = self.df[self.df['is_spoofing']]

        # Sample Normal Traffic (Optimization)
        normal_df = self.df[~(self.df['is_gap_anomaly']) & ~(self.df['is_spoofing'])]
        if len(normal_df) > 10000:
            normal_df = normal_df.sample(n=10000, random_state=42)

        # Layer 1: Normal Traffic
        print(f"--- [MAP] Adding {len(normal_df)} normal traffic points...")
        FastMarkerCluster(data=list(zip(normal_df['latitude'], normal_df['longitude'])),
                          name="Normal Traffic (Blue)").add_to(m)

        # Layer 2: Gap Anomalies
        print(f"--- [MAP] Adding {len(anomalies_gap)} Gap Anomalies...")
        for _, row in anomalies_gap.iterrows():
            folium.CircleMarker(
                location=[row['latitude'], row['longitude']],
                radius=3, color='red', fill=True, fill_opacity=0.6,
                popup=f"<b>GOING DARK</b><br>MMSI: {row['mmsi']}"
            ).add_to(m)

        # Layer 3: Spoofing Anomalies
        print(f"--- [MAP] Adding {len(anomalies_spoof)} Spoofing Anomalies...")
        for _, row in anomalies_spoof.iterrows():
            folium.CircleMarker(
                location=[row['latitude'], row['longitude']],
                radius=6, color='orange', fill=True, fill_opacity=0.9,
                popup=f"<b>SPOOFING ALERT</b><br>Name: {row['name']}<br>Claimed: {row['navstatus']}<br>Speed: {row['sog']} kn"
            ).add_to(m)

        # Save
        m.save(output_path)
        print(f"--- [SUCCESS] Map saved to: {output_path} ---")