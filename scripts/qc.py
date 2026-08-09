import json
import fcsparser

input_fcs = snakemake.input.fcs
output_json = snakemake.output.json
sample_name = snakemake.wildcards.sample

meta, data = fcsparser.parse(input_fcs, reformat_meta=True)

expected_channels = [
    "FSC-A", "FSC-H", "FSC-W",
    "SSC-A", "SSC-H", "SSC-W",
    "TNFa FITC FLR-A", "CD8 PerCP-Cy55 FLR-A", "IL2 BV421 FLR-A",
    "Aqua Amine FLR-A", "IFNg APC FLR-A", "CD3 APC-H7 FLR-A",
    "CD107a PE FLR-A", "CD4 PE-Cy7 FLR-A", "Time"
]

actual_channels = list(data.columns)

event_count = data.shape[0]
min_events_threshold = 10000
even_count_ok = event_count >= min_events_threshold

missing_channels = [ch for ch in expected_channels if ch not in actual_channels]
channels_ok = len(missing_channels) == 0

constant_channels = [col for col in data.columns if data[col].nunique() <= 1]
no_constant_channels = len(constant_channels) == 0

overall_pass = even_count_ok and channels_ok and no_constant_channels

qc_results = {
    "sample": sample_name,
    "event_count": event_count,
    "event_count_ok": even_count_ok,
    "channels_ok": channels_ok,
    "missing_channels": missing_channels,
    "no_constant_channels": no_constant_channels,
    "constant_channels": constant_channels,
    "overall_pass": overall_pass
}

with open(output_json, "w") as f:
    json.dump(qc_results, f, indent=2)
