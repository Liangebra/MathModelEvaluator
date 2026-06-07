# 数学建模论文质量检测工具

## 用途

论文自动评分 + AI痕迹检测一体化工具。支持：
- **22项量化指标**评价（5维度：结构/逻辑/方法/创新/规范）
- **熵权-CRITIC组合赋权 + TOPSIS评分**
- **6指标AI生成痕迹检测**（n-gram突现度/句长方差/类符形符比/信息熵/三词重复率/句长偏度）
- **自动评级**（优秀/良好/中等/及格/不及格）

## 输入格式

支持三种输入：

| 格式 | 说明 |
|------|------|
| `.md` | Markdown论文源码（推荐） |
| `.docx` | Word文档 |
| `.pdf` | PDF论文（需安装pdfplumber） |

## 快速开始

```bash
# 单篇检测
python main.py 论文.md

# 批量检测
python main.py 论文目录/

# 输出JSON报告
python main.py 论文.md -o report.json
```

## 输出内容

- 五项维度得分
- TOPSIS综合评分与等级
- AI检测6指标明细
- 综合AI评分
- 关键特征识别结果

## 依赖

```bash
pip install numpy pandas scipy scikit-learn
# PDF支持（可选）
pip install pdfplumber
# DOCX支持（可选）
pip install python-docx
```
