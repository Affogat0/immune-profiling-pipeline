import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

import pandas as pd
from qc import run_qc_checks


def make_good_df():
    return pd.DataFrame({
        "FSC-A": range(15000),
        "SSC-A": range(15000),
        "CD3 APC-H7 FLR-A": range(15000),
    })


def test_passes_when_everything_is_fine():
    df = make_good_df()
    result = run_qc_checks(df, expected_channels=["FSC-A", "SSC-A", "CD3 APC-H7 FLR-A"])

    assert result["overall_pass"] is True
    assert result["event_count_ok"] is True
    assert result["channels_ok"] is True
    assert result["no_constant_channels"] is True


def test_fails_on_too_few_events():
    df = make_good_df().head(500)
    result = run_qc_checks(df, expected_channels=["FSC-A", "SSC-A", "CD3 APC-H7 FLR-A"])

    assert result["event_count_ok"] is False
    assert result["overall_pass"] is False


def test_fails_on_missing_channel():
    df = make_good_df()
    result = run_qc_checks(df, expected_channels=["FSC-A", "SSC-A", "CD3 APC-H7 FLR-A", "CD4 PE-Cy7 FLR-A"])

    assert result["channels_ok"] is False
    assert "CD4 PE-Cy7 FLR-A" in result["missing_channels"]
    assert result["overall_pass"] is False


def test_fails_on_constant_channel():
    df = make_good_df()
    df["SSC-A"] = 0

    result = run_qc_checks(df, expected_channels=["FSC-A", "SSC-A", "CD3 APC-H7 FLR-A"])

    assert result["no_constant_channels"] is False
    assert "SSC-A" in result["constant_channels"]
    assert result["overall_pass"] is False