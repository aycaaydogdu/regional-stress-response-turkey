import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def load_panel(panel_file="event_region_stress_panel.csv"):
    df = pd.read_csv(panel_file)
    df["event_date"] = pd.to_datetime(df["event_date"])
    return df


def plot_delta_stress_by_region(df):
    plt.figure(figsize=(12, 6))
    sns.boxplot(data=df, x="region7", y="delta_stress")
    plt.axhline(0, color="black", linestyle="--", linewidth=1)
    plt.title("Delta Stress (Post – Pre) by Region")
    plt.ylabel("Δ Stress Index")
    plt.xlabel("Region")
    plt.tight_layout()
    plt.show()


def plot_delta_stress_bar(df):
    region_avg = df.groupby("region7")["delta_stress"].mean().reset_index()

    plt.figure(figsize=(10, 5))
    sns.barplot(data=region_avg, x="region7", y="delta_stress")
    plt.axhline(0, color="black", linestyle="--")
    plt.title("Average Δ Stress Response by Region")
    plt.ylabel("Mean Δ Stress")
    plt.xlabel("Region")
    plt.tight_layout()
    plt.show()


def plot_event_timeline(df):
    plt.figure(figsize=(14, 4))
    plt.scatter(df["event_date"], df["delta_stress"], c="red", alpha=0.7)
    plt.axhline(0, color="black", linestyle="--")

    for _, row in df.iterrows():
        plt.text(row["event_date"], row["delta_stress"],
                 row["event_type"], fontsize=8, alpha=0.6)

    plt.title("Event Timeline with Δ Stress")
    plt.ylabel("Δ Stress")
    plt.xlabel("Event Date")
    plt.tight_layout()
    plt.show()


def plot_fx_vs_quake(df):
    plt.figure(figsize=(8, 5))
    sns.boxplot(data=df, x="event_type", y="delta_stress")
    plt.title("Δ Stress: Earthquakes vs FX Shocks")
    plt.axhline(0, color="black", linestyle="--")
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    df = load_panel()

    plot_delta_stress_by_region(df)
    plot_delta_stress_bar(df)
    plot_event_timeline(df)
    plot_fx_vs_quake(df)
