# 当前译稿与验证

`zh_CN.po`、`zh_HK.po`、`zh_TW.po` 当前基于 Gwyddion **SVN r30752**，各 5,057/5,057 条已译，无 fuzzy、过时条目或空译文。

上游已经拆分 `Volume`：物理量分别使用“体积／體積”，`data-type|Volume` 数据类型分别使用“体数据／體數據／體資料”。这里是 Gwyddion 的 `gwy_sgettext` 前缀式上下文，不是 PO 的 `msgctxt`；译文中不包含 `data-type|`。

这些文件面向含此修复的开发版。2.71 稳定版仍共用裸 `Volume`，请使用[保留的 2.71 译稿](https://github.com/HamsterPark/gwyddion-zh/tree/8ea21621f8431cf4438907c7225fcd1e95d237e9/translations)。不要把当前译稿作为完全兼容 2.71 的语言包。

## 合并与检查

安装项目 `requirements.txt` 中的依赖及 GNU gettext 后运行：

```sh
python check_batches.py
python merge_drafts.py
python regionalize.py
python check_catalogs.py
msgfmt --check --statistics -o zh_CN.mo translations/zh_CN.po
msgfmt --check --statistics -o zh_HK.mo translations/zh_HK.po
msgfmt --check --statistics -o zh_TW.mo translations/zh_TW.po
```

`work/` 下的简体批次及其模板继续保留 2.71 基准。合并脚本在当前开发版模板上导入这些译文，再应用 `updates/zh_CN.po` 中的增补与覆盖；已经从上游模板删除的旧键不输出。地区脚本以当前模板和简体总稿生成繁体稿，并应用地区术语与逐条修复。

两个生成脚本会覆盖对应总稿。简体后续校对应写回原批次或开发版增补；繁体修订应同步地区规则或逐条修复表，并检查重新生成后的差异。

`check_catalogs.py` 核对三份最终稿的完整性、原文键和引用、格式参数、标签、快捷键及两个 `Volume` 语境。自动检查和编译不能替代完整界面、地区母语者及领域审阅。最新验证见 [上游反馈与续交记录](../UPSTREAM_UPDATE_20261109.md)，早期审校记录保留为历史证据。
