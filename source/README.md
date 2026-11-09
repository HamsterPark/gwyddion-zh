# 翻译模板来源

## 当前：SVN r30752

`gwyddion-r30752.pot` 从 [Gwyddion 官方 SVN 的固定 r30752 源码](https://svn.code.sf.net/p/gwyddion/code/!svn/bc/30752/trunk/gwyddion/) 提取，包含 5,057 个消息键。源码目录中的 PO 尚未刷新模板，不能把它们当作当前源码字符串的完整清单。

提取沿用上游 `utils/update-potfiles.sh` 的目录、文件类型和排除规则，以及 `po/Makevars` 的关键词配置。`POTFILES-r30752.in` 列出 533 个实际输入文件，`gwyddion-r30752.sources.json` 记录这些输入和模板的 SHA-256。

本次将官方 2.71 源码作为本地基础，读取固定 SVN 修订的目录清单和 r29700 至 r30752 的路径变更记录，更新了 46 个 C/C++ 源码或头文件，并补取未包含在发布源码包中的 `modules/xyz/xyz_drift.c`。使用 SVN 清单限定输入，避免将发布包生成文件误作版本库源码。仅从发布源码包直接提取会遗漏 XYZ 漂移模块的消息，故没有采用该不完整结果。

也可以直接导出完整的固定修订源码，按 `POTFILES-r30752.in` 重提模板。在导出源码根目录中运行（清单和输出路径按实际位置调整）：

```sh
xgettext --keyword=_ --keyword=N_ --keyword=gwy_sgettext \
  --foreign-user --from-code=UTF-8 --add-comments=TRANSLATORS \
  --package-name=Gwyddion --package-version="SVN r30752" \
  --msgid-bugs-address=yeti@gwyddion.net \
  --copyright-holder="David Necas (Yeti) & Petr Klapetek" \
  --files-from=POTFILES-r30752.in --output=gwyddion-r30752.pot
```

使用 GNU gettext 1.0 提取；工具版本、源码中的 SVN `$Id` 展开和生成时间可能影响排版、注释或时间戳。应比较消息键、占位符、格式标记和源码引用，而不只比较整个文件哈希。

## 历史：2.71

`gwyddion-2.71.pot` 是 [2.71 正式版源码](https://gwyddion.net/download/2.71/)中的官方模板，5,053 条。原始工作批次按此模板拆分，保留不变。

相较 2.71，r30752 有 7 个新键、3 个移除的旧键：其中 3 对仅调整曲线过滤相关英文的大小写；其余新增为 `data-type|Volume`、`Filter Curves` 及 Titan TEM 格式的两条说明。裸 `Volume` 的原文未变，但引用已限定为物理体积，现可单独翻译。
