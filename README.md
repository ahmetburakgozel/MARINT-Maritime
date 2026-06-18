# 🚢 MARINT: Maritime Intelligence & Anomaly Detection System

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue)](https://www.python.org/)
[![Type](https://img.shields.io/badge/Type-OSINT-red)](https://en.wikipedia.org/wiki/Open-source_intelligence)
[![Status](https://img.shields.io/badge/Status-Prototype-orange)](https://github.com/condor-k/MARINT-Maritime-Intelligence)
[![License](https://img.shields.io/badge/License-MIT-green)](https://opensource.org/licenses/MIT)

**MARINT** is an Open Source Intelligence (OSINT) tool designed to process AIS (Automatic Identification System) data for **Maritime Situational Awareness**. It automatically filters millions of data points to detect suspicious vessel behaviors, generate target lists, and visualize threats on an interactive tactical map.

---

## 📖 Table of Contents

- [🎯 Core Capabilities](#-core-capabilities)
- [📂 Project Architecture](#-project-architecture)
- [🚀 Getting Started](#-getting-started)
- [📊 Intelligence Products](#-intelligence-products)
- [📈 Sample Findings](#-sample-findings)
- [⚠️ Disclaimer](#️-disclaimer)

---

## 🎯 Core Capabilities

In the vastness of the oceans, manually tracking every vessel is impossible. MARINT acts as an automated "watchdog" to identify high-risk anomalies:

*   **🕵️‍♂️ Spoofing Detection:** Identifies vessels broadcasting a false navigation status.
    > *Logic:* If a ship claims to be `"Anchored"` or `"Moored"` but is moving at a speed **> 3.0 knots**, it is flagged as a spoofer attempting to mask its true activity.

*   **🌑 "Going Dark" Analysis:** Detects vessels that disable their AIS transponders for extended periods.
    > *Logic:* Flags vessels with signal gaps exceeding **4 hours**, a behavior often associated with illicit activities (smuggling, illegal fishing, etc.).

*   **🗺️ Interactive Tactical Map:** Generates a detailed HTML map visualizing normal traffic versus identified threats.

---

## 📂 Project Architecture

The project is structured for modularity and scalability:

```
MARINT-Maritime/
├── data/
│   └── raw/                   # Raw AIS datasets (CSV)
├── outputs/                   # Generated Intelligence Products
│   ├── marint_intelligence_map.html  # Interactive Map
│   └── suspicious_targets_report.csv # Suspicious Targets Report
├── src/                       # Source Code
│   ├── processor.py           # Data Cleaning & Anomaly Detection
│   └── visualizer.py          # Map Generation & Layering
├── run_analysis.py            # Main execution script
├── requirements.txt           # Project dependencies
└── README.md                  # This file
```

---

## 🚀 Getting Started

Follow these steps to run the analysis.

### 1. Clone the Repository
```bash
git clone https://github.com/ahmetburakgozel/MARINT-Maritime-Intelligence.git
cd MARINT-Maritime-Intelligence
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the Analysis
Execute the main script to process the data and generate the intelligence products:
```bash
python run_analysis.py
```

---

## 📊 Intelligence Products

Upon successful execution, two key files are generated in the `outputs/` directory:

### 1. Tactical Map (`marint_intelligence_map.html`)
An interactive Folium map, viewable in any web browser.

| Marker | Meaning |
| :--- | :--- |
| 🔵 **Blue Clusters** | Normal maritime traffic |
| 🔴 **Red Markers** | Vessels that "went dark" (>4h signal gap) |
| 🟠 **Orange Markers** | Spoofing targets (false status broadcast) |

### 2. Target List (`suspicious_targets_report.csv`)
A CSV report listing all suspicious vessels flagged during the analysis. It includes:
- `MMSI`
- `Name`
- `Callsign`
- `NavStatus` (Claimed)
- `SOG` (Actual Speed)
- `Coordinates`
- `Timestamp`

---

## 📈 Sample Findings (12-Hour Snapshot)

A test run on a sample AIS dataset yielded the following:

- **Total Vessels Tracked:** ~27,357
- **High-Risk Spoofing Alerts:** 124 vessels detected moving while claiming to be anchored.
- **Signal Gap Anomalies:** ~12,900 vessels with significant coverage gaps identified.

---

## ⚠️ Disclaimer

> This project is for educational and research purposes only and utilizes publicly available datasets. It is not intended for operational use or real-world decision-making.
