# Data Preprocessing Pipeline

## 1. Dataset
- **Source**: CERT Insider Threat Dataset v6.2 (synthetic logs)
- **Raw file location**: `data/raw`
- **Processed file location**: `data/processed/threatsight_clean.csv`

## 2. Steps Performed
1. **Load Data**
   - Used `pandas` to load raw CSV file.
2. **Parse Timestamps**
   - Converted timestamp strings to `datetime` objects using `pd.to_datetime`.
3. **Select & Normalize Columns**
   - Kept: `username`, `ip_address`, `action_type`, `timestamp`
4. **Geolocation**
   - Split IP-based location into `city` and `country` using `ip2geotools`.
5. **Data Cleaning**
   - Removed rows with missing/invalid IP addresses.
6. **Save**
   - Saved cleaned dataset to `data/processed/threatsight_clean.csv`.

## 3. Notes
- No rows were removed during cleaning (`30252` before and after).
- Geolocation API may need a key if scaled to larger datasets.
