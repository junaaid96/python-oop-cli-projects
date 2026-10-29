"""The same behaviour tests run against BOTH storage backends (parametrized fixture)."""

from datetime import datetime, timedelta
from pathlib import Path

import pytest
from url_shortener.cli import main
from url_shortener.codec import decode, encode
from url_shortener.service import Shortener, ShortenerError
from url_shortener.storage import LinkStore, MemoryStore, SqliteStore


@pytest.mark.parametrize("n", [0, 1, 61, 62, 3843, 10**9])
def test_codec_roundtrip(n: int) -> None:
    assert decode(encode(n)) == n


@pytest.fixture(params=["memory", "sqlite"])
def app(request: pytest.FixtureRequest) -> Shortener:
    store: LinkStore = MemoryStore() if request.param == "memory" else SqliteStore(":memory:")
    return Shortener(store)


def test_shorten_resolve_stats(app: Shortener) -> None:
    a = app.shorten("https://example.com/a")
    assert len(a.code) == 3
    app.shorten("https://example.com/b", alias="docs")
    assert app.resolve("docs") == "https://example.com/b"
    app.resolve("docs")
    assert [(link.code, link.clicks) for link in app.stats()] == [("docs", 2), (a.code, 0)]


def test_errors(app: Shortener) -> None:
    with pytest.raises(ShortenerError):
        app.shorten("ftp://nope")
    app.shorten("https://x.io", alias="taken")
    with pytest.raises(ShortenerError, match="taken"):
        app.shorten("https://y.io", alias="taken")
    t0 = datetime(2026, 1, 1)
    app.shorten("https://z.io", alias="temp", ttl_days=1, now=t0)
    with pytest.raises(ShortenerError, match="expired"):
        app.resolve("temp", now=t0 + timedelta(days=2))


def test_cli(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    db = ["--db", str(tmp_path / "l.db")]
    assert main([*db, "shorten", "https://example.com", "--alias", "exa"]) == 0
    assert main([*db, "open", "exa"]) == 0
    assert main([*db, "open", "missing"]) == 1
    assert "https://sho.rt/exa" in capsys.readouterr().out
