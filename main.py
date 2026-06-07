# -*- coding: utf-8 -*-
"""论文质量检测工具 — 主入口"""
import json, os, sys
import numpy as np

from utils.reader import read
from extractors.indicators import extract
from extractors.ai_detection import detect, ai_score
from scorers.weighting import topsis, assign_grade

# 固定赋权权重（来自30篇训练论文训练结果）
WEIGHTS = {
    'structure': 0.1963,
    'logic': 0.2486,
    'method': 0.2568,
    'innovation': 0.1960,
    'normative': 0.1024,
}

def analyze_one(text):
    """对单篇论文做完整检测"""
    features, dims = extract(text)
    dim_names = ['structure', 'logic', 'method', 'innovation', 'normative']
    dim_vals = np.array([[dims[k] for k in dim_names]])
    w = np.array([WEIGHTS[k] for k in dim_names])
    score = float(topsis(dim_vals, w)[0])
    grade = assign_grade([score])[0]
    ai_metrics = detect(text)
    ai = ai_score(ai_metrics)
    return {
        'dimensions': {k: round(dims[k], 4) for k in dim_names},
        'topsis_score': round(score, 4),
        'grade': grade,
        'ai_metrics': ai_metrics,
        'ai_score': ai,
    }

def analyze_batch(texts):
    """批量检测"""
    results = []
    all_dims = []
    for text in texts:
        r = analyze_one(text)
        results.append(r)
        all_dims.append([r['dimensions'][k] for k in ['structure','logic','method','innovation','normative']])
    if len(all_dims) > 1:
        w = np.array([WEIGHTS[k] for k in ['structure','logic','method','innovation','normative']])
        scores = topsis(np.array(all_dims), w)
        grades = assign_grade(scores)
        for i, r in enumerate(results):
            r['topsis_score'] = round(float(scores[i]), 4)
            r['grade'] = grades[i]
    return results

def main():
    if len(sys.argv) < 2:
        print('用法: python main.py <论文路径.md/docx/pdf> 或 <目录> [-o output.json]')
        sys.exit(1)
    path = sys.argv[1]
    output_json = None
    if '-o' in sys.argv:
        idx = sys.argv.index('-o')
        if idx + 1 < len(sys.argv):
            output_json = sys.argv[idx + 1]

    if os.path.isdir(path):
        # 批量模式
        files = [f for f in os.listdir(path) if f.endswith(('.md','.docx','.pdf'))]
        texts, names = [], []
        for f in files:
            fp = os.path.join(path, f)
            try:
                texts.append(read(fp))
                names.append(f)
            except Exception as e:
                print(f'[跳过] {f}: {e}')
        results = analyze_batch(texts)
        for name, r in zip(names, results):
            _print_result(name, r)
    else:
        # 单篇模式
        text = read(path)
        r = analyze_one(text)
        _print_result(os.path.basename(path), r)

    if output_json:
        with open(output_json, 'w', encoding='utf-8') as f:
            json.dump(results if os.path.isdir(path) else [r], f, ensure_ascii=False, indent=2)
        print(f'\n[结果已保存] {output_json}')

def _print_result(name, r):
    print(f'\n{"="*50}')
    print(f'论文: {name}')
    print(f'{"="*50}')
    print(f'五维评分: {r["dimensions"]}')
    print(f'TOPSIS综合: {r["topsis_score"]}  [{r["grade"]}]')
    print(f'AI检测: {r["ai_metrics"]}')
    print(f'AI评分: {r["ai_score"]} (越高=AI特征越明显)')

if __name__ == '__main__':
    main()
