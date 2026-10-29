"""The shortener depends on the LinkStore *protocol*, not a concrete database."""

from __future__ import annotations

import re
from datetime import datetime, timedelta
from urllib.parse import urlparse

from url_shortener.codec import encode
from url_shortener.storage import Link, LinkStore, with_click

ALIAS = re.compile(r"^[A-Za-z0-9_-]{3,30}$")


class ShortenerError(Exception):
    pass


class Shortener:
    def __init__(self, store: LinkStore, base_url: str = "https://sho.rt/") -> None:
        self.store = store
        self.base_url = base_url

    @staticmethod
    def validate(url: str) -> str:
        parts = urlparse(url)
        if parts.scheme not in {"http", "https"} or not parts.netloc:
            raise ShortenerError(f"not a valid http(s) URL: {url!r}")
        return url

    def shorten(
        self,
        url: str,
        *,
        alias: str | None = None,
        ttl_days: int | None = None,
        now: datetime | None = None,
    ) -> Link:
        now = now or datetime.now()
        new_id = self.store.next_id()
        code = alias or encode(new_id + 3843)  # offset so codes start at 3 characters
        if alias and not ALIAS.match(alias):
            raise ShortenerError("alias must be 3-30 letters, digits, _ or -")
        if self.store.by_code(code):
            raise ShortenerError(f"code {code!r} is taken")
        expires = now + timedelta(days=ttl_days) if ttl_days else None
        link = Link(new_id, self.validate(url), code, now, expires)
        self.store.save(link)
        return link

    def resolve(self, code: str, now: datetime | None = None) -> str:
        link = self.store.by_code(code)
        if link is None:
            raise ShortenerError(f"unknown code {code!r}")
        if link.expires and (now or datetime.now()) > link.expires:
            raise ShortenerError(f"link {code!r} has expired")
        self.store.save(with_click(link))
        return link.url

    def stats(self) -> list[Link]:
        return sorted(self.store.all(), key=lambda link: link.clicks, reverse=True)
