"""Check the final catalogs against the pinned development template."""
from collections import Counter
from pathlib import Path
import re
import polib
from check_batches import key, tokens, PRINTF

ROOT = Path(__file__).resolve().parent
template = polib.pofile(str(ROOT / 'source/gwyddion-r30752.pot'), check_for_duplicates=True)
mnemonics = lambda s: Counter(c.upper() for c in re.findall(r'(?<!_)_([A-Za-z0-9])', s))
expected_volume = {
    'zh_CN': ('体积', '体数据'),
    'zh_HK': ('體積', '體數據'),
    'zh_TW': ('體積', '體資料'),
}

for locale, expected in expected_volume.items():
    po = polib.pofile(str(ROOT / 'translations' / f'{locale}.po'), check_for_duplicates=True)
    assert [key(e) for e in po] == [key(e) for e in template], (locale, 'source keys/order')
    assert not po.obsolete_entries() and not po.fuzzy_entries() and not po.metadata_is_fuzzy, locale
    assert not po.untranslated_entries(), (locale, 'untranslated entries')
    assert po.metadata['Language'] == locale
    assert po.metadata['Plural-Forms'] == 'nplurals=1; plural=0;'
    assert 'charset=UTF-8' in po.metadata['Content-Type']
    assert po.metadata['Project-Id-Version'] == template.metadata['Project-Id-Version']
    assert po.metadata['POT-Creation-Date'] == template.metadata['POT-Creation-Date']
    for field in ('PO-Revision-Date', 'Last-Translator', 'Language-Team'):
        assert po.metadata.get(field), (locale, field)
    for original, entry in zip(template, po):
        for field in ('occurrences', 'flags'):
            assert getattr(original, field) == getattr(entry, field), (locale, entry.msgid, field)
        for field in ('comment', 'tcomment'):
            assert ' '.join(getattr(original, field).split()) == ' '.join(getattr(entry, field).split()), (locale, entry.msgid, field)
        sources = [original.msgid, original.msgid_plural] if original.msgid_plural else [original.msgid]
        if entry.msgid_plural:
            assert set(entry.msgstr_plural) == {0}, (locale, entry.msgid, 'plural forms')
        values = entry.msgstr_plural.values() if entry.msgid_plural else [entry.msgstr]
        for value in values:
            assert tokens(value) in [tokens(s) for s in sources], (locale, entry.msgid, 'tokens/tags')
            assert PRINTF.findall(value) in [PRINTF.findall(s) for s in sources], (locale, entry.msgid, 'printf order')
            assert not re.search('[\ufffd\ue000-\uf8ff]', value), (locale, entry.msgid, 'invalid character')
            if entry.msgid != 'current-language-code|en':
                assert mnemonics(value) in [mnemonics(s) for s in sources], (locale, entry.msgid, 'mnemonics')
    assert po.find('Volume').msgctxt is None and po.find('data-type|Volume').msgctxt is None
    assert (po.find('Volume').msgstr, po.find('data-type|Volume').msgstr) == expected
    print(f'{locale}: {len(po)}/{len(template)} translated; structure and Volume contexts OK')

print('Also run GNU msgfmt --check; these checks do not replace GUI or native-speaker review.')
