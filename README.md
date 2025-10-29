# Elections-and-Macroeconomic-Shocks-vs-Turkey’s-Reaction-by-Region

## *Project Idea*

This project aims to investigate how different regions of Türkiye react to nationwide stressful events such as **economic shocks** and **monetary policy decisions**.  
The central hypothesis is that Türkiye’s seven geographical regions respond to national stressors at **different intensities and time lags**.  

By analyzing **Google Trends** data for stress-related search terms across provinces and comparing them with **macroeconomic indicators** (e.g., currency volatility, inflation announcements, and central bank interest-rate decisions), the project seeks to determine whether some regions get “stressed out” earlier or more strongly than others when faced with the same national event.

---

## *Description of Dataset*

The project will utilize two primary datasets:

### *Google Trends Dataset (Regional Stress Indicators)*  
- **Search Keywords:** “anksiyete”, “uykusuzluk”, “stres”, “panik atak”, “mide yanması”  
- **Geographical Coverage:** All 81 Turkish provinces (aggregated into 7 official geographical regions)  
- **Temporal Range:** 2018 – 2025 (weekly)  
- **Metric:** Google Trends interest score (0–100), normalized by region  
- **Purpose:** Proxy for regional stress level and timing of reactions to national events  
- **Source:** [Google Trends](https://trends.google.com/trends/?geo=TR) via [PyTrends Python Library](https://github.com/GeneralMills/pytrends)  

### *Macroeconomic and Event Dataset (Stressful Event Indicators)*  
- **USD/TRY Exchange Rate:** Daily data from the [TCMB EVDS Data Portal](https://evds2.tcmb.gov.tr/)  
- **Economic Volatility Index:** 7-day rolling standard deviation of daily USD/TRY returns  
- **Monetary Policy Decisions (MPC Dates):** [TCMB Monetary Policy Committee Calendar](https://www.tcmb.gov.tr/wps/wcm/connect/en/tcmb+en/main+menu/monetary+policy/monetary+policy+committee/)  
- **Inflation (CPI) Release Dates:** [TÜİK CPI Release Schedule](https://data.tuik.gov.tr/)  
- **Optional Events:** Major earthquakes from the [AFAD Earthquake Catalog](https://deprem.afad.gov.tr/event-catalog) weighted by regional exposure  

---

## *Plan*

### *Data Collection*

- **Stress Data Sources:**  
  - Google Trends data pulled via PyTrends (`interest_by_region`, `interest_over_time`)  
  - [TÜİK ABPRS Population Data](https://data.tuik.gov.tr/) for population weighting by region  

- **Macroeconomic & Event Data Sources:**  
  - TCMB EVDS API for USD/TRY and MPC decision dates  
  - TÜİK data portal for inflation (CPI) release calendar  
  - AFAD earthquake records (optional control variable)  

---

### *Data Analysis Approach*

1. **Exploratory Data Analysis (EDA)**  
   - Visualize regional stress levels over time  
   - Identify synchronous and asynchronous responses among regions  
   - Examine ±30-day windows around major macroeconomic or policy events  

2. **Statistical Analysis**  
   - Cross-correlation and distributed-lag analysis between stress indices and macro shocks  
   - Event-study analysis on MPC and CPI dates  
   - Time-to-peak and lead-lag comparisons across the seven regions  

3. **Visualization and Presentation**  
   - Line plots comparing regional stress trends around events  
   - Heatmap showing lag time of stress responses by region  
   - Choropleth map of Türkiye colored by reaction speed or amplitude  

---

### *Tools and Technologies*

- **Python** – Core language for data collection and analysis  
- **PyTrends** – Google Trends API wrapper  
- **Pandas & NumPy** – Data cleaning, transformation, and aggregation  
- **Matplotlib & Seaborn** – Data visualization  
- **Statsmodels** – Correlation and lag regression modeling  
- **Jupyter Notebooks** – For documentation and reproducible workflow  

---

## *Expected Outcomes*

- Quantitative evidence of whether Türkiye’s regions react differently to national economic stressors  
- Identification of “early-reacting” vs. “delayed” regions after macroeconomic shocks  
- Insights into how socioeconomic or cultural characteristics affect stress sensitivity  
- Framework for continuous stress monitoring using open data sources  
- Visual tools to compare collective anxiety dynamics across regions  

---

## *Potential Challenges*

- Google Trends normalization (relative scores, not absolute values)  
- Sparse data for smaller provinces leading to noise in regional aggregation  
- Overlapping local vs. national events complicating causal interpretation  
- Ensuring comparability between event types (MPC, CPI, FX volatility)  
- Differentiating correlation from causation in temporal analyses  

---

This project will contribute to understanding how **collective stress responses differ across Türkiye’s regions**, revealing potential cultural, economic, and informational asymmetries in how populations react to uncertainty and macro-level shocks.

---

### ✅ **Recommended GitHub Repo Name**
`Regional-Stress-Response-Turkey`
