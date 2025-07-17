# Test suite
# test_diagnose.py
# Author : Saad Khan

from pathlib import Path
from src.diagnose import run_diagnostics

def test_diagnostics_creates_log(tmp_path, monkeypatch):

    import src.diagnose as diag
    diag.OUTPUT_DIR = tmp_path
    diag.OUTPUT_LOG = tmp_path / "diagnostics.log"

    run_diagnostics()

    log_file = tmp_path / "diagnostics.log"
    assert log_file.exists(), "diagnostics.log should be created"
    content = log_file.read_text()
    assert "Ticket #" in content, "Log should contain ticket entries"