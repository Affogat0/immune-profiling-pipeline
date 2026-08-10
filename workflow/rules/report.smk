rule generate_report:
    input:
        qc_json = f"{config['paths']['processed_dir']}/{{sample}}_qc.json",
        summary_json = f"{config['paths']['processed_dir']}/{{sample}}_population_summary.json"
    output:
        html = f"{config['paths']['reports_dir']}/{{sample}}_qc_report.html"
    script:
        "../../scripts/report.py"