rule gate_populations:
    input:
        parquet = f"{config['paths']['processed_dir']}/{{sample}}_compensated.parquet"
    output:
        parquet = f"{config['paths']['processed_dir']}/{{sample}}_gated.parquet",
        summary = f"{config['paths']['processed_dir']}/{{sample}}_population_summary.json"
    script:
        "../../scripts/gate.py"