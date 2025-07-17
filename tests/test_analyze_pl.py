# Test suite
# test_analyze_pl.py
# Author : Saad Khan

import subprocess
from pathlib import Path

def test_analyze_pl_summary(tmp_path):
    # I am creating temporary log file with known content
    log_file = tmp_path / "diagnostics.log"
    log_file.write_text(
        "2025-07-16T12:00:00 | Ticket #101 | 8.8.8.8 | SUCCESS\n"
        "2025-07-16T12:05:00 | Ticket #102 | 1.1.1.1 | FAIL\n"
    )

    # Now i will run the Perl script, passing my temp log file
    result = subprocess.run(
        ["perl", "src/analyze.pl", str(log_file)],
        capture_output=True,
        text=True,
        cwd=Path(__file__).resolve().parent.parent  # project root
    )

    # assertions on output
    assert result.returncode == 0, f"Perl script failed: {result.stderr}"
    output = result.stdout
    assert "Successful pings: 1" in output, "Should report 1 success"
    assert "Failed pings: 1" in output, "Should report 1 failure"