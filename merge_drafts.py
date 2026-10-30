# Merge verified simplified-Chinese batches without modifying regional catalogs.
from pathlib import Path
import polib
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
print(f'zh_CN: {len(translations)} imported source entries, '
      f'{catalog.percent_translated()}% of {len(catalog)} complete')
