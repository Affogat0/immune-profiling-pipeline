import boto3

input_html = snakemake.input.html
output_marker = snakemake.output.marker
sample_name = snakemake.wildcards.sample

bucket_name = snakemake.config["s3"]["bucket_name"]

s3 = boto3.client("s3")

s3_key = f"reports/{sample_name}_qc_report.html"

s3.upload_file(input_html, bucket_name, s3_key)

with open(output_marker, "w") as f:
    f.write(f"Uploaded to s3://{bucket_name}/{s3_key}\n")