# MiniQRadar
## Data Preprocessing
See [docs/preprocessing.md](docs/preprocessing.md) for full preprocessing details.
ThreatSight — Insider Threat Detection Prototype

Overview
ThreatSight is a log analysis and threat detection tool aimed at identifying suspicious activities within an organization. It processes user activity logs, enriches them with geolocation data, and prepares them for anomaly detection.
The project’s initial focus is on data preprocessing and pipeline setup to enable rapid experimentation with threat detection models.

Key Features (Day 1 Scope)

Load and clean user activity log data (CERT dataset or synthetic logs).

Parse and normalize timestamps, usernames, IP addresses, and actions.

Enrich logs with geolocation data from IP addresses.

Save clean, structured data for modeling and visualization.

Maintain reproducibility via a shared environment and clear dependencies.

Target Use Case

Security analysts can use ThreatSight to detect anomalies such as:

Unusual login times

Access from unexpected geographic locations

Multiple failed logins before success

File access anomalies

Planned Tech Stack

Python (pandas, numpy, scikit-learn)

Geolocation (geopy, geoip2)

Visualization (matplotlib, seaborn)

Interface (streamlit or flask for later stages)

Version Control (GitHub)

Current Status

✅ Dataset sourced and explored

✅ Preprocessing pipeline draft complete

🚧 Environment setup & dependency list in progress

🚧 IP geolocation library integration in progress
