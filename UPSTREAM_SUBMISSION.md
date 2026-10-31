# 向 Gwyddion 上游提交中文翻译

## 官方渠道

[官方翻译贡献指南](https://gwyddion.net/contribute.php)要求使用 UTF-8 PO 文件，并说明即使是部分翻译也可以提交；翻译成果可发送给协调翻译工作的 David Nečas（Yeti）。[官方联系页](https://gwyddion.net/contact.php)列出的翻译联系人为 `yeti@gwyddion.net`，同时建议一般开发讨论通过 [gwyddion-devel 邮件列表](https://sourceforge.net/p/gwyddion/mailman/gwyddion-devel/)公开进行。

邮件列表只接受已订阅地址发帖；官方说明未订阅或附件过大的邮件会被丢弃，即使自动回复显示等待审核。适合在讨论中提供公开仓库的链接，不要直接发送大附件。SourceForge 的 Web 论坛也是选择，但发帖需要登录。

上游 SVN 是主要源码库，仓库写权限按既有贡献情况单独授予；我们自己的 GitHub 仓库是协作与分享入口，不能假定上游接受 GitHub pull request。

## 提交前整理

1. 协调各地区负责人收尾，确认地区用词和贡献署名；对三份最新 PO 分别进行 GNU `msgfmt --check` 和关键界面验证。格式通过不等于母语者或领域审核完成。
2. 检查 PO 的真实修订日期、译者和语言团队元数据；简体文件目前缺相关头字段，不要虚构身份或邮箱。香港、台湾 PO 文件的作者与团队信息也应由参与者确认。
3. 与上游当前开发模板对照，合并新旧字符串并复核遗漏；目前基准为 2.71 正式版，并非保证与开发版完全相同。
4. 保持 `Volume` 未翻译，并说明它同时表示物理体积与体数据类型，希望上游为不同语境提供 gettext 上下文；应由上游决定兼容实现。
5. 按实际版权和许可确认贡献授权。GTK、GLib 的中文组件翻译来自 GNOME，保留原始署名和独立许可，不当作 Gwyddion 项目原创提交。
6. 更新并推送最终 PO、审校记录与清晰的项目状态；给上游的链接应指向实际准备提交的版本，而不是仍在修改的工作副本。

## 英文邮件初稿

收件人：yeti@gwyddion.net

主题：Chinese translations for Gwyddion and a translation context question

Hello David,

I have prepared Simplified Chinese, Traditional Chinese (Hong Kong), and Traditional Chinese (Taiwan) interface translations for Gwyddion, based on the 2.71 translation template. The translations were developed with assistance from GPT-6.1 Terra, Grok 4.7, and DeepSeek V4.1 Flash.

The files are available at https://github.com/HamsterPark/gwyddion-zh.

The catalogs pass `msgfmt --check`. One string, “Volume”, is shared between a physical measurement and the volume-data type, so we have left it untranslated. Would it be possible to give these uses separate gettext contexts?

Could you advise us on the preferred way to submit the PO files and any additional review or testing you would like us to complete?

Thank you for your work on Gwyddion.

Best regards,

Hamster Park (Yuanhao Lyu)
