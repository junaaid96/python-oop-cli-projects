"""`url-shortener shorten|open|stats`"""

import argparse
from collections.abc import Sequence
from pathlib import Path

from url_shortener.service import Shortener, ShortenerError
from url_shortener.storage import SqliteStore

DEFAULT_DB = Path.home() / ".python-oop-cli" / "links.db"


def main(argv: Sequence[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="url-shortener")
    p.add_argument("--db", type=Path, default=DEFAULT_DB)
    sub = p.add_subparsers(dest="command", required=True)
    s = sub.add_parser("shorten")
    s.add_argument("url")
    s.add_argument("--alias")
    s.add_argument("--ttl-days", type=int)
    sub.add_parser("open", help="resolve a code (counts a click)").add_argument("code")
    sub.add_parser("stats")
    args = p.parse_args(argv)

    args.db.parent.mkdir(parents=True, exist_ok=True)
    app = Shortener(SqliteStore(args.db))
    try:
        if args.command == "shorten":
            link = app.shorten(args.url, alias=args.alias, ttl_days=args.ttl_days)
            print(f"{app.base_url}{link.code}")
        elif args.command == "open":
            print(app.resolve(args.code))
        else:
            for link in app.stats():
                print(f"{link.code:<10} {link.clicks:>5} clicks  {link.url}")
    except ShortenerError as err:
        print(f"Error: {err}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
