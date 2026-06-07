# -*- coding: utf-8 -*-
"""22项二级指标提取"""
import re, math
import numpy as np

# ===== 全局词表 =====
LOGICAL_CONNECTIVES = ['因此','所以','由于','从而','因而','由此','据此','故而',
    '因为','如果','则','那么','假设','若','否则','不然',
    '虽然','但是','然而','不过','尽管','却','可是',
    '不仅','而且','并且','同时','此外','另外','还',
    '首先','其次','最后','综上','综上所述',
    '即','也就是说','换言之','换句话说',
    '例如','比如','譬如','以','为例',
    '基于此','据此','鉴于此','反之','相反',
    '一是','二是','三是','第一','第二','第三','其一','其二','其三']

CAUSAL_PAIRS = ['因为','所以','由于','因此','因而','从而','导致','造成','引起','使得','促使','源于','源自']

METHOD_KEYWORDS = ['模型','算法','方法','优化','预测','评价','回归',
    '神经网络','决策','规划','聚类','分类','仿真',
    'AHP','TOPSIS','熵权','灰色关联','模糊',
    '遗传算法','粒子群','规划','微分方程','马尔科夫',
    '时间序列','ARIMA','LSTM','XGBoost','随机森林',
    '主成分','因子分析','灵敏度','稳健性','Monte Carlo']

def extract(text, num_pages=None):
    """提取全部22项指标"""
    if num_pages is None:
        num_pages = max(len(text) // 1500, 1)
    S = _extract_S(text, num_pages)
    L = _extract_L(text)
    M = _extract_M(text)
    I = _extract_I(text)
    N = _extract_N(text, num_pages)
    features = {**S, **L, **M, **I, **N}
    # 计算5维度得分
    dims = {
        'structure':  np.mean([S[k] for k in S]),
        'logic':      np.mean([L[k] for k in L]),
        'method':     np.mean([M[k] for k in M]),
        'innovation': np.mean([I[k] for k in I]),
        'normative':  np.mean([N[k] for k in N]),
    }
    return features, dims

def _extract_S(text, num_pages):
    S = {}
    clean = text.replace('---PAGE BREAK---', '')
    S['S1'] = max(0, 1 - abs(num_pages - 20) / 40) if num_pages <= 60 else 0.0
    sections = set()
    for pat in [r'(?:^|\n)\s*[一二三四五六七八九十]+[、\.\s]',
                r'(?:^|\n)\s*\d+[\.\、\s][^\n]{0,20}',
                r'(?:^|\n)\s*第[一二三四五六七八九十]+[章节部分]']:
        for m in re.finditer(pat, clean): sections.add(m.group().strip()[:30])
    S['S2'] = min(len(sections) / 8.0, 1.0)
    abs_match = re.search(r'摘[要][：:\s][\s\S]{0,800}关键[词字]', clean[:5000])
    S['S3'] = (1 if abs_match else 0) * min(len(abs_match.group())/300.0 if abs_match else 0, 1.0)
    S['S4'] = 1.0 if re.search(r'(?:^|\n)\s*(?:[4567][\.\、]?\s*(?:结论|总结)|结论与)', clean) else 0.0
    S['S5'] = min(len(re.findall(r'\[\d+\]', clean)) / 15.0, 1.0)
    return S

def _extract_L(text):
    L = {}; clean = text.replace('---PAGE BREAK---', '')
    words = [w for w in list(clean) if w.strip()]; Nw = max(len(words), 1)
    sents = [s.strip() for s in re.split(r'[。！？\n]+', clean) if len(s.strip()) > 5]
    Ns = max(len(sents), 1)
    L['L1'] = sum(clean.count(c) for c in LOGICAL_CONNECTIVES) / Nw
    L['L2'] = sum(clean.count(c) for c in CAUSAL_PAIRS) / Ns
    cc = {c: clean.count(c) for c in LOGICAL_CONNECTIVES if clean.count(c) > 0}
    if cc:
        t = sum(cc.values()); en = -sum((c/t)*math.log(c/t) for c in cc.values())
        L['L3'] = en / math.log(len(cc)) if len(cc) > 0 else 0
    else: L['L3'] = 0.0
    L['L4'] = (1 if any(k in clean for k in ['假设','假定','条件','前提']) else 0 +
               1 if any(k in clean for k in ['结论','验证','检验']) else 0) / 2.0
    paras = [p.strip() for p in clean.split('\n') if len(p.strip()) > 20]
    L['L5'] = min(sum(1 for i in range(len(paras)-1)
               if any(c in paras[i] for c in LOGICAL_CONNECTIVES)) / max(len(paras)-1,1), 1.0) if len(paras)>=2 else 0.0
    return L

def _extract_M(text):
    M = {}; clean = text.replace('---PAGE BREAK---', '')
    M['M1'] = min(sum(clean.count(k) for k in METHOD_KEYWORDS) / 20.0, 1.0)
    fc = len(re.findall(r'$$\d+$$', clean)) + len(re.findall(r'（\d+）', clean))
    fc += len(re.findall(r'[=≤≥≈≠∑∫]', clean)) // 5
    M['M2'] = 0.5*min(fc/30.0,1.0)+0.3*min(sum(clean.count(k) for k in ['因此','由','可得','代入','整理']) /5,1)+0.2*min(fc/20,1)
    pk = ['参数','系数','权重','阈值','取值','α','β','γ','λ']
    M['M3'] = min(sum(clean.count(k) for k in pk) / 20.0, 1.0)
    vk = ['验证','检验','测试','对比','误差','精度','R²','RMSE']
    M['M4'] = min(sum(clean.count(k) for k in vk) / 10.0, 1.0)
    M_kp = set(re.findall(r'优化|预测|评价|回归|分类|聚类|仿真', clean[:200]))
    M_ap = set(re.findall(r'优化|预测|评价|回归|分类|聚类|仿真', clean[-500:]))
    M['M5'] = len(M_kp & M_ap) / max(len(M_kp | M_ap), 1) if (M_kp | M_ap) else 0.5
    return M

def _extract_I(text):
    I = {}; clean = text.replace('---PAGE BREAK---', '')
    adv = ['改进','融合','混合','组合','多目标','深度学习','LSTM','贝叶斯','自适应']
    I['I1'] = min(sum(clean.count(k) for k in adv) / 15.0, 1.0)
    imp = ['改进','优化','提升','修正','扩展','推广']
    I['I2'] = min(sum(clean.count(k) for k in imp) / 10.0, 1.0)
    cmp = ['对比','比较','优于','高于','低于','更优','基准']
    I['I3'] = min(sum(clean.count(k) for k in cmp) / 8.0, 1.0)
    th = ['定理','证明','推导','收敛性','稳定性','最优性']
    I['I4'] = min(sum(clean.count(k) for k in th) / 8.0, 1.0)
    I['I5'] = min(len([k for k in ['融合','结合','组合'] if k in clean]) / 8.0, 1.0)
    return I

def _extract_N(text, num_pages):
    N = {}; clean = text.replace('---PAGE BREAK---', '')
    t = len(re.findall(r'$$\d+$$', clean))
    N['N1'] = min(t / 15.0, 1.0) if t > 0 else 0.5
    N['N2'] = min((len(re.findall(r'图\s*\d+', clean)) + len(re.findall(r'表\s*\d+', clean))) / max(num_pages,1) * 5, 1.0)
    N['N3'] = 0.5
    nt = ['s.t.','min','max','∑','∫','∈','→']
    N['N4'] = sum(1 for k in nt if k in clean) / len(nt)
    return N
