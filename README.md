# 🌍 Google Trends: Digital Interest in Sustainable Mobility (2018–2025)

This project analyzes how digital interest in urban and sustainable mobility has evolved in seven key countries (DE, FR, GB, IT, PT, US, ES), using search data from Google Trends. The aim is to explain variation in interest over time based on economic, sociodemographic, environmental, and infrastructure-related factors.

---

## 🎯 Objective

To build a **Digital Interest Index for Sustainable Mobility**, based on relevant and comparable search terms across countries, and to model its dynamics using panel data techniques. Explanatory variables include:

- Transportation and energy prices
- EV charging infrastructure
- Environmental and economic indicators
- Demographic and digital structure

---

## 📂 Project Structure

### `config/`
- `keywords_mapping.py`: defines the keyword list for each country in its local language. Exports the file `keywords_by_country_vertical.csv`.
- `common_keywords.py`: maps all language-specific keywords to standardized analytical categories such as `electric_car`, `car_sharing`, or `remote_work`.

### `src/`
- `trends_processing.py`: core data processing module. 
  - Loads raw Google Trends CSVs.
  - Performs linear regression-based imputation to complete the time series.
  - Applies z-score normalization and builds the full monthly panel by keyword and country.

### `scripts/`
- `preprocess.ipynb`: integrates all data sources (Google Trends, fuel prices, CPI, EV infrastructure, etc.) into the final monthly panel `df_model`.
- `download.py` / `download_proxy.py`: support scripts for downloading data via APIs or automated exports from Google Trends (local/remote versions may vary).

### `docs/`
- `paper_digital_mobility.docx`: main manuscript describing the research framework, methods and early results.

---

## 📊 Workflow

```plaintext
[config/keywords_mapping.py]
        ⬇
[config/common_keywords.py]
        ⬇
[src/trends_processing.py]  →  Imputed and normalized time series construction
        ⬇
[scripts/preprocess.ipynb]  →  Integration of contextual variables (CPI, charging, etc.)
        ⬇
```

---

## 🧾 Author

Developed by Antonio Gutiérrez (2024–2025) as part of a comparative study on digital mobility behavior.  
All scripts and data prepared for reproducible and scalable analysis.
