# 09 · Files, Paths and JSON

```python
import json
from pathlib import Path

data_dir = Path.home() / ".python-oop-cli"  # `/` joins paths on every OS
data_dir.mkdir(parents=True, exist_ok=True)
path = data_dir / "contacts.json"

path.write_text(json.dumps({"name": "Ana"}, indent=2), encoding="utf-8")
loaded = json.loads(path.read_text(encoding="utf-8"))

for p in Path(".").glob("*.py"):  # rglob for recursive
    print(p.name, p.suffix, p.stat().st_size)
```

## Tips
- Always pass `encoding="utf-8"`.
- Write to a temp file then `replace()` it for crash-safe saves.
- JSON has no dates/Decimals: convert with `isoformat()` / `str()` and back.
- `csv.DictReader`/`DictWriter` for spreadsheets; `tomllib` for reading TOML.
- In tests, use pytest's `tmp_path` fixture. Never touch real user files.

**See it in:** 01 Contact Book, 03 Todo, 05 File Organizer, 15 Text Adventure (save games).
