#!/usr/bin/env python3
"""Build reviewed zh_TW / zh_HK catalogs from the merged zh_CN draft.

OpenCC supplies character and phrase conversion.  The explicit tables below
then apply Taiwan / Hong Kong vocabulary that OpenCC does not handle, including
scientific and UI terms.  Run this after merge_drafts.py; it rewrites
translations/zh_TW.po and translations/zh_HK.po from the merged zh_CN draft.
"""
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent
TOOLS = ROOT / '.tools'
if TOOLS.is_dir():
    sys.path.insert(0, str(TOOLS))
import polib
from opencc import OpenCC

SRC = ROOT / 'translations' / 'zh_CN.po'
POT = ROOT / 'source' / 'gwyddion-2.71.pot'
OUT = ROOT / 'translations'


def key(entry):
    return entry.msgctxt, entry.msgid, entry.msgid_plural


# Taiwan: OpenCC s2twp already handles most vocabulary; these are the
# remaining mainland forms and a few Taiwan-specific scientific terms.
TW_REPLACEMENTS = [
    ('右鍵單擊', '以滑鼠右鍵按一下'),
    ('左鍵單擊', '以滑鼠左鍵按一下'),
    ('單擊', '按一下'),
    ('雙擊', '按兩下'),
    ('選項卡', '索引標籤'),
    ('另存為', '另存新檔'),
    ('控制檯', '主控台'),
    ('影象', '影像'),
    ('掩膜', '遮罩'),
    ('質量', '品質'),
    ('幫助', '說明'),
    ('退出', '結束'),
    ('協議', '協定'),
    ('插值', '內插'),
    ('方差', '變異數'),
    ('均變異數', '均方差'),
    ('偏度', '偏態'),
    ('標量', '純量'),
    ('漸變', '漸層'),
    ('字符', '字元'),
    ('噪聲', '雜訊'),
    ('聚類', '分群'),
    ('歸一化', '正規化'),
    ('最小二乘法', '最小平方法'),
    ('位深度', '位元深度'),
    ('位深', '位元深度'),
    ('指標工具', '游標工具'),
    ('讀取指標下', '讀取游標下'),
    ('字號', '字級'),
    ('灰度', '灰階'),
    ('引用', '參照'),
    ('HDF5 庫', 'HDF5 函式庫'),
    ('其他庫', '其他函式庫'),
    ('檔案頭', '檔案標頭'),
    ('檔案名稱', '檔名'),
    ('檔案名', '檔名'),
    ('Surfstand 專案', 'Surfstand 群組'),
    ('專案', '項目'),
    ('型別', '類型'),
    ('類型頭', '類型標頭'),
    ('控制元件', '控制項'),
    ('區域性', '局部'),
    ('鐳射', '雷射'),
    ('映象', '鏡像'),
    ('擴充套件', '擴展'),
    ('全域性', '全域'),
    ('部分割槽域', '部分區域'),
    ('分割槽法', '分割法'),
    ('條頻', '條帶'),
    ('溼', '濕'),
    ('丟失', '遺失'),
    ('查詢曲線圖中的峰', '尋找曲線圖中的峰'),
    ('查詢峰', '尋找峰'),
    ('查詢谷', '尋找谷'),
    ('查詢極小值', '尋找極小值'),
    ('查詢資料間的簡單關係', '尋找資料間的簡單關係'),
    ('查詢欄位', '尋找欄位'),
    ('Igor 二進位制 wave', 'Igor 二進位波形'),
    ('行動式', '可攜式'),
    ('英寸', '英吋'),
    ('透過選定點', '穿過選定點'),
    ('卷積', '摺積'),
    ('采樣', '取樣'),
    ('當前', '目前'),
    ('生成', '產生'),
    ('獲取', '取得'),
    ('撤銷', '復原'),
    ('替換', '取代'),
    ('校準', '校正'),
    ('實現', '實作'),
    ('柵格', '點陣'),
    ('拆分', '分割'),
    ('模量', '模數'),
    ('錯誤程式碼', '錯誤碼'),
    ('單位程式碼', '單位代碼'),
    ('身份', '身分'),
    ('提取', '擷取'),
    ('應用', '套用'),
    ('重置', '重設'),
    ('選中', '選取'),
    ('電勢', '電位'),
    ('互動裁剪', '相互裁剪'),
    ('引數掃描', '參數掃描'),
    ('空間引數', '空間參數'),
    ('分割法', '分區法'),
]

# Hong Kong: s2hk mostly converts characters, so the vocabulary table is
# larger.  Order matters: files are converted before documents.
HK_REPLACEMENTS = [
    ('右鍵單擊', '以滑鼠右鍵按一下'),
    ('左鍵單擊', '以滑鼠左鍵按一下'),
    ('單擊', '按一下'),
    ('雙擊', '按兩下'),
    ('選項卡', '索引標籤'),
    ('另存為', '另存新檔'),
    ('控制枱', '控制台'),
    ('文件夾', '資料夾'),
    ('文件', '檔案'),
    ('文檔', '文件'),
    ('文本', '文字'),
    ('剪貼板', '剪貼簿'),
    ('默認', '預設'),
    ('設置', '設定'),
    ('鼠標', '滑鼠'),
    ('光標', '游標'),
    ('內存', '記憶體'),
    ('磁盤', '磁碟'),
    ('打印', '列印'),
    ('視頻', '影片'),
    ('音頻', '音訊'),
    ('創建', '建立'),
    ('搜索', '搜尋'),
    ('質量', '質素'),
    ('用户', '用戶'),
    ('界面', '介面'),
    ('程序', '程式'),
    ('信息', '資訊'),
    ('消息', '訊息'),
    ('支持', '支援'),
    ('保存', '儲存'),
    ('加載', '載入'),
    ('打開', '開啟'),
    ('窗口', '視窗'),
    ('導出', '匯出'),
    ('導入', '匯入'),
    ('插件', '外掛程式'),
    ('模塊', '模組'),
    ('字節', '位元組'),
    ('分辨率', '解析度'),
    ('運行', '執行'),
    ('查看', '檢視'),
    ('幫助', '說明'),
    ('退出', '結束'),
    ('控件', '控制項'),
    ('對話框', '對話方塊'),
    ('協議', '協定'),
    ('命令行', '命令列'),
    ('堆棧', '堆疊'),
    ('腳本', '指令碼'),
    ('元數據', '元資料'),
    ('視圖', '檢視'),
    ('掩膜', '遮罩'),
    ('運算符', '運算子'),
    ('操作數', '運算元'),
    ('標識符', '識別碼'),
    ('字符串', '字串'),
    ('字符', '字元'),
    ('變量', '變數'),
    ('數組', '陣列'),
    ('對象', '物件'),
    ('接口', '介面'),
    ('源代碼', '原始碼'),
    ('信號', '訊號'),
    ('採樣', '取樣'),
    ('傅里葉', '傅立葉'),
    ('噪聲', '雜訊'),
    ('歸一化', '正規化'),
    ('指針工具', '游標工具'),
    ('讀取指針下', '讀取游標下'),
    ('字號', '字體大小'),
    ('灰度', '灰階'),
    ('圖標', '圖示'),
    ('菜單', '選單'),
    ('HDF5 庫', 'HDF5 程式庫'),
    ('其他庫', '其他程式庫'),
    ('檔案頭', '檔案標頭'),
    ('檔案名稱', '檔名'),
    ('檔案名', '檔名'),
    ('Surfstand 項目', 'Surfstand 群組'),
    ('頭檔案', '標頭檔案'),
    ('類型頭', '類型標頭'),
    ('存儲', '儲存'),
    ('鋭', '銳'),
    ('閲', '閱'),
    ('丟失', '遺失'),
    ('Igor 二進制 wave', 'Igor 二進制波形'),
    ('矢量', '向量'),
    ('位圖', '點陣圖'),
    ('反捲積', '反卷積'),
    ('捲積', '卷積'),
    ('位深度', '位元深度'),
    ('位深', '位元深度'),
    ('采樣', '取樣'),
    ('當前', '目前'),
    ('生成', '產生'),
    ('獲取', '取得'),
    ('通過', '透過'),
    ('添加', '新增'),
    ('撤銷', '復原'),
    ('替換', '取代'),
    ('查找', '尋找'),
    ('字段', '欄位'),
    ('迴歸', '回歸'),
    ('透過選定點', '穿過選定點'),
    ('温', '溫'),
    ('説', '說'),
    ('啓', '啟'),
    ('峯', '峰'),
    ('硅', '矽'),
    ('交互裁剪', '相互裁剪'),
    ('數據夾', '資料夾'),
]

# Shared corrections for wording that is wrong or unnatural in both
# Traditional Chinese locales.  These are applied after the locale-specific
# tables so that the latter can first normalize regional vocabulary.
COMMON_REPLACEMENTS = [
    ('配置', '設定'),
    ('禁用', '停用'),
    ('構建於', '建置於'),
    ('構建時', '建置時'),
    ('正在構建', '正在建立'),
    ('資料頭', '資料標頭'),
    ('數據頭', '數據標頭'),
    ('幅值', '振幅'),
    ('中值', '中位數'),
    ('選擇管理器', '選區管理器'),
    ('規則化', '正則化'),
    ('力與壓入', '力與壓痕'),
    ('判據', '準則'),
    ('預定義', '預先定義'),
    ('按塊', '分塊'),
    ('掃描電鏡', '掃描式電子顯微鏡'),
    ('每取樣位數', '每取樣位元數'),
    ('標籤頭行', '標籤標頭行'),
    ('計算器', '計算機'),
    ('轉儲', '傾印'),
    ('既不是組', '既不是群組'),
    ('魔數檔案標頭不匹配', '檔案標頭魔數不匹配'),
    ('頁頭魔數', '頁面標頭魔數'),
    ('取代將覆蓋其內容', '若取代，將覆蓋其內容'),
    ('排除線性傾斜', '排除線性歪斜'),
    ('遮蔽空白區域', '遮罩空白區域'),
    ('偏正態分佈', '偏常態分佈'),
    ('類型 %s 是座標軸 %s 唯一支援的類型。', '僅支援類型 %s（座標軸 %s）。'),
    ('列表 ‘%s’ 含有 %u 項，這與數量 %u 不同，後者由 ‘%s’ 給出。', '列表 ‘%s’ 含有 %u 項，與數量 %u（由 ‘%s’ 給出）不同。'),
    ('匯出量', '衍生量'),
    ('錶面', '表面'),
    # Preserve the source mnemonic letter, not just the underscore count.
    ('測量特徵(_M)', '測量特徵(_F)'),
    ('縱向(_G)', '縱向(_N)'),
    ('視窗高度(_H)', '視窗高度(_E)'),
]

# Context-sensitive fixes that must not be applied as blind substring
# replacements (they would affect unrelated UI strings).
ENTRY_FIXES = {
    '_Activation': {
        'zh_TW': '活化(_A)',
        'zh_HK': '激活(_A)',
    },
    '_Load applied': {
        'zh_TW': '施加負載(_L)',
        'zh_HK': '施加載荷(_L)',
    },
    'AUX in 6 (Surface Potential)': {
        'zh_TW': 'AUX 輸入 6（表面電位）',
        'zh_HK': 'AUX 輸入 6（表面電勢）',
    },
}


# Grok review: raw image rows and columns, keyed by source context.
ENTRY_FIXES.update({
    "_Each image row skip": {
        "zh_HK": "每個圖像列跳過(_E)",
        "zh_TW": "每個影像列略過(_E)"
    },
    "E_xtract column": {
        "zh_HK": "提取欄(_X)",
        "zh_TW": "擷取欄(_X)"
    },
    "After each _row skip": {
        "zh_HK": "每列之後跳過(_R)",
        "zh_TW": "每列之後略過(_R)"
    },
    "Expected whitespace to skip more fields in row %u, got `%.16s'": {
        "zh_HK": "第 %u 列需要用空白跳過更多欄位，實際遇到 `%.16s'",
        "zh_TW": "第 %u 列需要用空白跳過更多欄位，實際遇到 `%.16s'"
    },
    "Expected `%c' to skip more fields in row %u, got `%.16s'": {
        "zh_HK": "需要用 `%c’ 在第 %u 列跳過更多欄位，實際遇到 `%.16s'",
        "zh_TW": "需要用 `%c’ 在第 %u 列跳過更多欄位，實際遇到 `%.16s'"
    },
    "Expected `%s' to skip more fields in row %u, got `%.16s'": {
        "zh_HK": "需要用 `%s’ 在第 %u 列跳過更多欄位，實際遇到 `%.16s'",
        "zh_TW": "需要用 `%s’ 在第 %u 列跳過更多欄位，實際遇到 `%.16s'"
    },
    "Garbage `%.16s' in row %u, column %u": {
        "zh_HK": "多餘內容 `%.16s’ 出現在第 %u 列第 %u 欄",
        "zh_TW": "多餘內容 `%.16s’ 出現在第 %u 列第 %u 欄"
    },
    "Expected delimiter `%c' after data in row %u, column %u, got `%c'": {
        "zh_HK": "數據之後應為分隔符 `%c’，位置在第 %u 列第 %u 欄，實際為 `%c'",
        "zh_TW": "資料之後應為分隔符 `%c’，位置在第 %u 列第 %u 欄，實際為 `%c'"
    },
    "Expected delimiter `%s' after data in row %u, column %u, got `%.16s'": {
        "zh_HK": "數據之後應為分隔符 `%s’，位置在第 %u 列第 %u 欄，實際為 `%.16s'",
        "zh_TW": "資料之後應為分隔符 `%s’，位置在第 %u 列第 %u 欄，實際為 `%.16s'"
    }
})


# Data-table/matrix directions use row = 列 and column = 欄.  Keep text
# lines (line = 行) and scanning terminology separate from these entries.
ENTRY_FIXES.update({
    'Rows:': {'zh_HK': '列：', 'zh_TW': '列：'},
    'Columns:': {'zh_HK': '欄：', 'zh_TW': '欄：'},
    'Wrong number of header rows or columns.': {
        'zh_HK': '檔案標頭的列數或欄數不正確。',
        'zh_TW': '檔案標頭的列數或欄數不正確。',
    },
    'DATA_INFO does not contain the expected columns: %s.': {
        'zh_HK': 'DATA_INFO 未包含預期的欄：%s。',
        'zh_TW': 'DATA_INFO 未包含預期的欄：%s。',
    },
    'Wrong number of initial data columns.': {
        'zh_HK': '起始數據欄數不正確。',
        'zh_TW': '起始資料欄數不正確。',
    },
    'Row/Column Statistics': {'zh_HK': '列／欄統計', 'zh_TW': '列／欄統計'},
    'Calculate row/column statistical functions': {
        'zh_HK': '計算列／欄統計函數',
        'zh_TW': '計算列／欄統計函式',
    },
    'Row/column statistical function tool, mean values, medians, maxima, minima, RMS, ..., of rows or columns.': {
        'zh_HK': '列／欄統計函數工具，計算各列或欄的平均值、中位數、最大值、最小值、均方根等。',
        'zh_TW': '列／欄統計函式工具，計算各列或欄的平均值、中位數、最大值、最小值、均方根等。',
    },
    'Data ended prematurely at line %d and column %d.': {
        'zh_HK': '數據在第 %d 行、第 %d 欄提前結束。',
        'zh_TW': '資料在第 %d 行、第 %d 欄提前結束。',
    },
    'Malformed data encountered at line %d and column %d.': {
        'zh_HK': '第 %d 行、第 %d 欄遇到格式錯誤的數據。',
        'zh_TW': '第 %d 行、第 %d 欄遇到格式錯誤的資料。',
    },
    'Line %d has %d columns instead of expected %d.': {
        'zh_HK': '第 %d 行有 %d 欄，預期應為 %d 欄。',
        'zh_TW': '第 %d 行有 %d 欄，預期應為 %d 欄。',
    },
    'Rows stride %u does not match length and bytes per item (%u×%u).': {
        'zh_HK': '列跨度 %u 與長度及每項位元組數（%u×%u）不符。',
        'zh_TW': '列跨度 %u 與長度及每項位元組數（%u×%u）不符。',
    },
})


def normalize(text, replacements, kmeans):
    # "平均值" already contains the substring "均值"; protect it (and the
    # K-means label) before replacing the remaining mainland form.
    text = text.replace('平均值', '\ue000')
    text = text.replace('K 均值', '\ue001')
    text = text.replace('均值', '平均值')
    text = text.replace('\ue001', kmeans)
    text = text.replace('\ue000', '平均值')
    for old, new in replacements:
        text = text.replace(old, new)
    return text


def build(locale, scheme, replacements, team, title):
    converter = OpenCC(scheme)
    cn = polib.pofile(str(SRC))
    translations = {key(e): e for e in cn if e.msgstr or e.msgstr_plural}
    po = polib.pofile(str(POT))
    po.metadata = {
        'Project-Id-Version': 'Gwyddion 2.71',
        'Report-Msgid-Bugs-To': 'yeti@gwyddion.net',
        'POT-Creation-Date': po.metadata.get('POT-Creation-Date', ''),
        'PO-Revision-Date': datetime.now().astimezone().strftime('%Y-%m-%d %H:%M%z'),
        'Last-Translator': 'Hamster Park (Yuanhao Lyu)',
        'Language-Team': team + ' <https://github.com/HamsterPark/gwyddion-zh>',
        'Language': locale,
        'MIME-Version': '1.0',
        'Content-Type': 'text/plain; charset=UTF-8',
        'Content-Transfer-Encoding': '8bit',
        'Plural-Forms': 'nplurals=1; plural=0;',
    }
    po.header = (title + '\nDistributed under the same license as Gwyddion.\n'
                 'Translation and proofreading assisted by GPT-6.1 Terra, Grok 4.7, and DeepSeek V4.1 Flash.')
    po.metadata_is_fuzzy = []
    po.wrapwidth = 0
    changed = 0
    for entry in po:
        source = translations.get(key(entry))
        if source is not None:
            entry.msgstr = source.msgstr
            entry.msgstr_plural = dict(source.msgstr_plural)
        kmeans = 'K 平均法' if locale == 'zh_TW' else 'K 均值'
        all_replacements = replacements + COMMON_REPLACEMENTS
        if entry.msgstr:
            new = normalize(converter.convert(entry.msgstr), all_replacements, kmeans)
            if new != entry.msgstr:
                changed += 1
            entry.msgstr = new
        if entry.msgstr_plural:
            entry.msgstr_plural = {
                i: normalize(converter.convert(s), all_replacements, kmeans)
                for i, s in entry.msgstr_plural.items()
            }
        fix = ENTRY_FIXES.get(entry.msgid, {}).get(locale)
        if fix is not None:
            entry.msgstr = fix
        # Taiwan distinguishes parameter (參數) from argument (引數); the
        # Simplified draft uses 引數 for both.  Keep the three true argument
        # strings untouched.
        if (locale == 'zh_TW' and 'parameter' in entry.msgid.lower()
                and 'argument' not in entry.msgid.lower()):
            entry.msgstr = entry.msgstr.replace('引數', '參數')
        if entry.msgid == 'current-language-code|en':
            entry.msgstr = locale
        entry.flags = [f for f in entry.flags if f != 'fuzzy']
    path = OUT / f'{locale}.po'
    po.save(str(path), newline='\n')
    raw = path.read_bytes().replace(b'\r\n', b'\n')
    path.write_bytes(raw)
    print(f'{locale}: {len(po)} entries, {changed} entries adjusted, {len(po.fuzzy_entries())} fuzzy')


build(
    'zh_TW', 's2twp', TW_REPLACEMENTS,
    'Chinese (Traditional, Taiwan)',
    'Gwyddion 2.71 Traditional Chinese (Taiwan) translation.',
)
build(
    'zh_HK', 's2hk', HK_REPLACEMENTS,
    'Chinese (Traditional, Hong Kong)',
    'Gwyddion 2.71 Traditional Chinese (Hong Kong) translation.',
)
