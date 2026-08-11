import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

import pandas as pd
from gate import apply_gating, summarize_populations


def make_tests_df():
    return pd.DataFrame({
        "Aqua Amine FLR-A": [0.5, 3.0, 0.2, 0.1, 0.8],
        "CD3 APC-H7 FLR-A": [3.0, 3.0, 0.5, 3.0, 3.0],
        "CD4 PE-Cy7 FLR-A": [4.0, 4.0, 0.5, 0.5, 4.0],
        "CD8 PerCP-Cy55 FLR-A": [0.5, 0.5, 0.5, 4.0, 4.0],
    })


def test_apply_gating_assigns_correct_populations():
    df = make_tests_df()
    result = apply_gating(
        df,
        viability_channel="Aqua Amine FLR-A", viability_threshold=1.3,
        lineage_channel="CD3 APC-H7 FLR-A", lineage_threshold=1.75,
        cd4_channel="CD4 PE-Cy7 FLR-A", cd4_threshold=2.4,
        cd8_channel="CD8 PerCP-Cy55 FLR-A", cd8_threshold=3.15,
    )
    expected = [
        "CD4_T_cell",
        "dead",
        "live_non_T_cell",
        "CD8_T_cell",
        "double_positive_T_cell",
    ]
    assert result["population"].tolist() == expected


def test_summarize_populations_counts_correctly():
    df = make_tests_df()
    df["population"] = ["CD4_T_cell", "dead", "live_non_T_cell", "CD8_T_cell", "double_positive_T_cell"]
    summary = summarize_populations(df, sample_name="test_sample")
    assert summary["total_events"] == 5
    assert summary["population_counts"]["dead"] == 1
    assert summary["population_percentages"]["dead"] == 20.0