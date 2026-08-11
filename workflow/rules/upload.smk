rule upload_to_s3:
    input:
        html = f"{config['paths']['reports_dir']}/{{sample}}_qc_report.html"
    output:
        marker = f"{config['paths']['reports_dir']}/{{sample}}_upload.done"
    script:
        "../../scripts/upload.py"