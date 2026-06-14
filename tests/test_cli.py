import pytest
from pathlib import Path
from pilepack.cli import main, _stream_report
import sys
from io import StringIO

def test_stream_report_no_content(test_project):
    stream = StringIO()
    _stream_report(test_project, stream, include_content=False, fmt="txt")
    output = stream.getvalue()
    assert "--- FILE:" not in output
    assert "test_project" in output
    assert "main.py" in output

def test_cli_basic(test_project, capsys, monkeypatch):
    monkeypatch.setattr(sys, "argv", ["pilepack", str(test_project), "--no-content"])
    main()
    captured = capsys.readouterr()
    assert "test_project" in captured.out
    assert "main.py" in captured.out
    assert "--- FILE:" not in captured.out

def test_cli_output_file(test_project, tmp_path, monkeypatch):
    out_file = tmp_path / "report.txt"
    monkeypatch.setattr(sys, "argv", ["pilepack", str(test_project), "-o", str(out_file)])
    main()
    assert out_file.exists()
    content = out_file.read_text()
    assert "main.py" in content

def test_cli_follow_symlinks_flag(test_project, tmp_path, monkeypatch, capsys):
    outside_file = tmp_path / "outside.txt"
    outside_file.write_text("outside")
    link = test_project / "linked-outside.txt"
    try:
        link.symlink_to(outside_file)
    except (NotImplementedError, OSError) as exc:
        pytest.skip(f"symlinks are not supported here: {exc}")

    monkeypatch.setattr(sys, "argv", ["pilepack", str(test_project), "--no-content", "--follow-symlinks"])
    main()

    captured = capsys.readouterr()

    assert "linked-outside.txt" in captured.out

def test_cli_invalid_dir(capsys, monkeypatch):
    monkeypatch.setattr(sys, "argv", ["pilepack", "/nonexistent"])
    with pytest.raises(SystemExit):
        main()
    captured = capsys.readouterr()
    assert "not a valid directory" in captured.err
