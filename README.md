# Immune Profiling Pipeline

A modular, production-style data pipeline for processing flow cytometry (FCS) data —
built to demonstrate bioinformatics engineering practices applied to immune profiling data,
the kind used in clinical trial biomarker analysis.

## Status
🚧 In progress

## Pipeline overview

```text
FCS files (raw)
        ↓
QC & Validation
        ↓
Compensation & Transformation
        ↓
Population Identification
        ↓
Structured Output
        ↓
Automatic Report
        ↓
Cloud Upload
```

## Why rule-based gating
Clinical trial data pipelines need auditable, reproducible logic over black-box predictions.
This project prioritizes deterministic, testable population identification over ML-based
approaches — matching how a production bioinformatics pipeline would actually be built.

## Tech stack
- **Orchestration:** Snakemake
- **Data processing:** Python, pandas, fcsparser
- **Testing:** pytest
- **Storage:** Parquet / SQLite
- **Cloud:** AWS S3 (boto3)
- **CI:** GitHub Actions (planned)

## Project structure
workflow/ Snakemake rule files, one per pipeline stage
scripts/ Python logic called by each rule
config/ YAML configuration (paths, parameters)
tests/ pytest test suite
data/ raw + processed FCS data (gitignored)
reports/ generated QC/summary reports (gitignored)

## Setup
\`\`\`bash
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\Activate.ps1 on Windows
pip install -r requirements.txt
\`\`\`