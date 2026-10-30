"""Check returned gettext batches without treating draft translations as final."""
import re
import sys
from collections import Counter
from pathlib import Path

try:
    import polib
except ImportError:
    print("Install dependencies from requirements.txt to run this check.", file=sys.stderr)
    raise SystemExit(2)

ROOT = Path(__file__).resolve().parent
PRINTF = re.compile(r"%(?:\d+\$)?[-+ #0']*(?:\d+|\*(?:\d+\$)?)?(?:\.(?:\d+|\*(?:\d+\$)?))?(?:hh|ll|[hljztL])?[diouxXfFeEgGaAcspn%]")
GWY_FORMAT = re.compile(r"%\{[^{}]+\}[A-Za-z]")
TAGS = re.compile(r"</?[A-Za-z][^>]*>")


def key(e):
    return e.msgctxt, e.msgid, e.msgid_plural


def tokens(text):
    return Counter(PRINTF.findall(text)), Counter(GWY_FORMAT.findall(text)), Counter(TAGS.findall(text))


def check_batch(po_path):
    match = re.fullmatch(r'(codex|grok|deepseek)-(\d{3})-zh_CN\.po', po_path.name)
    if not match:
        return [f'{po_path}: invalid batch filename'], 0, 0
    template = ROOT / 'batches' / match[1] / f'{match[1]}-{match[2]}.pot'
    if not template.exists():
        return [f'{po_path}: missing matching template'], 0, 0
    try:
        src = polib.pofile(str(template), check_for_duplicates=True)
        out = polib.pofile(str(po_path), check_for_duplicates=True)
    except Exception as exc:
        return [f'{po_path}: invalid PO: {exc}'], 0, 0
    errors = []
    src_entries = {key(e): e for e in src}
    out_entries = {key(e): e for e in out}
    if src_entries.keys() != out_entries.keys():
        errors.append(f'{po_path.name}: missing {len(src_entries.keys() - out_entries.keys())}, unexpected {len(out_entries.keys() - src_entries.keys())}')
    if out.metadata.get('Language') != 'zh_CN':
        errors.append(f'{po_path.name}: expected Language: zh_CN')
    if re.sub(r'\s+', '', out.metadata.get('Plural-Forms', '')) != 'nplurals=1;plural=0;':
        errors.append(f'{po_path.name}: expected Chinese plural rule')
    if 'charset=UTF-8' not in out.metadata.get('Content-Type', ''):
        errors.append(f'{po_path.name}: expected UTF-8 charset')
    count = 0
    for k, entry in out_entries.items():
        original = src_entries.get(k)
        if original is None:
            continue
        if set(entry.flags) != set(original.flags):
            errors.append(f'{po_path.name}: flags changed for {entry.msgid!r}')
        variants = list(entry.msgstr_plural.values()) if entry.msgid_plural else [entry.msgstr]
        if entry.msgid_plural and set(entry.msgstr_plural) != {0}:
            errors.append(f'{po_path.name}: expected only msgstr[0] for {entry.msgid!r}')
        if 'fuzzy' not in entry.flags and variants and all(variants):
            count += 1
        for translation in variants:
            if not translation:
                continue
            # A plural translation may use either singular or plural placeholders.
            expected = [tokens(entry.msgid)]
            if entry.msgid_plural:
                expected.append(tokens(entry.msgid_plural))
            if tokens(translation) not in expected:
                errors.append(f'{po_path.name}: placeholders or tags differ for {entry.msgid!r}')
            if 'c-format' in entry.flags:
                source_orders = [PRINTF.findall(entry.msgid)]
                if entry.msgid_plural:
                    source_orders.append(PRINTF.findall(entry.msgid_plural))
                target_order = PRINTF.findall(translation)
                positional = target_order and all(re.match(r'%\d+\$', x) for x in target_order if x != '%%')
                if not positional and target_order not in source_orders:
                    errors.append(f'{po_path.name}: printf argument order differs for {entry.msgid!r}')
    return errors, count, len(src_entries)


def main():
    files = [Path(x) for x in sys.argv[1:]] or sorted((ROOT / 'work').rglob('*-zh_CN.po'))
    if not files:
        print('No PO batches found.', file=sys.stderr)
        return 2
    issues, translated, total = [], 0, 0
    for file in files:
        errors, n, size = check_batch(file)
        issues.extend(errors)
        translated += n
        total += size
        print(f'{file.name}: {n}/{size} translated; {len(errors)} structural issues')
    print(f'Total: {translated}/{total} translated; {len(issues)} structural issues')
    for issue in issues:
        print('ERROR:', issue)
    print('This check does not replace msgfmt, scientific review, or GUI testing.')
    return int(bool(issues))


if __name__ == '__main__':
    raise SystemExit(main())


