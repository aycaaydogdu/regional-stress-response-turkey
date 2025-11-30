"""
collect_trends_provinces.py

Bu script şunları yapar:

- Türkiye'deki 81 il için ISO kodlarını ve 7 coğrafi bölgeyi tanımlar
- Her il için Google Trends'ten (interest_over_time) 2018-2025 haftalık zaman serisi çeker
- Sonuçları tek bir CSV'de toplar: google_trends_province_timeseries.csv

Çalıştırma:
    python collect_trends_provinces.py
"""

from pytrends.request import TrendReq
import pandas as pd
import time

# --------------------------------------------------
# 81 il + ISO kodu + 7 bölge (Marmara, Ege, Akdeniz,
# İç Anadolu, Karadeniz, Doğu Anadolu, Güneydoğu Anadolu)
# --------------------------------------------------
PROVINCES = [
    # Akdeniz
    {"code": "TR-01", "province": "Adana",        "region7": "Akdeniz"},
    {"code": "TR-07", "province": "Antalya",      "region7": "Akdeniz"},
    {"code": "TR-15", "province": "Burdur",       "region7": "Akdeniz"},
    {"code": "TR-31", "province": "Hatay",        "region7": "Akdeniz"},
    {"code": "TR-32", "province": "Isparta",      "region7": "Akdeniz"},
    {"code": "TR-33", "province": "Mersin",       "region7": "Akdeniz"},
    {"code": "TR-46", "province": "Kahramanmaraş","region7": "Akdeniz"},
    {"code": "TR-80", "province": "Osmaniye",     "region7": "Akdeniz"},

    # Ege
    {"code": "TR-03", "province": "Afyonkarahisar","region7": "Ege"},
    {"code": "TR-09", "province": "Aydın",         "region7": "Ege"},
    {"code": "TR-20", "province": "Denizli",       "region7": "Ege"},
    {"code": "TR-35", "province": "İzmir",         "region7": "Ege"},
    {"code": "TR-43", "province": "Kütahya",       "region7": "Ege"},
    {"code": "TR-45", "province": "Manisa",        "region7": "Ege"},
    {"code": "TR-48", "province": "Muğla",         "region7": "Ege"},
    {"code": "TR-64", "province": "Uşak",          "region7": "Ege"},

    # Marmara
    {"code": "TR-10", "province": "Balıkesir",     "region7": "Marmara"},
    {"code": "TR-11", "province": "Bilecik",       "region7": "Marmara"},
    {"code": "TR-16", "province": "Bursa",         "region7": "Marmara"},
    {"code": "TR-17", "province": "Çanakkale",     "region7": "Marmara"},
    {"code": "TR-22", "province": "Edirne",        "region7": "Marmara"},
    {"code": "TR-34", "province": "İstanbul",      "region7": "Marmara"},
    {"code": "TR-39", "province": "Kırklareli",    "region7": "Marmara"},
    {"code": "TR-41", "province": "Kocaeli",       "region7": "Marmara"},
    {"code": "TR-54", "province": "Sakarya",       "region7": "Marmara"},
    {"code": "TR-59", "province": "Tekirdağ",      "region7": "Marmara"},
    {"code": "TR-77", "province": "Yalova",        "region7": "Marmara"},

    # İç Anadolu
    {"code": "TR-06", "province": "Ankara",        "region7": "İç Anadolu"},
    {"code": "TR-18", "province": "Çankırı",       "region7": "İç Anadolu"},
    {"code": "TR-26", "province": "Eskişehir",     "region7": "İç Anadolu"},
    {"code": "TR-38", "province": "Kayseri",       "region7": "İç Anadolu"},
    {"code": "TR-40", "province": "Kırşehir",      "region7": "İç Anadolu"},
    {"code": "TR-42", "province": "Konya",         "region7": "İç Anadolu"},
    {"code": "TR-50", "province": "Nevşehir",      "region7": "İç Anadolu"},
    {"code": "TR-51", "province": "Niğde",         "region7": "İç Anadolu"},
    {"code": "TR-58", "province": "Sivas",         "region7": "İç Anadolu"},
    {"code": "TR-66", "province": "Yozgat",        "region7": "İç Anadolu"},
    {"code": "TR-68", "province": "Aksaray",       "region7": "İç Anadolu"},
    {"code": "TR-70", "province": "Karaman",       "region7": "İç Anadolu"},
    {"code": "TR-71", "province": "Kırıkkale",     "region7": "İç Anadolu"},

    # Karadeniz
    {"code": "TR-05", "province": "Amasya",        "region7": "Karadeniz"},
    {"code": "TR-14", "province": "Bolu",          "region7": "Karadeniz"},
    {"code": "TR-19", "province": "Çorum",         "region7": "Karadeniz"},
    {"code": "TR-28", "province": "Giresun",       "region7": "Karadeniz"},
    {"code": "TR-29", "province": "Gümüşhane",     "region7": "Karadeniz"},
    {"code": "TR-37", "province": "Kastamonu",     "region7": "Karadeniz"},
    {"code": "TR-52", "province": "Ordu",          "region7": "Karadeniz"},
    {"code": "TR-53", "province": "Rize",          "region7": "Karadeniz"},
    {"code": "TR-55", "province": "Samsun",        "region7": "Karadeniz"},
    {"code": "TR-57", "province": "Sinop",         "region7": "Karadeniz"},
    {"code": "TR-60", "province": "Tokat",         "region7": "Karadeniz"},
    {"code": "TR-61", "province": "Trabzon",       "region7": "Karadeniz"},
    {"code": "TR-67", "province": "Zonguldak",     "region7": "Karadeniz"},
    {"code": "TR-74", "province": "Bartın",        "region7": "Karadeniz"},
    {"code": "TR-78", "province": "Karabük",       "region7": "Karadeniz"},
    {"code": "TR-81", "province": "Düzce",         "region7": "Karadeniz"},
    {"code": "TR-08", "province": "Artvin",        "region7": "Karadeniz"},
    {"code": "TR-10", "province": "Balıkesir",     "region7": "Marmara"},  # Zaten yukarıda

    # Doğu Anadolu
    {"code": "TR-04", "province": "Ağrı",          "region7": "Doğu Anadolu"},
    {"code": "TR-12", "province": "Bingöl",        "region7": "Doğu Anadolu"},
    {"code": "TR-13", "province": "Bitlis",        "region7": "Doğu Anadolu"},
    {"code": "TR-23", "province": "Elazığ",        "region7": "Doğu Anadolu"},
    {"code": "TR-24", "province": "Erzincan",      "region7": "Doğu Anadolu"},
    {"code": "TR-25", "province": "Erzurum",       "region7": "Doğu Anadolu"},
    {"code": "TR-30", "province": "Hakkâri",       "region7": "Doğu Anadolu"},
    {"code": "TR-36", "province": "Kars",          "region7": "Doğu Anadolu"},
    {"code": "TR-44", "province": "Malatya",       "region7": "Doğu Anadolu"},
    {"code": "TR-49", "province": "Muş",           "region7": "Doğu Anadolu"},
    {"code": "TR-62", "province": "Tunceli",       "region7": "Doğu Anadolu"},
    {"code": "TR-65", "province": "Van",           "region7": "Doğu Anadolu"},
    {"code": "TR-75", "province": "Ardahan",       "region7": "Doğu Anadolu"},
    {"code": "TR-76", "province": "Iğdır",         "region7": "Doğu Anadolu"},
    {"code": "TR-79", "province": "Kilis",         "region7": "Güneydoğu Anadolu"},  # sınır ama GDA

    # Güneydoğu Anadolu
    {"code": "TR-02", "province": "Adıyaman",      "region7": "Güneydoğu Anadolu"},
    {"code": "TR-21", "province": "Diyarbakır",    "region7": "Güneydoğu Anadolu"},
    {"code": "TR-27", "province": "Gaziantep",     "region7": "Güneydoğu Anadolu"},
    {"code": "TR-47", "province": "Mardin",        "region7": "Güneydoğu Anadolu"},
    {"code": "TR-56", "province": "Siirt",         "region7": "Güneydoğu Anadolu"},
    {"code": "TR-63", "province": "Şanlıurfa",     "region7": "Güneydoğu Anadolu"},
    {"code": "TR-72", "province": "Batman",        "region7": "Güneydoğu Anadolu"},
    {"code": "TR-73", "province": "Şırnak",        "region7": "Güneydoğu Anadolu"},
]

# Bazı iller yukarıda iki kez görünebilir (ör: Balıkesir), bunu merge ederken uniq alacağız.


KW_LIST = ["anksiyete", "uykusuzluk", "stres", "panik atak", "mide yanması"]
TIMEFRAME = "2018-01-01 2025-11-30"


def collect_trends_provinces(out_file="google_trends_province_timeseries.csv"):
    """
    Her il (ISO code = TR-xx) için Google Trends zaman serisi çeker
    ve tek bir CSV'de toplar.
    """
    print("[INFO] Google Trends oturumu açılıyor...")
    pytrends = TrendReq(hl="tr-TR", tz=180)

    all_dfs = []

    # Province listesi DataFrame'e dönsün (tekrarları da temizleriz)
    provinces_df = pd.DataFrame(PROVINCES).drop_duplicates(subset=["code"])

    for _, row in provinces_df.iterrows():
        code = row["code"]
        province = row["province"]
        region7 = row["region7"]

        print(f"[INFO] Çekiliyor: {province} ({code}) - Bölge: {region7}")

        try:
            pytrends.build_payload(
                kw_list=KW_LIST,
                geo=code,          # kritik nokta: TR-xx formatı
                timeframe=TIMEFRAME
            )

            iot = pytrends.interest_over_time().reset_index()

            if iot.empty:
                print(f"  [WARN] {province} için boş veri döndü, atlanıyor.")
                continue

            if "isPartial" in iot.columns:
                iot = iot.drop(columns=["isPartial"])

            iot["province_code"] = code
            iot["province"] = province
            iot["region7"] = region7

            all_dfs.append(iot)

            # Google'a çok yüklenmemek için ufak bekleme
            time.sleep(1)

        except Exception as e:
            print(f"  [ERROR] {province} ({code}) için hata: {e}")

    if not all_dfs:
        print("[ERROR] Hiç veri toplanamadı.")
        return

    result = pd.concat(all_dfs, ignore_index=True)

    # Çıktıyı kaydet
    result.to_csv(out_file, index=False)
    print(f"[OK] İl bazlı Google Trends zaman serileri '{out_file}' dosyasına kaydedildi.")
    print(result.head())


if __name__ == "__main__":
    collect_trends_provinces()
