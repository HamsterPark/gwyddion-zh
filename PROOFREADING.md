# Gwyddion 2.71 繁体中文全稿校对报告

> 更新（2026-10-31）：本机已安装 GNU gettext，简体、香港和台湾总稿均已通过 `msgfmt --check`；各有 5,052 条译文，`Volume` 留空。以下关于缺少 `msgfmt` 的记载保留为当时的检查状态。

日期：2026-10-30

范围：`translations/zh_TW.po`、`translations/zh_HK.po`

基准：`source/gwyddion-2.71.pot`（5,053 条）

## 结论

台湾（`zh_TW`）与香港（`zh_HK`）两版均已完成全文分段审阅、地区用语复核和结构校验。两版各 5,053 条，其中 5,052 条有译文，`Volume` 因上游共享不同语境而留空，均无 fuzzy 标记。当前没有发现原文键、引用、注释、flags、printf 占位符数量或顺序、Pango/XML 标签、转义、空白或 GTK 快捷键字母的结构性错误。

本报告记录的是模型辅助全文审校、术语规则复核和自动检查的结果，不等同于台湾／香港母语者的领域终审，也不等同于 Gwyddion 2.71 的实际界面验收。

## 校对流程

1. **生成**：以合并后的 `translations/zh_CN.po` 为源，经 OpenCC `s2twp`／`s2hk` 转换，再由 `regionalize.py` 套用地区用语表、通用术语表和少量上下文修复。没有直接采用未经复核的 OpenCC 输出。
2. **全文分段审阅**：三个独立分段审阅通道覆盖全部 5,053 条；另对 690 条完整句子或不少于八个英文词的条目逐条通读，并对全部 TW/HK 地区差异做逐条归类。
3. **语义重点复核**：统计与拟合术语、扫描探针显微学术语、文件格式与导入错误、菜单路径、掩膜／选区、插值／卷积、校准／校正、参数／引数等易混词。
4. **自动扫描**：术语一致性、跨地区用词泄漏、拉丁字母残留、重复标点、括号平衡、可疑重复、译文长度比例，以及已知错误串回归检查。
5. **结构校验**：原文键及顺序、引用、注释、flags、printf 与 Gwyddion 占位符的数量和顺序、XML/Pango 标签、转义、首尾空白、换行、GTK 快捷键字母。
6. **编译检查**：使用 `polib` 解析两份 PO，并编译为 MO；当前环境没有 GNU `msgfmt`，因此尚未运行 `msgfmt --check`。

## 本轮修复的主要问题

### printf 占位符顺序

- `Only type %s is supported for axis %s.` 原译把两个 `%s` 的顺序对调，轴名和类型会互换。已改为保持参数顺序的 `僅支援類型 %s（座標軸 %s）。`
- `List ‘%s’ has %u items which differs from the number %u given by ‘%s’.` 原译把第三个 `%s` 与第四个 `%u` 对调，存在类型不匹配风险。已改为 `列表 ‘%s’ 含有 %u 項，與數量 %u（由 ‘%s’ 給出）不同。`

### 语义与术语

- `_Exclude linear skew`：扫描歪斜不是倾斜，改为“排除線性歪斜”。
- `_Mask empty regions`：此处是建立遮罩，不是“遮蔽”，改为“遮罩空白區域”。
- `distribution|Skew-normal`：改为“偏常態分佈”。
- `Skewed silicon 7x7`：香港版把“硅”统一为“矽”，与台湾及香港化学用字一致。
- `Mean square difference`：台湾版由“均變異數值”改为“均方差值”，避免把 mean square difference 与 variance 混同。
- `Unit code`：台湾版由“單位程式碼”改为“單位代碼”。
- `Surface dilation by defined tip`：修正“錶面”为“表面”。
- `Mutual Crop`：由“互動裁剪／交互裁剪”改为“相互裁剪”，避免把 mutual 误作 interactive。
- `Derived Quantities`：由“匯出量”改为“衍生量”。
- `_Load applied`：由不成词的“施載入荷”改为台湾“施加負載”、香港“施加載荷”。
- `_Activation`：台湾版由 UI 用语的“啟用”改为物理/化学语境的“活化”；香港版保留“激活”。
- `AUX in 6 (Surface Potential)`：台湾用“表面電位”，香港用“表面電勢”。
- `Partitioning`：两版统一为“分區法”，与分形维数方法语境一致，避免与“分割”混淆。

### 参数与引数

台湾版原先把 parameter 与 argument 都译为“引數”。本轮按台湾习惯区分：

- parameter／参数类条目改为“參數”；
- argument／函数或命令行参数保留“引數”。

共 40 条原用“引數”的 parameter、参数扫描类条目改为“參數”，仅 3 条 argument 条目保留“引數”。

### 台湾地区 UI 用语

- `Apply`：由“應用”改为“套用”（21 条）。
- `Reset`：由“重置”改为“重設”（6 条）。
- `selected`：由“選中”改为“選取”（7 条）。

香港版保留“應用／重置／選中”，作为当地 UI 用词；两版的这些差异已登记为预期地区差异。

### GTK 快捷键字母

结构校验原先只比较下划线数量，本轮增加了快捷键字母比较，修复了以下字母不一致：

- `/Measure _Features/...`：`測量特徵(_M)` 改为 `測量特徵(_F)`（6 条菜单路径）。
- `Le_ngthwise`：`縱向(_G)` 改为 `縱向(_N)`。
- `Window h_eight`：`視窗高度(_H)` 改为 `視窗高度(_E)`。

### 其他地区修正

- 香港版 `數據夾` 改为 `資料夾`，避免“資料→數據”规则误伤文件夹。
- `current-language-code|en` 分别写为 `zh_TW`／`zh_HK`。

## 地区术语约定

| 英文 | `zh_TW` | `zh_HK` |
| --- | --- | --- |
| data | 資料 | 數據 |
| image | 影像 | 圖像 |
| quality | 品質 | 質素 |
| user | 使用者 | 用戶 |
| software / hardware | 軟體／硬體 | 軟件／硬件 |
| network | 網路 | 網絡 |
| metadata | 後設資料 | 元資料 |
| convolution | 摺積 | 卷積 |
| interpolation | 內插 | 插值 |
| variance | 變異數 | 方差 |
| skewness | 偏態 | 偏度 |
| scalar | 純量 | 標量 |
| gradient | 漸層 | 漸變 |
| clustering | 分群 | 聚類 |
| calibration | 校正 | 校準 |
| regression | 迴歸 | 回歸 |
| pixel | 畫素 | 像素 |
| compatible | 相容 | 兼容 |
| binary | 二進位 | 二進制 |
| raster | 點陣 | 柵格 |
| split | 分割 | 拆分 |
| modulus | 模數 | 模量 |
| potential | 電位 | 電勢 |
| activation | 活化 | 激活 |
| load | 負載 | 載荷 |
| apply | 套用 | 應用 |
| reset | 重設 | 重置 |
| selected | 選取 | 選中 |
| parameter | 參數 | 參數 |
| argument | 引數 | 參數（香港不強分） |

## 验收结果

| 项目 | `zh_TW` | `zh_HK` |
| --- | --- | --- |
| 条目总数 | 5,053 | 5,053 |
| 有译文 | 5,052 | 5,052 |
| fuzzy | 0 | 0 |
| 空译文 | 1（`Volume`） | 1（`Volume`） |
| 结构问题 | 0 | 0 |
| printf 数量问题 | 0 | 0 |
| printf 顺序问题 | 0 | 0 |
| 复数占位符问题 | 0 | 0 |
| 快捷键字母问题 | 0 | 0 |
| 编码 | UTF-8、LF、无 BOM | UTF-8、LF、无 BOM |
| `Plural-Forms` | `nplurals=1; plural=0;` | `nplurals=1; plural=0;` |
| MO 编译（`polib`） | 通过 | 通过 |

简体字扫描报告 119 条警告，均为“台、峰、干、里、群、岩、游”等共享字或异体字造成的误报，不是简体泄漏。

## 剩余问题与测试缺口

1. **`Volume` 仍留空**：上游同一原文既表示颗粒统计中的“体积”，又表示数据浏览器中的“体数据”。当前 gettext 目录无法按位置区分；留空时界面回退英文，避免在错误语境中给出确定但错误的译文。
2. **缺少母语者终审**：本轮是模型辅助全文审校，不是台湾／香港母语者的领域验收。薄膜模型、粗糙度指标、残差定义、统计术语等仍应由相关领域使用者复核。
3. **GNU `msgfmt --check` 未运行**：当前环境没有 `msgfmt`；已用 `polib` 解析和 MO 编译代替。提交前应在有 gettext 的环境中补跑三份 PO 的 `msgfmt --check --statistics`。
4. **未做 Gwyddion 2.71 界面实测**：菜单布局、中文断行、按钮截断、字体宽度、快捷键冲突和实际加载行为仍需在 2.71 中验证；不能以 2.67 的冒烟测试代替。
5. **少量技术名保留英文**：如 `NaN`、`pickle`、`Schwoebel`、`sech`、`XYZ`、`Key`、`OMOMS`、`NNA`、`Schaum` 等，属于专名、算法名或没有可靠统一译名的技术标签；未强行意译。
6. **`Lunette`、`Parabola`**：沿用简体总校记录的暂译说明；如上游增加 context，可进一步按“月牙形／抛物面／抛物线”分语境处理。
7. **`Good Mean Profile`** 等少量风格性译法未做进一步统一；不影响结构或主要语义，但可在母语终审时调整。

## 复现与验证

```sh
python regionalize.py
python C:\Users\yuanh\AppData\Local\Temp\opencode\validate_regional.py
```

`regionalize.py` 会以固定模板和简体合并稿重新生成 `zh_TW.po`／`zh_HK.po`；手工修改应先写回地区用语表或上下文修复表，否则会被下一次生成覆盖。`work/grok-*` 批次文件未修改。

本次没有提交或推送；`translations/zh_CN.po` 保持原状，其头部 fuzzy 状态和 CRLF 行尾不在本次繁体稿修订范围内。
