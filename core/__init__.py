#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Stock Analysis SaaS - 股票分析核心模块

提供完整的技术分析和基本面分析功能

模块结构:
- core/
    - stock_analyzer.py    # 股票分析器主模块
    - technical_indicators.py  # 技术指标库
    - fundamental_analysis.py   # 基本面分析模块
- tests/                      # 单元测试

作者: Stock Analysis SaaS
版本: 1.0.0
"""

__version__ = '1.0.0'
__author__ = 'Stock Analysis SaaS'

from core.stock_analyzer import StockAnalyzer
from core.technical_indicators import TechnicalIndicators
from core.fundamental_analysis import FundamentalAnalyzer

__all__ = [
    'StockAnalyzer',
    'TechnicalIndicators',
    'FundamentalAnalyzer'
]
