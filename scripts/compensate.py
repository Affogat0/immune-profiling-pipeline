import json
import numpy as np
import pandas as pd
import fcsparser

input_fcs = snakemake.input.fcs
comp_matrix_path = snakemake.input.comp_matrix
qc_json_path = snakemake.input.qc_json
output_parquet = snakemake.output.parquet

with open(qc_json_path) as f:
    qc_results = json.load(f)

if not qc_results["overall_pass"]:
    raise ValueError(f"Sample failed QC, refusing to compensate: {qc_results}")

meta, data = fcsparser.parse(input_fcs, reformat_meta=True)

comp_df = pd.read_csv(comp_matrix_path, comment="#", header=None)
comp_channels = pd.read_csv(comp_matrix_path, nrows=0).columns.tolist()
comp_channels = [c.lstrip("# ").strip() for c in comp_channels]

fluor_data = data[comp_channels].to_numpy()
comp_matrix = comp_df.to_numpy()
comp_matrix_inv = np.linalg.inv(comp_matrix)
compensated = fluor_data @ comp_matrix_inv

cofactor = snakemake.config["transform"]["cofactor"]
transformed = np.arcsinh(compensated / cofactor)

transformed_df = pd.DataFrame(transformed, columns=comp_channels)

non_fluor_channels = [c for c in data.columns if c not in comp_channels]
final_df = pd.concat([data[non_fluor_channels].reset_index(drop=True), transformed_df], axis=1)

final_df.to_parquet(output_parquet, index=False)
