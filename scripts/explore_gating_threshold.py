"""
Exploratory script used to visualize marker distributions and determine
gating thresholds for the pipeline (see config/config.yaml gating section).
Not part of the automated pipeline: run manually when re-evaluating thresholds.
"""

import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_parquet("data/processed/101_DEN084Y5_15_E01_008_clean_compensated.parquet")

fig, axes = plt.subplots(2, 2, figsize=(10, 8))

axes[0, 0].hist(df["Aqua Amine FLR-A"], bins=200)
axes[0, 0].set_title("Aqua Amine (viability)")

axes[0, 1].hist(df["CD3 APC-H7 FLR-A"], bins=200)
axes[0, 1].set_title("CD3")

axes[1, 0].hist(df["CD4 PE-Cy7 FLR-A"], bins=200)
axes[1, 0].set_title("CD4")

axes[1, 1].hist(df["CD8 PerCP-Cy55 FLR-A"], bins=200)
axes[1, 1].set_title("CD8")

plt.tight_layout()
plt.savefig("scripts/exploration_histograms.png")
print("Saved to scripts/exploration_histograms.png")