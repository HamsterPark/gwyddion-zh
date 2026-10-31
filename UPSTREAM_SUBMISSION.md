# 向 Gwyddion 上游提交中文翻译

## 官方渠道

[官方翻译贡献指南](https://gwyddion.net/contribute.php)要求使用 UTF-8 PO 文件，并说明即使是部分翻译也可以提交；翻译成果可发送给协调翻译工作的 David Nečas（Yeti）。[官方联系页](https://gwyddion.net/contact.php)列出的翻译联系人为 `yeti@gwyddion.net`，同时建议一般开发讨论通过 [gwyddion-devel 邮件列表](https://sourceforge.net/p/gwyddion/mailman/gwyddion-devel/)公开进行。

邮件列表只接受已订阅地址发帖；官方说明未订阅或附件过大的邮件会被丢弃，即使自动回复显示等待审核。适合在讨论中提供公开仓库的链接，不要直接发送大附件。SourceForge 的 Web 论坛也是选择，但发帖需要登录。

上游 SVN 是主要源码库，仓库写权限按既有贡献情况单独授予；我们自己的 GitHub 仓库是协作与分享入口，不能假定上游接受 GitHub pull request。

## 提交前整理

1. 协调各地区负责人收尾，确认地区用词和贡献署名；对三份最新 PO 分别进行 GNU `msgfmt --check` 和关键界面验证。格式通过不等于母语者或领域审核完成。
2. 三份 PO 已补齐实际修订日期、用户确认的署名 Hamster Park (Yuanhao Lyu) 和项目团队链接，并在注释中注明 GPT-6.1 Terra、Grok 4.7、DeepSeek V4.1 Flash 的辅助贡献。后续修改时更新修订日期。
3. 与上游当前开发模板对照，合并新旧字符串并复核遗漏；目前基准为 2.71 正式版，并非保证与开发版完全相同。
4. 保持 `Volume` 未翻译，并说明它同时表示物理体积与体数据类型，希望上游为不同语境提供 gettext 上下文；应由上游决定兼容实现。
5. 按实际版权和许可确认贡献授权。GTK、GLib 的中文组件翻译来自 GNOME，保留原始署名和独立许可，不当作 Gwyddion 项目原创提交。
6. 更新并推送最终 PO、审校记录与清晰的项目状态；给上游的链接应指向实际准备提交的版本，而不是仍在修改的工作副本。

## 发送前复核

详见 [发送前检查记录](PRE_SUBMISSION_CHECK.md)。发送时直接附上 `translations/zh_CN.po`、`translations/zh_HK.po`、`translations/zh_TW.po`，同时保留 GitHub 链接；不要附上工作批次或 GTK/GLib 测试包。以下为邮件草稿，尚未发送。

## 英文邮件草稿

收件人：yeti@gwyddion.net

主题：Chinese translations for Gwyddion (zh_CN, zh_HK, zh_TW)

Hello David,

I would like to contribute three Chinese interface translations for Gwyddion, based on the 2.71 translation template. The following PO files are attached:

- zh_CN.po — Simplified Chinese
- zh_HK.po — Traditional Chinese for Hong Kong and Macau
- zh_TW.po — Traditional Chinese for Taiwan

The files and project notes are also available on GitHub:
https://github.com/HamsterPark/gwyddion-zh

The translation and proofreading work was assisted by GPT-6.1 Terra, Grok 4.7, and DeepSeek V4.1 Flash. All three catalogs pass GNU `msgfmt --check`.

One string, “Volume”, remains untranslated because it is shared between physical volume and the volume-data type, which require different Chinese terms. Could these uses be given separate gettext contexts?

We would be glad to contribute these translations for inclusion in Gwyddion. Please let me know if any changes or further testing are needed.

Thank you for your work on Gwyddion!

Best regards,

Hamster Park (Yuanhao Lyu)
