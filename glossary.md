# Gwyddion 中文术语表（简体初稿）

本表目前仅为简体中文的翻译协作暂定约定；香港／澳门与台湾繁体术语及地区差异另行审校。本表，不代表 Gwyddion 官方中文译名。请结合界面位置、源代码和实际功能审校；有歧义的词不要机械替换。遇到可能改变科学含义的译法，请记录待讨论项。术语也应根据词性与上下文灵活调整。

| 英文 | 建议译法 | 说明 |
| --- | --- | --- |
| scanning probe microscopy (SPM) | 扫描探针显微术 | 指技术；仪器译为扫描探针显微镜。 |
| atomic force microscopy (AFM) | 原子力显微术 | 指仪器时译为原子力显微镜。 |
| scanning tunnelling microscopy (STM) | 扫描隧道显微术 | 指仪器时译为扫描隧道显微镜。 |
| topography | 表面形貌 | 不宜在此领域一律译为地形。 |
| height field | 高度场 | 与普通图像区分。 |
| levelling / level | 调平 | 指去除倾斜或背景；其他语境依实际含义翻译。 |
| Plane Level | 平面调平 | 拟合并减去平面。 |
| Facet Level | 面片调平 | 根据局部面片方向估计调平平面；涉及实际晶体学晶面时，facet 可按上下文译为晶面。 |
| Flatten Base | 基底平坦化 | 针对平坦基底处理，与平面调平区分。 |
| background subtraction | 背景扣除 | 与基底平坦化区分。 |
| line correction | 扫描线校正 | 用于修正扫描线之间或扫描线内部的缺陷。 |
| Align Rows | 对齐扫描行 | 区分对整幅图像的配准。 |
| Step Line Correction | 扫描线阶跃校正 | 处理扫描线中的高度突变。 |
| artefact / artifact | 伪影 | 指测量或处理引入的非真实特征。 |
| mask | 掩膜 | 标记或限制处理区域；建议统一使用掩膜。 |
| grain | 颗粒 | 在 Gwyddion 的分割语境中指一个被标记的区域，不必然是物理晶粒。 |
| grain boundary | 颗粒边界 | 明确涉及晶体学晶界时按上下文翻译。 |
| watershed | 分水岭 | 图像分割算法。 |
| tip | 探针尖端 / 针尖 | 在扫描探针语境中；提示信息语境则另译。 |
| tip convolution | 针尖卷积 | 表示测量形貌受针尖几何形状影响。 |
| tip reconstruction | 针尖重建 | 与数据反卷积区分。 |
| blind tip estimation | 盲针尖估计 | 根据测量数据估计针尖形状。 |
| deconvolution | 反卷积 | 与卷积区分。 |
| roughness | 粗糙度 | 具体统计量需保留原有符号和定义。 |
| waviness | 波纹度 | 与粗糙度区分。 |
| root mean square roughness | 均方根粗糙度 | 保留 Sq、Rq 等具体符号。 |
| skewness | 偏度 | 保留具体统计量的符号。 |
| kurtosis / excess kurtosis | 峰度 / 超额峰度 | 两者不能混同；Gwyddion 手册中相关统计量采用超额峰度。 |
| autocorrelation function (ACF) | 自相关函数 | 可保留 ACF 缩写。 |
| height-height correlation function (HHCF) | 高度-高度相关函数 | 与自相关函数区分。 |
| power spectral density (PSD) | 功率谱密度 | 可保留 PSD 缩写。 |
| force curve | 力曲线 | 具体含义视轴和测量方式而定。 |
| curve map | 曲线图谱 | 空间位置对应曲线的数据，与单个曲线图区分。 |
| volume data | 体数据 | 也可能用于表示图像堆栈。 |
| trace / retrace | 正向扫描 / 反向扫描 | 仅用于扫描方向语境；其他语境按含义翻译。 |
| outlier | 异常值 | 具体处理方式视功能而定。 |

## 主要依据

- [Gwyddion 用户手册：数据调平与背景扣除](https://gwyddion.net/documentation/user-guide-en/leveling-and-background.html)，用于区分平面调平、面片调平及基底平坦化等操作。
- [Gwyddion 用户手册：扫描线伪影](https://gwyddion.net/documentation/user-guide-en/scan-line-defects.html)，用于理解扫描线相关的校正方法。
- [Gwyddion 用户手册：统计分析](https://gwyddion.net/documentation/user-guide-en/statistical-analysis.html)，用于区分超额峰度、自相关函数、高度-高度相关函数及功率谱密度。
- [Gwyddion 用户手册：图像堆栈](https://gwyddion.net/documentation/user-guide-en/image-stacks-processing.html)，说明体数据可用于表示图像堆栈。

上述官方页面用于核对功能含义，并非中文译名来源。

