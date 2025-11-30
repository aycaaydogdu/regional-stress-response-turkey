"""
analyze_region_stress.py

Amaç:
- region_stress_index_weekly.csv + event_dates.csv dosyalarını okur
- Her event + bölge için pre/post stres ortalaması ve delta_stress hesaplar
- Basit ANOVA ile bölgeler arası delta_stress farkı var mı diye bakar

Çalıştırma:
    python analyze_region_stress.py
"""

import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
from statsmodels.formula.api import ols


# --------------------------
# 1) Veri yükleme
# --------------------------

def load_data(
    region_file="region_stress_index_weekly.csv",
    events_file="event_dates.csv"
):
    print(f"[INFO] Bölgesel stres verisi okunuyor: {region_file}")
    region = pd.read_csv(region_file)
    region["date"] = pd.to_datetime(region["date"])

    print(f"[INFO] Event tarihleri okunuyor: {events_file}")
    events = pd.read_csv(events_file)
    events["event_date"] = pd.to_datetime(events["event_date"])

    return region, events


# --------------------------
# 2) Basit EDA
# --------------------------

def run_eda(region):
    print("\n--- region_stress_index_weekly.head() ---")
    print(region.head())

    print("\n--- region_stress_index_weekly.describe() ---")
    print(region.describe())

    print("\n[INFO] 7 bölgenin stres indeksini çiziyorum...")
    plt.figure(figsize=(12, 6))
    for reg in sorted(region["region7"].unique()):
        sub = region[region["region7"] == reg]
        plt.plot(sub["date"], sub["stress_index"], label=reg, alpha=0.8)
    plt.title("7 Bölge İçin Haftalık Stres İndeksi (Google Trends)")
    plt.xlabel("Tarih")
    plt.ylabel("Stres İndeksi (z-score ortalaması)")
    plt.legend()
    plt.tight_layout()
    plt.show()


# --------------------------
# 3) Event + bölge paneli
# --------------------------

def build_event_panel(region, events,
                      pre_days=30, post_days=30,
                      out_file="event_region_stress_panel.csv"):
    """
    Her event + bölge için:
    - pre_mean: event_date - pre_days .. event_date-1
    - post_mean: event_date .. event_date + post_days
    - delta_stress: post_mean - pre_mean
    """
    print(f"\n[INFO] Event panel oluşturuluyor (pre={pre_days}, post={post_days})...")

    rows = []
    regions = sorted(region["region7"].unique())

    for _, ev in events.iterrows():
        ev_date = ev["event_date"]
        ev_type = ev["event_type"]

        for reg in regions:
            sub = region[region["region7"] == reg].copy()

            pre_mask = (sub["date"] >= ev_date - pd.Timedelta(days=pre_days)) & \
                       (sub["date"] < ev_date)
            post_mask = (sub["date"] >= ev_date) & \
                        (sub["date"] <= ev_date + pd.Timedelta(days=post_days))

            pre_mean = sub.loc[pre_mask, "stress_index"].mean()
            post_mean = sub.loc[post_mask, "stress_index"].mean()
            delta = post_mean - pre_mean

            rows.append({
                "event_date": ev_date,
                "event_type": ev_type,
                "region7": reg,
                "pre_mean": pre_mean,
                "post_mean": post_mean,
                "delta_stress": delta
            })

    panel = pd.DataFrame(rows)
    panel.to_csv(out_file, index=False)

    print(f"[OK] event_region_stress_panel kaydedildi: {out_file}")
    print(panel.head())

    return panel


# --------------------------
# 4) ANOVA: Bölgelerarası fark
# --------------------------

def run_anova(panel):
    """
    H0: delta_stress ortalaması tüm bölgelerde aynıdır.
    H1: En az bir bölgenin delta_stress ortalaması farklıdır.
    """
    df = panel.dropna(subset=["delta_stress"]).copy()

    print("\n--- ANOVA için gözlem sayısı ---")
    print(len(df))

    model = ols("delta_stress ~ C(region7)", data=df).fit()
    anova_table = sm.stats.anova_lm(model, typ=2)

    print("\n--- ANOVA Sonuçları (delta_stress ~ C(region7)) ---")
    print(anova_table)

    p_val = anova_table["PR(>F)"][0]
    alpha = 0.05

    if p_val < alpha:
        print(
            f"\nYorum: p={p_val:.4f} < {alpha} → H0 reddedilir."
            "\n       En az bir bölgenin event sonrası stres değişimi diğerlerinden farklı."
        )
    else:
        print(
            f"\nYorum: p={p_val:.4f} >= {alpha} → H0 reddedilemez."
            "\n       Bölgeler arasında event sonrası stres değişiminde anlamlı fark yok."
        )


# --------------------------
# MAIN
# --------------------------

if __name__ == "__main__":
    region, events = load_data()
    run_eda(region)
    panel = build_event_panel(region, events)
    run_anova(panel)
    print("\n[DONE] Bölgesel stres analizi tamamlandı.")
