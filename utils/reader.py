# -*- coding: utf-8 -*-
"""论文读取器 — 支持 .md / .docx / .pdf"""
import os, re

def read(path):
    ext = os.path.splitext(path)[1].lower()
    if ext == '.md':
        return _read_md(path)
    elif ext == '.docx':
        return _read_docx(path)
    elif ext == '.pdf':
        return _read_pdf(path)
    else:
        raise ValueError(f'不支持的格式: {ext}')

def _read_md(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def _read_docx(path):
    try:
        from docx import Document
        doc = Document(path)
        return '\n'.join(p.text for p in doc.paragraphs)
    except ImportError:
        raise ImportError('需安装 python-docx: pip install python-docx')

def _read_pdf(path):
    try:
        import pdfplumber
        with pdfplumber.open(path) as pdf:
            return '\n'.join(page.extract_text() or '' for page in pdf.pages)
    except ImportError:
        raise ImportError('需安装 pdfplumber: pip install pdfplumber')
