"""Merge verified batches into draft catalogs; generate fuzzy regional drafts."""
from copy import deepcopy
from pathlib import Path
import polib
from opencc import OpenCC
from check_batches import check_batch, key

ROOT = Path(__file__).resolve().parent
FILES = sorted((ROOT / 'work').rglob('*-zh_CN.po'))
if not FILES:
    raise SystemExit('No batch files found')
translations = {}
for file in FILES:
    errors, _, _ = check_batch(file)
    if errors:
        raise SystemExit('\n'.join(errors))
    for entry in polib.pofile(str(file), check_for_duplicates=True):
        k = key(entry)
        if k in translations:
            raise SystemExit(f'Duplicate across batch files: {k!r}')
        translations[k] = entry

catalog = polib.pofile(str(ROOT / 'source' / 'gwyddion-2.71.pot'), check_for_duplicates=True)
catalog.header = 'Gwyddion Chinese localization draft. Distributed under the same license as Gwyddion.'
catalog.metadata = {
    'Project-Id-Version': 'Gwyddion 2.71',
    'Report-Msgid-Bugs-To': 'yeti@gwyddion.net',
    'POT-Creation-Date': catalog.metadata.get('POT-Creation-Date', ''),
    'Language': 'zh_CN',
    'MIME-Version': '1.0',
    'Content-Type': 'text/plain; charset=UTF-8',
    'Content-Transfer-Encoding': '8bit',
    'Plural-Forms': 'nplurals=1; plural=0;',
}
catalog.fuzzy = False
for entry in catalog:
    if entry.msgid_plural:
        entry.msgstr_plural = {0: entry.msgstr_plural.get(0, "")}
    translated = translations.get(key(entry))
    if translated is not None:
        entry.msgstr = translated.msgstr
        entry.msgstr_plural = dict(translated.msgstr_plural)
output = ROOT / 'translations'
output.mkdir(exist_ok=True)
catalog.save(str(output / 'zh_CN.po'))
for locale, scheme in [('zh_HK', 's2hk'), ('zh_TW', 's2twp')]:
    result = deepcopy(catalog)
    result.metadata['Language'] = locale
    result.header = ('Automatically converted regional draft, not yet reviewed. '
                     'Distributed under the same license as Gwyddion.')
    converter = OpenCC(scheme)
    for entry in result:
        if entry.msgstr:
            entry.msgstr = converter.convert(entry.msgstr)
            if 'fuzzy' not in entry.flags:
                entry.flags.append('fuzzy')
        if entry.msgstr_plural:
            entry.msgstr_plural = {i: converter.convert(s) for i, s in entry.msgstr_plural.items()}
            if any(entry.msgstr_plural.values()) and 'fuzzy' not in entry.flags:
                entry.flags.append('fuzzy')
    result.save(str(output / f'{locale}.po'))
    print(f'{locale}: converted entries marked fuzzy; regional review required')
print(f'zh_CN: {len(translations)} imported source entries, '
      f'{catalog.percent_translated()}% of {len(catalog)} complete')


