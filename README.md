
#  数学建模论文质量检测工具

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Status](https://img.shields.io/badge/status-active-brightgreen.svg)

**论文自动评分 + AI 痕迹检测一体化工具**，基于熵权-CRITIC组合赋权与TOPSIS法，实现数学建模竞赛论文的量化评估与AI生成痕迹检测。

---
## 项目介绍

这个项目源于2026年中青杯数学建模的A题，看到A题时就感觉这个东西有意思，完成A题后感觉这个还算有点用处，就放到了GitHub上，论文为[相关论文/文档](./A202603209.pdf)，各位如果有兴趣可以看看

##  核心功能

- **22项量化指标** – 覆盖结构完整性、逻辑严密性、方法合理性、创新性、规范性五个维度
- **熵权-CRITIC + TOPSIS** – 客观赋权与多属性综合评分
- **AI痕迹检测** – 6项统计指标识别AI生成文本（n-gram突现度、句长方差系数、类符形符比、信息熵、三词重复率、句长分布偏度）
- **自动评级** – 优秀 / 良好 / 中等 / 及格 / 不及格

---

##  项目结构

```
MathModelEvaluator/
├── README.md              # 使用说明
├── main.py                # 主入口
├── utils/reader.py        # 支持 .md / .docx / .pdf
├── extractors/
│   ├── indicators.py      # 22项指标提取
│   └── ai_detection.py    # 6指标AI痕迹检测
├── scorers/weighting.py   # 熵权-CRITIC + TOPSIS 评分
└── sample/test_e2e.py     # 端到端测试
```

---

##  输入格式

| 格式 | 说明 |
|------|------|
| `.md` | Markdown 论文源码（**推荐**） |
| `.docx` | Word 文档 |
| `.pdf` | PDF 论文（需安装 `pdfplumber`） |

---

##  快速开始

```bash
# 单篇检测
python main.py 论文.md

# 批量检测
python main.py 论文目录/

# 输出 JSON 报告
python main.py 论文.md -o report.json
```

---

## 输出内容

- 五项维度得分
- TOPSIS 综合评分与等级
- AI 检测 6 指标明细
- 综合 AI 评分
- 关键特征识别结果

---

## 依赖安装

```bash
# 核心依赖
pip install numpy pandas scipy scikit-learn

# PDF 支持（可选）
pip install pdfplumber

# DOCX 支持（可选）
pip install python-docx
```

---

##  License

本项目基于 [MIT License](LICENSE) 开源。

