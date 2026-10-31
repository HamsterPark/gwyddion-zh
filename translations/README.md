# 翻译草稿与检查

`zh_CN.po` 是简体中文合并草稿：5,053 条中有 5,052 条已译，`Volume` 由于上游共享不同语境而暂时留空。批次已通读并进行了重点源码复核；详见 [简体中文总校记录](../REVIEW.md)。界面测试和领域审核仍待完成。

`zh_TW.po` 与 `zh_HK.po` 已由简体合并稿转换，并完成全文分段审校、地区用语复核和结构校验：各 5,053 条，其中 5,052 条有译文，`Volume` 暂留空，均无 fuzzy 标记。仍建议台湾／香港母语者终审并在 Gwyddion 2.71 中做界面测试；详见 [繁体全稿校对报告](../PROOFREADING.md) 和 [总校记录](../REVIEW.md)。

## 合并与检查

在项目根目录安装 `requirements.txt` 中的依赖，然后运行：

```sh
python check_batches.py
python merge_drafts.py
python regionalize.py
msgfmt --check --statistics -o zh_CN.mo translations/zh_CN.po
msgfmt --check --statistics -o zh_TW.mo translations/zh_TW.po
msgfmt --check --statistics -o zh_HK.mo translations/zh_HK.po
```

检查脚本核对批次原文键、格式标记、常见 printf 和 Gwyddion 占位符及标签；它并不能替代 GNU `msgfmt --check`、领域审校或实际运行测试。合并脚本以固定模板为准，只导入批次译文并生成简体合并稿；`regionalize.py` 随后从简体稿生成 `zh_TW.po`／`zh_HK.po`，套用地区用语表、通用术语表和上下文修复，并移除 fuzzy。重新运行 `regionalize.py` 会覆盖这两份繁体稿，手工修改应先写回地区用语表、上下文修复表或备份。简体校对应写回各批次，再重新合并。

`work/` 下的各 PO 是简体翻译工作底稿；详见[交接说明](../HANDOFF.md)。
