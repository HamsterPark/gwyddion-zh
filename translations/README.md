# 翻译草稿与检查

`zh_CN.po` 是简体中文合并草稿：5,053 条中有 5,052 条已译，`Volume` 由于上游共享不同语境而暂时留空。批次已通读并进行了重点源码复核；详见 [简体中文总校记录](../REVIEW.md)。界面测试和领域审核仍待完成。

香港／澳门及台湾版本正在独立制作和审校。原有自动转换稿并非已审核的地区翻译；请以相应地区工作的最新状态为准。简体合并不会覆盖这两个文件。

## 合并与检查

在项目根目录安装 `requirements.txt` 中的依赖，然后运行：

```sh
python check_batches.py
python merge_drafts.py
msgfmt --check --statistics -o zh_CN.mo translations/zh_CN.po
```

检查脚本核对批次原文键、格式标记、常见 printf 和 Gwyddion 占位符及标签；它并不能替代 GNU `msgfmt --check`、领域审校或实际运行测试。合并脚本以固定模板为准，只导入批次译文，只覆盖本目录的简体草稿，不会生成或覆盖香港、台湾的繁体文件。简体校对应写回各批次，再重新合并。

`work/` 下的各 PO 是简体翻译工作底稿；详见[交接说明](../HANDOFF.md)。
