# -*- coding: utf-8 -*-
"""端到端测试论文质量检测工具"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '竞赛资料', '06-论文质量检测工具'))

from main import analyze_one

path = r'C:\Users\12258\Desktop\PythonWork\diangong_2026\zhongqingbei2026A_results\论文.md'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

sample = text[:5000]
r = analyze_one(sample)
print('END-TO-END TEST PASSED')
print('TOPSIS:', r['topsis_score'], '[' + r['grade'] + ']')
print('AI Score:', r['ai_score'])
print('Dimensions:', r['dimensions'])
