# -*- coding: utf-8 -*-
"""6指标AI生成痕迹检测"""
import re, numpy as np, pandas as pd
from collections import Counter

def cn(text): return re.findall(r'[\u4e00-\u9fff]', text)
def en(text): return re.findall(r'[a-zA-Z]+', text)
def _sentences(text): return [s.strip() for s in re.split(r'[。！？\n]', text) if len(s.strip()) > 5]

def B(text, n=3):
    """n-gram突现度 — CV of n-gram frequencies"""
    chars = cn(text) + en(text)
    freqs = list(Counter(tuple(chars[i:i+n]) for i in range(len(chars)-n+1)).values())
    return np.std(freqs)/np.mean(freqs) if freqs and np.mean(freqs)>0 else 0.0

def CV_len(text):
    """句长方差系数"""
    lens = [len(s) for s in _sentences(text)]
    return np.std(lens)/np.mean(lens) if lens and np.mean(lens)>0 else 0.0

def TTR(text):
    """类符形符比"""
    c = cn(text)
    return len(set(c))/len(c) if c else 0.0

def unigram_entropy(text):
    """单字信息熵 (bits/char)"""
    c = cn(text)
    probs = np.array(list(Counter(c).values()))/len(c)
    return -np.sum(probs*np.log2(probs))

def repetitiveness(text, n=3):
    """三词重复率"""
    chars = cn(text)+en(text)
    ngrams = [tuple(chars[i:i+n]) for i in range(len(chars)-n+1)]
    counts = Counter(ngrams)
    return sum(c for c in counts.values() if c>1)/len(ngrams) if ngrams else 0.0

def skewness(text):
    """句长分布偏度"""
    lens = [len(s) for s in _sentences(text)]
    return float(pd.Series(lens).skew()) if len(lens)>=3 else 0.0

def detect(text):
    """返回6项AI检测指标"""
    return {
        'B': round(B(text), 4),
        'CV_len': round(CV_len(text), 4),
        'TTR': round(TTR(text), 4),
        'entropy': round(unigram_entropy(text), 4),
        'repetitiveness': round(repetitiveness(text), 4),
        'skewness': round(skewness(text), 4),
    }

def ai_score(metrics_dict):
    """6指标加权融合 AI评分 (0~1, 越高越像AI)"""
    df = pd.DataFrame([metrics_dict])
    def norm(s):
        mn, mx = s.min(), s.max()
        return (s-mn)/(mx-mn) if mx>mn else pd.Series([0.5]*len(s))
    df['B_n'] = 1-norm(df['B']); df['CV_n'] = 1-norm(df['CV_len'])
    df['TTR_n'] = 1-norm(df['TTR']); df['H_n'] = norm(df['entropy'])
    df['R3_n'] = norm(df['repetitiveness']); df['Sk_n'] = 1-norm(df['skewness'].abs())
    val = (0.25*df['B_n'] + 0.20*df['CV_n'] + 0.15*df['TTR_n']
          + 0.15*df['H_n'] + 0.15*df['R3_n'] + 0.10*df['Sk_n']).iloc[0]
    return round(float(val), 4)
