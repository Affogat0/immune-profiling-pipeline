rule compensate_transform:
    input:
        fcs = lambda wc: f"{config['paths']['raw_dir']}/{wc.sample}.fcs",
        comp_matrix = config["compensation_matrix"],
        qc_json = f"{config['paths']['processed_dir']}/{{sample}}_qc.json"
    output:
        parquet = f"{config['paths']['processed_dir']}/{{sample}}_compensated.parquet"
    script:
        "../../scripts/compensate.py"