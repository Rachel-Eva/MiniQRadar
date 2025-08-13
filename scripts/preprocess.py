import re
from pathlib import Path
import pandas as pd
import geoip2.database

RAW_PATH = Path("data/raw/threatsight_synthetic_log.csv")
PROCESSED_DIR = Path("data/processed")
PROCESSED_PATH = PROCESSED_DIR / "threatsight_clean.csv"

def valid_ipv4(ip: str) -> bool:
    # Simple IPv4 validator
    m = re.match(r"^(\d{1,3}\.){3}\d{1,3}$", str(ip))
    if not m:
        return False
    parts = [int(p) for p in ip.split(".") if p.isdigit()]
    return len(parts) == 4 and all(0 <= p <= 255 for p in parts)

def preprocess(input_path: Path, output_path: Path) -> pd.DataFrame:
    print(f"Loading raw data from {input_path}")
    df = pd.read_csv(input_path)

    # --- Parse timestamps (Step 4)
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")

    # --- Normalize key columns (Step 5)
    df = df.rename(columns={
        "user_id": "user",
        "ip_address": "ip",
        "event_type": "action",
        "file_name": "file"
    })

    # --- Split existing location column into city/country if present
    if "location" in df.columns:
        city = []
        country = []
        for loc in df["location"].astype(str):
            parts = [p.strip() for p in loc.split(",")]
            if len(parts) >= 2:
                city.append(parts[0])
                country.append(parts[-1])
            else:
                city.append(parts[0] if parts else "")
                country.append("")
        df["city"] = city
        df["country"] = country

    # --- Clean data (Step 7)
    core = ["user", "timestamp", "ip", "action"]
    before = len(df)
    df = df.dropna(subset=core)

    # Validate IPs; set invalid to NaN then drop
    df.loc[~df["ip"].map(valid_ipv4), "ip"] = pd.NA
    df = df.dropna(subset=["ip"])

    # file column: if action is file_access & file is NaN -> "unknown", else fill "N/A"
    df["file"] = df["file"].where(df["file"].notna(), None)
    is_file_event = df["action"] == "file_access"
    df.loc[is_file_event & df["file"].isna(), "file"] = "unknown"
    df["file"] = df["file"].fillna("N/A")

    # Ensure bools are bool
    for bcol in ["success", "anomaly"]:
        if bcol in df.columns:
            df[bcol] = df[bcol].astype(bool)

    # --- Enrich IPs with geolocation using geoip2
    print("Enriching data with geolocation from IP addresses...")
    geo_city = []
    geo_country = []

    # Update this path if your mmdb file is elsewhere
    mmdb_path = Path("data\GeoLite2-City\GeoLite2-City_20250811\GeoLite2-City.mmdb")
    with geoip2.database.Reader(str(mmdb_path)) as reader:
        def lookup_location(ip):
            try:
                response = reader.city(ip)
                city_name = response.city.name or ""
                country_name = response.country.name or ""
                return city_name, country_name
            except Exception:
                return "", ""

        for ip in df["ip"]:
            city_name, country_name = lookup_location(ip)
            geo_city.append(city_name)
            geo_country.append(country_name)

    df["geo_city"] = geo_city
    df["geo_country"] = geo_country

    # --- Feature engineering (useful later)
    df["hour"] = df["timestamp"].dt.hour
    df["day_of_week"] = df["timestamp"].dt.dayofweek
    df["date"] = df["timestamp"].dt.date.astype(str)

    # Reorder columns nicely
    cols = [
        "user", "ip", "action", "timestamp", "date", "hour", "day_of_week",
        "file", "city", "country", "geo_city", "geo_country", "success", "anomaly"
    ]
    cols = [c for c in cols if c in df.columns]
    df = df[cols]

    # --- Save (Step 8)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)

    after = len(df)
    kept_pct = (after / before) * 100 if before else 100
    print(f"Rows before: {before} | after: {after} | kept: {kept_pct:.2f}%")
    print(f"Saved cleaned data to: {output_path}")
    return df

if __name__ == "__main__":
    preprocess(RAW_PATH, PROCESSED_PATH)
