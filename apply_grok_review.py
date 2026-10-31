"""Apply context-specific Grok review fixes to the regional raw import dialog.

Run after any regional catalog regeneration. This intentionally touches only
known gettext message keys and preserves the rest of each catalog verbatim.
"""
import hashlib
import json
from pathlib import Path
import polib

ROOT = Path(__file__).resolve().parent
HEADERS = {
    '_Each image row skip': {'zh_HK': '每個圖像列跳過(_E)', 'zh_TW': '每個影像列略過(_E)'},
    'E_xtract column': {'zh_HK': '提取欄(_X)', 'zh_TW': '擷取欄(_X)'},
    'After each _row skip': {'zh_HK': '每列之後跳過(_R)', 'zh_TW': '每列之後略過(_R)'},
}
ERRORS = {
    "Expected whitespace to skip more fields in row %u, got `%.16s'",
    "Expected `%c' to skip more fields in row %u, got `%.16s'",
    "Expected `%s' to skip more fields in row %u, got `%.16s'",
    "Garbage `%.16s' in row %u, column %u",
    "Expected delimiter `%c' after data in row %u, column %u, got `%c'",
    "Expected delimiter `%s' after data in row %u, column %u, got `%.16s'",
}

def update(path, locale):
    original = path.read_bytes()
    digest = hashlib.sha256(original).digest()
    text = original.decode('utf-8')
    if '\r' in text:
        raise SystemExit(f'{path}: unexpected CRLF; refusing to rewrite')
    blocks = text.split('\n\n')
    seen = set()
    changes = 0
    for index, block in enumerate(blocks):
        if 'modules/file/rawfile.c:' not in block:
            continue
        parsed = polib.pofile(block)
        if len(parsed) != 1:
            continue
        entry = parsed[0]
        msgid = entry.msgid
        if msgid not in HEADERS and msgid not in ERRORS:
            continue
        if msgid in seen:
            raise SystemExit(f'{path}: duplicate {msgid!r}')
        seen.add(msgid)
        old = entry.msgstr
        if msgid in HEADERS:
            new = HEADERS[msgid][locale]
        else:
            new = old.replace('第 %u 行第 %u 列', '第 %u 列第 %u 欄').replace('第 %u 行', '第 %u 列')
        if old == new:
            continue
        oldline = 'msgstr ' + json.dumps(old, ensure_ascii=False)
        newline = 'msgstr ' + json.dumps(new, ensure_ascii=False)
        if block.count(oldline) != 1:
            raise SystemExit(f'{path}: translation is not a unique single-line entry: {msgid!r}')
        blocks[index] = block.replace(oldline, newline, 1)
        changes += 1
    missing = set(HEADERS) | ERRORS
    missing -= seen
    if missing:
        raise SystemExit(f'{path}: missing expected entries: {missing!r}')
    if hashlib.sha256(path.read_bytes()).digest() != digest:
        raise SystemExit(f'{path}: file changed during review; retry safely')
    if changes:
        path.write_bytes('\n\n'.join(blocks).encode('utf-8'))
    print(f'{path.name}: {changes} translations corrected')

for lang in ('zh_HK', 'zh_TW'):
    update(ROOT / 'translations' / f'{lang}.po', lang)
