# -*- coding: utf-8 -*-
"""赋权方法: 熵权法 + CRITIC法 + TOPSIS评分 + 分级"""
import numpy as np, math

def entropy_weight(X):
    """熵权法"""
    X = np.array(X)
    X_norm = X / np.sum(X, axis=0, keepdims=True)
    X_norm = np.clip(X_norm, 1e-12, 1)
    k = 1.0 / math.log(X.shape[0])
    e = -k * np.sum(X_norm * np.log(X_norm), axis=0)
    return (1 - e) / np.sum(1 - e)

def critic_weight(X):
    """CRITIC法"""
    X = np.array(X)
    std = np.std(X, axis=0, ddof=1)
    conflict = np.sum(1 - np.abs(np.corrcoef(X.T)), axis=1)
    C = std * conflict
    return C / np.sum(C)

def combined_weight(X):
    """熵权-CRITIC组合赋权"""
    w_e = entropy_weight(X)
    w_c = critic_weight(X)
    return np.sqrt(w_e * w_c) / np.sum(np.sqrt(w_e * w_c))

def topsis(X, weights, reference_max=None, reference_min=None):
    """TOPSIS评分 (越高越好)"""
    X = np.array(X)
    if X.shape[0] == 1 or reference_max is not None:
        # 单样本模式：用参考范围[0,1]或固定理想解
        ideal_best = np.ones(X.shape[1]) if reference_max is None else np.array(reference_max)
        ideal_worst = np.zeros(X.shape[1]) if reference_min is None else np.array(reference_min)
    else:
        ideal_best = np.max(X, axis=0)
        ideal_worst = np.min(X, axis=0)
    db = np.sqrt(np.sum(weights * (X - ideal_best)**2, axis=1))
    dw = np.sqrt(np.sum(weights * (X - ideal_worst)**2, axis=1))
    score = dw / (db + dw)
    # 处理全0退化为0.5
    score = np.nan_to_num(score, nan=0.5)
    return score

def assign_grade(scores):
    """五级分级"""
    p = [np.percentile(scores, 85), np.percentile(scores, 65),
         np.percentile(scores, 40), np.percentile(scores, 15)]
    return ['优秀' if s>=p[0] else '良好' if s>=p[1] else '中等' if s>=p[2] else '及格' if s>=p[3] else '不及格' for s in scores]
