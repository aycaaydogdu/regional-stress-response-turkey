"""
build_event_dates.py

Amaç:
- earthquake.csv içinden "büyük ve sığ" depremleri seçip event tarihleri üretir
- USD_TRY Historical Data.csv içinden "kur şoku" günlerini seçip event tarihleri üretir
- İkisini birleştirip event_dates.csv olarak kaydeder

Çalıştırma:
    python build_event_dates.py
"""

import pandas as pd
import numpy as np


# Eşik değerleri istersen buradan değiştirebilirsin
MAG_MIN = 4.5        # Deprem için minimum magnitüd
DEPTH_MIN = 0.0      # Deprem derinliği alt sınır (km)
DEPTH_MAX = 40.0     # Deprem derinliği üst sınır (km)

FX_RET_THRESHOLD = 0.02  # Kur şoku için log-getiri eşiği (~%2)


def build_event_dates(
    eq_file="earthquake.csv",
    fx_file="USD_TRY Historical Data.csv",
    out_file="event_dates.csv"
):
    # --------------------------------------------------
    # 1) Deprem event tarihleri
    # --------------------------------------------------
    print(f"[INFO] Deprem verisi okunuyor: {eq_file}")
    eq = pd.read_csv(eq_file)

    # AFAD CSV'inde Date kolonu: '31/10/2025 07:18:50' formatında (gün/ay/yıl)
    eq["date"] = pd.to_datetime(eq["Date"], dayfirst=True, errors="coerce")
    eq = eq.dropna(subset=["date"])

    # Filtre: Magnitüd ≥ MAG_MIN ve derinlik DEPTH_MIN–DEPTH_MAX arası
    mask_mag = eq["Magnitude"] >= MAG_MIN
    mask_depth = (eq["Depth"] >= DEPTH_MIN) & (eq["Depth"] <= DEPTH_MAX)
    eq_big = eq[mask_mag & mask_depth].copy()

    # Sadece tarih (saatten bağımsız)
    eq_big["event_date"] = eq_big["date"].dt.date

    # Tekil günleri al
    eq_dates = (
        eq_big[["event_date"]]
        .drop_duplicates()
        .sort_values("event_date")
        .reset_index(drop=True)
    )
    eq_dates["event_type"] = "earthquake"

    print(f"[INFO] Deprem event günü sayısı: {len(eq_dates)}")

    # --------------------------------------------------
    # 2) Kur şoku event tarihleri
    # --------------------------------------------------
    print(f"[INFO] Kur verisi okunuyor: {fx_file}")
    fx = pd.read_csv(fx_file)

    # USD_TRY dosyasında Date: '11/23/2025' formatı (ay/gün/yıl)
    fx["date"] = pd.to_datetime(fx["Date"], dayfirst=False, errors="coerce")
    fx = fx.dropna(subset=["date"])

    # Tarihe göre sırala (çoğu finans datası tersten gelir)
    fx = fx.sort_values("date")

    # Fiyatı numeric yap
    fx["price"] = pd.to_numeric(fx["Price"], errors="coerce")
    fx = fx.dropna(subset=["price"])

    # Günlük/haftalık log-getiri
    fx["ret"] = np.log(fx["price"]).diff()

    # Şok tanımı: |ret| > FX_RET_THRESHOLD
    fx_shock = fx[fx["ret"].abs() > FX_RET_THRESHOLD].copy()

    # Kur şoku event tarihleri
    fx_shock["event_date"] = fx_shock["date"].dt.date

    fx_dates = (
        fx_shock[["event_date"]]
        .drop_duplicates()
        .sort_values("event_date")
        .reset_index(drop=True)
    )
    fx_dates["event_type"] = "fx_shock"

    print(f"[INFO] Kur şoku event günü sayısı: {len(fx_dates)}")

    # --------------------------------------------------
    # 3) Birleştir ve kaydet
    # --------------------------------------------------
    events = pd.concat([eq_dates, fx_dates], ignore_index=True)
    events = events.sort_values("event_date").reset_index(drop=True)

    events.to_csv(out_file, index=False)

    print(f"[OK] Toplam {len(events)} event günü '{out_file}' dosyasına kaydedildi.")
    print(events.head())


if __name__ == "__main__":
    build_event_dates()
