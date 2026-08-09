rule qc_validate:
    input:
        fcs = lambda wc: f"{config['paths']['raw_dir']}/{wc.sample}.fcs"
    output:
        json = f"{config['paths']['processed_dir']}/{{sample}}_qc.json"
    script:
        "../../scripts/qc.py"