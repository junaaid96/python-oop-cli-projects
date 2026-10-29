"""Pure functions are trivial to test: data in, data out."""

from pathlib import Path

import pytest
from log_analyzer.cli import main
from log_analyzer.pipeline import (
    all_of,
    compose,
    parse,
    path_startswith,
    status_at_least,
    summary,
    where,
)

LOG = """\
2026-10-30T10:00:00 GET /home 200 10ms
2026-10-30T10:00:01 GET /api/users 500 300ms
garbage line
2026-10-30T10:00:02 POST /api/users 201 50ms
2026-10-30T10:00:03 GET /api/items 404 20ms
""".splitlines()


def test_parse_skips_bad_lines() -> None:
    assert len(list(parse(LOG))) == 4


def test_pipeline() -> None:
    api_errors = compose(where(all_of(path_startswith("/api"), status_at_least(400))))
    assert [e.status for e in api_errors(parse(LOG))] == [500, 404]


def test_summary() -> None:
    s = summary(parse(LOG))
    assert s["requests"] == 4
    assert s["statuses"] == {200: 1, 201: 1, 404: 1, 500: 1}
    assert s["top_paths"] == [("/api/users", 2), ("/home", 1), ("/api/items", 1)]


def test_cli(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    f = tmp_path / "a.log"
    f.write_text("\n".join(LOG))
    assert main([str(f), "--errors"]) == 0
    assert "requests   2" in capsys.readouterr().out
    assert main([str(tmp_path / "nope.log")]) == 1
