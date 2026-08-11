![Tests](https://github.com/Affogat0/immune-profiling-pipeline/actions/workflows/test.yml/badge.svg)

# Immune Profiling Pipeline

A modular, production-style data pipeline for processing flow cytometry (FCS) data —
built to demonstrate bioinformatics engineering practices applied to immune profiling data,
the kind used in clinical trial biomarker analysis.

## Status
Core pipeline complete (QC → compensation/transform → gating → report → S3 upload), tested, CI passing

## Data
This pipeline uses 3 FCS files from an 8-color ICS panel (FlowKit's example dataset).
Raw data is gitignored (not committed) since it's regenerable and shouldn't live in version control.
To fetch it:

\`\`\`bash
git clone --depth 1 https://github.com/whitews/FlowKit.git /tmp/flowkit-src
mkdir -p data/raw data/reference
cp /tmp/flowkit-src/data/8_color_data_set/fcs_files/*.fcs data/raw/
cp /tmp/flowkit-src/data/8_color_data_set/den_comp.csv data/reference/
\`\`\`

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
Clinical trial data pipelines need auditable, reproducible logic over black box predictions.
This project prioritizes deterministic, testable population identification over ML-based
approaches, matching how a production bioinformatics pipeline would actually be built.

Gating thresholds (`config/config.yaml`) were chosen by visually inspecting marker distribution
histograms for this specific dataset (see `scripts/explore_gating_thresholds.py`) and placing
gates at the valley between populations. This
method has known limitations worth being explicit about:
- **Dataset-specific**: thresholds may need to be tuned again for samples with different staining intensity.
- **Operator-dependent**: manual valley placement can vary between analysts, a wellknown source
  of inter-operator variability in the field.
- **No FMO control available**: an FMO (Fluorescence-Minus-One) control sample would give a more
  objective negative population boundary, however this dataset didn't include one.

A natural extension would be algorithmic valley detection (e.g. `scipy.signal.find_peaks` on
inverted density) to make threshold selection reproducible rather than manual.

## Tech stack
- **Orchestration:** Snakemake
- **Data processing:** Python, pandas, fcsparser
- **Testing:** pytest
- **Storage:** Parquet / SQLite
- **Cloud:** AWS S3 (boto3)
- **CI:** GitHub Actions - runs pytest on every push (see badge above)

## Cloud Storage
Reports are uploaded to a private S3 bucket after generation. Access uses IAM credentials
configured locally via `aws configure` (never committed to this repo). The current IAM user
has broad S3 permissions (`AmazonS3FullAccess`) for simplicity; a more security-conscious
follow-up would scope this down to a custom policy limited to just this project's bucket,
following the principle of least privilege.

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