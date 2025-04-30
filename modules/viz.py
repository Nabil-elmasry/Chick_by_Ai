
# modules/viz.py

import matplotlib.pyplot as plt

def plot_sensor_deviations(df, stats_df):
    figures = []
    for col in df.columns:
        if col not in stats_df['feature'].values:
            continue

        actual_values = df[col].dropna()
        mean_val = stats_df[stats_df['feature'] == col]['mean'].values[0]
        std_val = stats_df[stats_df['feature'] == col]['std'].values[0]

        fig, ax = plt.subplots(figsize=(6, 4))
        ax.plot(actual_values, label='Actual', color='blue')
        ax.axhline(mean_val, color='green', linestyle='--', label='Mean')
        ax.axhline(mean_val + std_val, color='orange', linestyle=':', label='Mean + 1 STD')
        ax.axhline(mean_val - std_val, color='orange', linestyle=':', label='Mean - 1 STD')

        ax.set_title(f"Deviation of {col}")
        ax.set_xlabel("الزمن / العينات")
        ax.set_ylabel("القيمة")
        ax.legend()
        figures.append(fig)

    return figures

