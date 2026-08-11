import json
import pandas as pd
import numpy as np

def apply_gating(df, viability_channel, viability_threshold, lineage_channel,lineage_threshold,cd4_channel, cd4_threshold,cd8_channel, cd8_threshold):


    df = df.copy()
    df["is_live"] = df[viability_channel] < viability_threshold
    df["is_cd3_pos"] = df[lineage_channel] > lineage_threshold
    df["is_cd4_pos"] = df[cd4_channel] > cd4_threshold
    df["is_cd8_pos"] = df[cd8_channel] > cd8_threshold

    conditions = [
        ~df["is_live"],
        df["is_live"] & ~df["is_cd3_pos"],
        df["is_live"] & df["is_cd3_pos"] & df["is_cd4_pos"] & ~df["is_cd8_pos"],
        df["is_live"] & df["is_cd3_pos"] & df["is_cd8_pos"] & ~df["is_cd4_pos"],
        df["is_live"] & df["is_cd3_pos"] & df["is_cd4_pos"] & df["is_cd8_pos"],
    ]

    choices = [
        "dead",
        "live_non_T_cell",
        "CD4_T_cell",
        "CD8_T_cell",
        "double_positive_T_cell",
    ]

    df["population"] = np.select(conditions, choices, default="double_negative_T_cell")
    return df

def summarize_populations(df, sample_name):
    population_counts = df["population"].value_counts().to_dict()
    total_events = len(df)

    return {
        "sample": sample_name,
        "total_events": total_events,
        "population_counts": population_counts,
        "population_percentages": {
            pop: round(count / total_events*100,2)
            for pop, count in population_counts.items()
        }
    }


if __name__ == "__main__":
    input_parquet = snakemake.input.parquet
    output_parquet = snakemake.output.parquet
    output_summary = snakemake.output.summary
    sample_name = snakemake.wildcards.sample

    df = pd.read_parquet(input_parquet)

    gating_config = snakemake.config["gating"]
    df = apply_gating(
        df,
        gating_config["viability_channel"], gating_config["viability_threshold"],
        gating_config["lineage_channel"], gating_config["lineage_threshold"],
        gating_config["cd4_channel"], gating_config["cd4_threshold"],
        gating_config["cd8_channel"], gating_config["cd8_threshold"],
    )

    population_summary = summarize_populations(df, sample_name)

    df.to_parquet(output_parquet, index=False)

    with open(output_summary, "w") as f:
        json.dump(population_summary, f, indent=2)