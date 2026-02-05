#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
基本面分析模块
提供股票基本面分析和筛选功能

支持的功能:
- PE/PB筛选
- ROE排名
- 股息率计算
- 财务指标整合
- 综合评分

作者: Stock Analysis SaaS
版本: 1.0.0
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple, Union
from dataclasses import dataclass
from datetime import datetime, timedelta


@dataclass
class ValuationMetrics:
    """估值指标"""
    pe: float  # 市盈率
    pb: float  # 市净率
    ps: Optional[float] = None  # 市销率
    pcf: Optional[float] = None  # 市现率
    market_cap: Optional[float] = None  # 市值


@dataclass
class FinancialMetrics:
    """财务指标"""
    roe: float  # 净资产收益率
    netprofit_margin: Optional[float] = None  # 净利润率
    grossprofit_margin: Optional[float] = None  # 毛利率
    revenue_growth: Optional[float] = None  # 营收增长率
    profit_growth: Optional[float] = None  # 利润增长率


@dataclass
class DividendMetrics:
    """股息指标"""
    dividend_ratio: float  # 股息率 (%)
    dividend_per_share: Optional[float] = None  # 每股股息
    payout_ratio: Optional[float] = None  # 分红比例


@dataclass
class CompositeScore:
    """综合评分结果"""
    total_score: float
    pe_score: float
    pb_score: float
    roe_score: float
    dividend_score: float
    liquidity_score: float
    score_breakdown: Dict


class FundamentalAnalyzer:
    """
    基本面分析器
    
    提供完整的基本面分析功能，
    包括估值分析、财务分析、股息分析
    """
    
    # 默认筛选条件
    DEFAULT_FILTERS = {
        'pe_min': 0,
        'pe_max': 50,
        'pb_min': 0,
        'pb_max': 5,
        'roe_min': 5,
        'dividend_min': 1,
        'turnover_rate_min': 0.5,
        'turnover_rate_max': 15,
        'market_cap_min': None  # 无最小市值限制
    }
    
    # 默认评分权重
    DEFAULT_WEIGHTS = {
        'pe_weight': 0.25,
        'pb_weight': 0.20,
        'roe_weight': 0.25,
        'dividend_weight': 0.20,
        'liquidity_weight': 0.10
    }
    
    def __init__(self, data: pd.DataFrame = None):
        """
        初始化基本面分析器
        
        Args:
            data: 股票数据DataFrame
        """
        self.data = data
    
    def set_data(self, data: pd.DataFrame) -> None:
        """
        设置分析数据
        
        Args:
            data: 股票数据DataFrame
        """
        self.data = data
    
    # ==================== 筛选功能 ====================
    
    def filter_stocks(
        self,
        filters: Dict = None,
        data: pd.DataFrame = None
    ) -> pd.DataFrame:
        """
        根据基本面条件筛选股票
        
        Args:
            filters: 筛选条件字典，如果为None使用默认条件
            data: 分析数据，如果为None使用初始化时的数据
        
        Returns:
            pd.DataFrame: 筛选后的股票数据
        """
        if data is None:
            data = self.data
        
        if data is None or data.empty:
            raise ValueError("没有提供分析数据")
        
        if filters is None:
            filters = self.DEFAULT_FILTERS
        
        df = data.copy()
        
        # PE筛选
        if 'pe' in df.columns:
            if filters.get('pe_min') is not None:
                df = df[df['pe'] > filters['pe_min']]
            if filters.get('pe_max') is not None:
                df = df[df['pe'] < filters['pe_max']]
        
        # PB筛选
        if 'pb' in df.columns:
            if filters.get('pb_min') is not None:
                df = df[df['pb'] > filters['pb_min']]
            if filters.get('pb_max') is not None:
                df = df[df['pb'] < filters['pb_max']]
        
        # ROE筛选
        if 'roe' in df.columns:
            if filters.get('roe_min') is not None:
                df = df[df['roe'] > filters['roe_min']]
        
        # 股息率筛选
        if 'dv_ratio' in df.columns:
            if filters.get('dividend_min') is not None:
                df = df[df['dv_ratio'] > filters['dividend_min']]
        
        # 换手率筛选
        if 'turnover_rate' in df.columns:
            if filters.get('turnover_rate_min') is not None:
                df = df[df['turnover_rate'] > filters['turnover_rate_min']]
            if filters.get('turnover_rate_max') is not None:
                df = df[df['turnover_rate'] < filters['turnover_rate_max']]
        
        # 市值筛选
        if 'market_cap' in df.columns:
            if filters.get('market_cap_min') is not None:
                df = df[df['market_cap'] > filters['market_cap_min']]
        
        return df
    
    # ==================== 评分功能 ====================
    
    def calculate_composite_score(
        self,
        weights: Dict = None,
        data: pd.DataFrame = None
    ) -> pd.DataFrame:
        """
        计算基本面综合评分
        
        评分维度:
        - PE (市盈率): 越低越好
        - PB (市净率): 越低越好
        - ROE (净资产收益率): 越高越好
        - 股息率: 越高越好
        - 成交量: 适中最好
        
        Args:
            weights: 评分权重字典
            data: 分析数据
        
        Returns:
            pd.DataFrame: 包含评分结果的数据
        """
        if data is None:
            data = self.data
        
        if data is None or data.empty:
            raise ValueError("没有提供分析数据")
        
        if weights is None:
            weights = self.DEFAULT_WEIGHTS
        
        df = data.copy()
        
        # 1. PE评分 (越低越好)
        if 'pe' in df.columns:
            df['pe_score'] = df['pe'].apply(
                lambda x: 100 if pd.isna(x) or x <= 0 
                else max(0, min(100, 50 - (x - 10) * 2))
            )
        else:
            df['pe_score'] = 50
        
        # 2. PB评分 (越低越好)
        if 'pb' in df.columns:
            df['pb_score'] = df['pb'].apply(
                lambda x: 100 if pd.isna(x) or x <= 0 
                else max(0, min(100, 40 - (x - 1) * 10))
            )
        else:
            df['pb_score'] = 50
        
        # 3. ROE评分 (越高越好)
        if 'roe' in df.columns:
            df['roe_score'] = df['roe'].apply(
                lambda x: 100 if pd.isna(x) 
                else min(100, max(0, x * 10))
            )
        else:
            df['roe_score'] = 50
        
        # 4. 股息率评分 (越高越好)
        if 'dv_ratio' in df.columns:
            df['dividend_score'] = df['dv_ratio'].apply(
                lambda x: 100 if pd.isna(x) 
                else min(100, x * 20)
            )
        else:
            df['dividend_score'] = 50
        
        # 5. 流动性评分 (成交率适中为佳)
        if 'turnover_rate' in df.columns:
            df['liquidity_score'] = df['turnover_rate'].apply(
                lambda x: 50 if pd.isna(x) 
                else min(100, max(0, 50 - abs(x - 3) * 10))
            )
        else:
            df['liquidity_score'] = 50
        
        # 计算综合评分
        df['composite_score'] = (
            df['pe_score'] * weights.get('pe_weight', 0.25) +
            df['pb_score'] * weights.get('pb_weight', 0.20) +
            df['roe_score'] * weights.get('roe_weight', 0.25) +
            df['dividend_score'] * weights.get('dividend_weight', 0.20) +
            df['liquidity_score'] * weights.get('liquidity_weight', 0.10)
        )
        
        return df
    
    def get_stock_score(
        self,
        stock_data: Dict,
        weights: Dict = None
    ) -> CompositeScore:
        """
        获取单只股票的综合评分
        
        Args:
            stock_data: 股票数据字典
            weights: 评分权重
        
        Returns:
            CompositeScore: 综合评分结果
        """
        if weights is None:
            weights = self.DEFAULT_WEIGHTS
        
        # 计算各项评分
        pe = stock_data.get('pe', 0)
        pb = stock_data.get('pb', 0)
        roe = stock_data.get('roe', 0)
        dv_ratio = stock_data.get('dv_ratio', 0)
        turnover_rate = stock_data.get('turnover_rate', 3)
        
        # PE评分
        if pe <= 0 or pd.isna(pe):
            pe_score = 100
        else:
            pe_score = max(0, min(100, 50 - (pe - 10) * 2))
        
        # PB评分
        if pb <= 0 or pd.isna(pb):
            pb_score = 100
        else:
            pb_score = max(0, min(100, 40 - (pb - 1) * 10))
        
        # ROE评分
        if pd.isna(roe):
            roe_score = 50
        else:
            roe_score = min(100, max(0, roe * 10))
        
        # 股息评分
        if pd.isna(dv_ratio):
            dividend_score = 50
        else:
            dividend_score = min(100, dv_ratio * 20)
        
        # 流动性评分
        if pd.isna(turnover_rate):
            liquidity_score = 50
        else:
            liquidity_score = min(100, max(0, 50 - abs(turnover_rate - 3) * 10))
        
        # 综合评分
        total_score = (
            pe_score * weights.get('pe_weight', 0.25) +
            pb_score * weights.get('pb_weight', 0.20) +
            roe_score * weights.get('roe_weight', 0.25) +
            dividend_score * weights.get('dividend_weight', 0.20) +
            liquidity_score * weights.get('liquidity_weight', 0.10)
        )
        
        score_breakdown = {
            'pe_score': round(pe_score, 2),
            'pb_score': round(pb_score, 2),
            'roe_score': round(roe_score, 2),
            'dividend_score': round(dividend_score, 2),
            'liquidity_score': round(liquidity_score, 2)
        }
        
        return CompositeScore(
            total_score=round(total_score, 2),
            pe_score=round(pe_score, 2),
            pb_score=round(pb_score, 2),
            roe_score=round(roe_score, 2),
            dividend_score=round(dividend_score, 2),
            liquidity_score=round(liquidity_score, 2),
            score_breakdown=score_breakdown
        )
    
    # ==================== 排名功能 ====================
    
    def rank_by_roe(
        self,
        data: pd.DataFrame = None,
        ascending: bool = False,
        top_n: int = None
    ) -> pd.DataFrame:
        """
        按ROE排名
        
        Args:
            data: 分析数据
            ascending: 是否升序排列
            top_n: 返回前N名
        
        Returns:
            pd.DataFrame: 排名后的数据
        """
        if data is None:
            data = self.data
        
        if data is None or 'roe' not in data.columns:
            raise ValueError("数据中缺少ROE列")
        
        df = data.sort_values('roe', ascending=ascending)
        
        if top_n is not None:
            df = df.head(top_n)
        
        return df
    
    def rank_by_pe(
        self,
        data: pd.DataFrame = None,
        ascending: bool = True,
        top_n: int = None
    ) -> pd.DataFrame:
        """
        按PE排名（低估值优先）
        
        Args:
            data: 分析数据
            ascending: 是否升序排列
            top_n: 返回前N名
        
        Returns:
            pd.DataFrame: 排名后的数据
        """
        if data is None:
            data = self.data
        
        if data is None or 'pe' not in data.columns:
            raise ValueError("数据中缺少PE列")
        
        df = data.sort_values('pe', ascending=ascending)
        
        if top_n is not None:
            df = df.head(top_n)
        
        return df
    
    def rank_by_dividend(
        self,
        data: pd.DataFrame = None,
        ascending: bool = False,
        top_n: int = None
    ) -> pd.DataFrame:
        """
        按股息率排名
        
        Args:
            data: 分析数据
            ascending: 是否升序排列
            top_n: 返回前N名
        
        Returns:
            pd.DataFrame: 排名后的数据
        """
        if data is None:
            data = self.data
        
        if data is None or 'dv_ratio' not in data.columns:
            raise ValueError("数据中缺少股息率列")
        
        df = data.sort_values('dv_ratio', ascending=ascending)
        
        if top_n is not None:
            df = df.head(top_n)
        
        return df
    
    def rank_by_composite(
        self,
        data: pd.DataFrame = None,
        ascending: bool = False,
        top_n: int = None
    ) -> pd.DataFrame:
        """
        按综合评分排名
        
        Args:
            data: 分析数据
            ascending: 是否升序排列
            top_n: 返回前N名
        
        Returns:
            pd.DataFrame: 排名后的数据
        """
        if data is None:
            data = self.data
        
        if data is None:
            raise ValueError("没有提供分析数据")
        
        # 确保有综合评分
        if 'composite_score' not in data.columns:
            data = self.calculate_composite_score(data=data)
        
        df = data.sort_values('composite_score', ascending=ascending)
        
        if top_n is not None:
            df = df.head(top_n)
        
        return df
    
    # ==================== 估值分析 ====================
    
    def get_valuation_status(
        self,
        stock_data: Dict
    ) -> Tuple[str, Dict]:
        """
        获取股票估值状态
        
        Args:
            stock_data: 股票数据字典
        
        Returns:
            tuple: (估值状态, 详细指标)
        """
        pe = stock_data.get('pe', 0)
        pb = stock_data.get('pb', 0)
        
        pe_status = self._get_pe_status(pe)
        pb_status = self._get_pb_status(pb)
        
        # 综合估值判断
        if pe_status == '低估' and pb_status == '低估':
            valuation_status = '严重低估'
        elif pe_status == '低估' or pb_status == '低估':
            valuation_status = '相对低估'
        elif pe_status == '高估' and pb_status == '高估':
            valuation_status = '严重高估'
        elif pe_status == '高估' or pb_status == '高估':
            valuation_status = '相对高估'
        else:
            valuation_status = '估值合理'
        
        details = {
            'pe': pe,
            'pb': pb,
            'pe_status': pe_status,
            'pb_status': pb_status,
            'valuation_status': valuation_status
        }
        
        return valuation_status, details
    
    def _get_pe_status(self, pe: float) -> str:
        """判断PE估值状态"""
        if pe <= 0 or pd.isna(pe):
            return '异常'
        elif pe < 10:
            return '低估'
        elif pe < 20:
            return '合理偏低'
        elif pe < 40:
            return '合理'
        elif pe < 60:
            return '合理偏高'
        else:
            return '高估'
    
    def _get_pb_status(self, pb: float) -> str:
        """判断PB估值状态"""
        if pb <= 0 or pd.isna(pb):
            return '异常'
        elif pb < 1:
            return '低估'
        elif pb < 2:
            return '合理偏低'
        elif pb < 4:
            return '合理'
        elif pb < 6:
            return '合理偏高'
        else:
            return '高估'
    
    # ==================== 股息分析 ====================
    
    def analyze_dividend(
        self,
        dividend_ratio: float,
        payout_ratio: float = None
    ) -> Dict:
        """
        分析股息回报
        
        Args:
            dividend_ratio: 股息率 (%)
            payout_ratio: 分红比例
        
        Returns:
            dict: 股息分析结果
        """
        result = {
            'dividend_ratio': dividend_ratio,
            'rating': self._get_dividend_rating(dividend_ratio)
        }
        
        if payout_ratio is not None:
            result['payout_ratio'] = payout_ratio
            result['sustainability'] = self._get_dividend_sustainability(payout_ratio)
        
        return result
    
    def _get_dividend_rating(self, ratio: float) -> str:
        """评级股息率"""
        if pd.isna(ratio):
            return '无股息'
        elif ratio >= 5:
            return '优秀'
        elif ratio >= 3:
            return '良好'
        elif ratio >= 1:
            return '一般'
        else:
            return '较低'
    
    def _get_dividend_sustainability(self, payout_ratio: float) -> str:
        """评级股息可持续性"""
        if pd.isna(payout_ratio):
            return '未知'
        elif payout_ratio > 80:
            return '较高风险'
        elif payout_ratio > 50:
            return '适中'
        else:
            return '健康'
    
    # ==================== 财务健康度 ====================
    
    def check_financial_health(
        self,
        stock_data: Dict
    ) -> Dict:
        """
        检查财务健康度
        
        Args:
            stock_data: 股票数据字典
        
        Returns:
            dict: 财务健康度检查结果
        """
        roe = stock_data.get('roe', 0)
        netprofit_margin = stock_data.get('netprofit_margin', 0)
        grossprofit_margin = stock_data.get('grossprofit_margin', 0)
        
        checks = []
        score = 60  # 基础分
        
        # ROE检查
        if pd.notna(roe):
            if roe > 15:
                checks.append("✓ ROE优秀 (>15%)")
                score += 10
            elif roe > 10:
                checks.append("✓ ROE良好 (>10%)")
                score += 5
            elif roe > 5:
                checks.append("○ ROE一般 (>5%)")
            else:
                checks.append("✗ ROE偏低")
                score -= 10
        
        # 净利润率检查
        if pd.notna(netprofit_margin):
            if netprofit_margin > 20:
                checks.append("✓ 净利润率高 (>20%)")
                score += 5
            elif netprofit_margin > 10:
                checks.append("✓ 净利润率良好 (>10%)")
                score += 3
            elif netprofit_margin > 0:
                checks.append("○ 净利润率为正")
            else:
                checks.append("✗ 净利润率为负")
                score -= 15
        
        # 毛利率检查
        if pd.notna(grossprofit_margin):
            if grossprofit_margin > 50:
                checks.append("✓ 毛利率优秀 (>50%)")
                score += 5
            elif grossprofit_margin > 30:
                checks.append("✓ 毛利率良好 (>30%)")
                score += 3
            elif grossprofit_margin > 0:
                checks.append("○ 毛利率为正")
            else:
                checks.append("✗ 毛利率为负")
                score -= 10
        
        # 综合评级
        score = max(0, min(100, score))
        
        if score >= 80:
            health_rating = '优秀'
        elif score >= 60:
            health_rating = '良好'
        elif score >= 40:
            health_rating = '一般'
        else:
            health_rating = '较差'
        
        return {
            'health_score': score,
            'health_rating': health_rating,
            'checks': checks
        }
    
    # ==================== 综合分析 ====================
    
    def full_analysis(
        self,
        data: pd.DataFrame = None,
        filters: Dict = None,
        weights: Dict = None,
        top_n: int = 10
    ) -> Dict:
        """
        完整基本面分析流程
        
        Args:
            data: 原始数据
            filters: 筛选条件
            weights: 评分权重
            top_n: 返回Top N
        
        Returns:
            dict: 完整分析结果
        """
        # 1. 筛选
        df_filtered = self.filter_stocks(filters=filters, data=data)
        
        if df_filtered.empty:
            return {
                'status': 'warning',
                'message': '筛选后无股票',
                'stocks': []
            }
        
        # 2. 评分
        df_scored = self.calculate_composite_score(weights=weights, data=df_filtered)
        
        # 3. 排名
        df_ranked = self.rank_by_composite(data=df_scored, top_n=top_n)
        
        # 4. 转换为字典格式
        stocks = []
        for idx, row in df_ranked.iterrows():
            stock = row.to_dict()
            stock['rank'] = len(stocks) + 1
            stocks.append(stock)
        
        return {
            'status': 'success',
            'total_stocks': len(df_filtered),
            'analyzed_stocks': len(stocks),
            'stocks': stocks,
            'filters_used': filters or self.DEFAULT_FILTERS,
            'weights_used': weights or self.DEFAULT_WEIGHTS
        }


# ==================== 便捷函数 ====================

def calculate_pe(price: float, eps: float) -> float:
    """
    便捷函数：计算市盈率
    
    Args:
        price: 股价
        eps: 每股收益
    
    Returns:
        float: 市盈率
    """
    if eps <= 0:
        return 0
    return round(price / eps, 2)


def calculate_pb(price: float, bvps: float) -> float:
    """
    便捷函数：计算市净率
    
    Args:
        price: 股价
        bvps: 每股净资产
    
    Returns:
        float: 市净率
    """
    if bvps <= 0:
        return 0
    return round(price / bvps, 2)


def calculate_roe(net_profit: float, equity: float) -> float:
    """
    便捷函数：计算净资产收益率
    
    Args:
        net_profit: 净利润
        equity: 净资产
    
    Returns:
        float: ROE (%)
    """
    if equity <= 0:
        return 0
    return round(net_profit / equity * 100, 2)


def calculate_dividend_yield(dividend: float, price: float) -> float:
    """
    便捷函数：计算股息率
    
    Args:
        dividend: 每股股息
        price: 股价
    
    Returns:
        float: 股息率 (%)
    """
    if price <= 0:
        return 0
    return round(dividend / price * 100, 2)


def calculate_payout_ratio(dividend: float, eps: float) -> float:
    """
    便捷函数：计算分红比例
    
    Args:
        dividend: 每股股息
        eps: 每股收益
    
    Returns:
        float: 分红比例 (%)
    """
    if eps <= 0:
        return 0
    return round(dividend / eps * 100, 2)
