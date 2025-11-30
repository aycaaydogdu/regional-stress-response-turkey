"""
build_region_stress_index.py

Amaç:
- google_trends_province_timeseries.csv dosyasını okur
- Her il için stresle ilgili kelimeleri uzun forma (long) çevirir
- İl + keyword bazında z-score (standart skor) hesaplar
- 7 bölge (region7) düzeyinde haftalık ortalama z-score'u hesaplar
- Sonuç: region_stress_index_weekly.csv

Çalıştırma:
    python build_region_stress_index.py
"""

import pandas as pd
from scipy.stats import zscore


def build_region_stress_index(
    in_file="google_trends_province_timeseries.csv",
    out_file="region_stress_index_weekly.csv"
):
    # Veriyi oku
    print(f"[INFO] İl bazlı Trends verisi okunuyor: {in_file}")
    df = pd.read_csv(in_file)

    # Tarih formatı
    df["date"] = pd.to_datetime(df["date"])

    # Stresle ilgili keyword kolonları
    # Bu isimler collect_trends_provinces.py içindeki KW_LIST ile birebir aynı olmalı
    value_cols = ["anksiyete", "uykusuzluk", "stres", "panik atak", "mide yanması"]

    # long formata çevir (her satır: date, province, region7, keyword, score)
    long_df = df.melt(
        id_vars=["date", "province_code", "province", "region7"],
        value_vars=value_cols,
        var_name="keyword",
        value_name="score"
    )

    # Eksik skorları at
    long_df = long_df.dropna(subset=["score"])

    print("[INFO] Z-score hesaplanıyor (province + keyword bazında)...")

    # Her il + keyword için z-score (standartlaştırma)
    # Gruplar tek elemanlı ise zscore NaN verebilir, onları 0'a çekeceğiz.
    def zscore_safe(x):
        z = zscore(x, nan_policy="omit")
        # Tek gözlemde zscore 'nan' olabilir, 0 ile doldur
        if hasattr(z, "__len__"):
            return z
        else:
            return 0.0

    long_df["score_z"] = long_df.groupby(
        ["province", "keyword"]
    )["score"].transform(zscore_safe)

    # Kalan NaN'leri 0 yap
    long_df["score_z"] = long_df["score_z"].fillna(0)

    print("[INFO] Bölge bazında haftalık stres indeksi hesaplanıyor...")

    # Bölge + tarih düzeyinde ortalama z-score = regional stress index
    region_weekly = (
        long_df
        .groupby(["date", "region7"], as_index=False)["score_z"]
        .mean()
        .rename(columns={"score_z": "stress_index"})
        .sort_values(["region7", "date"])
    )

    # Kaydet
    region_weekly.to_csv(out_file, index=False)

    print(f"[OK] Bölgesel stres indeksi kaydedildi: {out_file}")
    print(region_weekly.head())


if __name__ == "__main__":
    build_region_stress_index()
