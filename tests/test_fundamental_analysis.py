#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
基本面分析单元测试
"""

import unittest
import sys
import os
import pandas as pd
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.fundamental_analysis import (
    FundamentalAnalyzer,
    calculate_pe,
    calculate_pb,
    calculate_roe,
    calculate_dividend_yield,
    calculate_payout_ratio,
    CompositeScore
)


class TestFundamentalAnalyzer(unittest.TestCase):
    """基本面分析器测试类"""
    
    def setUp(self):
        """测试数据准备"""
        self.analyzer = FundamentalAnalyzer()
        
        # 创建测试数据
        self.test_data = pd.DataFrame({
            'code': ['sh.600000', 'sh.600001', 'sh.600002', 'sh.600003', 'sh.600004'],
            'name': ['浦发银行', '邯郸钢铁', '齐鲁石化', 'ST银广夏', '万科A'],
            'close': [10.0, 8.0, 12.0, 5.0, 15.0],
            'pe': [8.0, 15.0, 12.0, 0, 20.0],  # ST股票PE为0
            'pb': [1.0, 1.5, 1.2, 0.3, 2.0],
            'roe': [12.0, 10.0, 15.0, -5.0, 18.0],  # ST股票ROE为负
            'dv_ratio': [3.5, 2.0, 4.0, 0, 5.0],
            'turnover_rate': [2.0, 3.0, 1.5, 10.0, 5.0],
            'market_cap': [1000, 800, 1200, 300, 2000]
        })
    
    # ==================== 筛选功能测试 ====================
    
    def test_filter_stocks_pe(self):
        """测试PE筛选"""
        filters = {
            'pe_min': 0,
            'pe_max': 15
        }
        
        df = self.analyzer.filter_stocks(filters=filters, data=self.test_data.copy())
        
        # PE应该都在0-15之间
        self.assertTrue((df['pe'] >= 0).all())
        self.assertTrue((df['pe'] <= 15).all())
    
    def test_filter_stocks_pb(self):
        """测试PB筛选"""
        filters = {
            'pb_min': 1.0,
            'pb_max': 2.0
        }
        
        df = self.analyzer.filter_stocks(filters=filters, data=self.test_data.copy())
        
        self.assertTrue((df['pb'] >= 1.0).all())
        self.assertTrue((df['pb'] <= 2.0).all())
    
    def test_filter_stocks_roe(self):
        """测试ROE筛选"""
        filters = {
            'roe_min': 10
        }
        
        df = self.analyzer.filter_stocks(filters=filters, data=self.test_data.copy())
        
        self.assertTrue((df['roe'] >= 10).all())
    
    def test_filter_stocks_dividend(self):
        """测试股息率筛选"""
        filters = {
            'dividend_min': 3.0
        }
        
        df = self.analyzer.filter_stocks(filters=filters, data=self.test_data.copy())
        
        self.assertTrue((df['dv_ratio'] >= 3.0).all())
    
    def test_filter_stocks_turnover(self):
        """测试换手率筛选"""
        filters = {
            'turnover_rate_min': 1.0,
            'turnover_rate_max': 5.0
        }
        
        df = self.analyzer.filter_stocks(filters=filters, data=self.test_data.copy())
        
        self.assertTrue((df['turnover_rate'] >= 1.0).all())
        self.assertTrue((df['turnover_rate'] <= 5.0).all())
    
    def test_filter_combined(self):
        """测试组合筛选"""
        filters = {
            'pe_max': 20,
            'pb_max': 2.0,
            'roe_min': 10,
            'dividend_min': 2.0
        }
        
        df = self.analyzer.filter_stocks(filters=filters, data=self.test_data.copy())
        
        # 验证所有条件
        self.assertTrue((df['pe'] <= 20).all())
        self.assertTrue((df['pb'] <= 2.0).all())
        self.assertTrue((df['roe'] >= 10).all())
        self.assertTrue((df['dv_ratio'] >= 2.0).all())
    
    def test_filter_st_stocks(self):
        """测试过滤ST股票"""
        # ST股票ROE为负，pe为0
        filters = {
            'roe_min': 0
        }
        
        df = self.analyzer.filter_stocks(filters=filters, data=self.test_data.copy())
        
        # ST银广夏应该被过滤
        self.assertFalse('ST银广夏' in df['name'].values)
    
    # ==================== 评分功能测试 ====================
    
    def test_calculate_composite_score(self):
        """测试综合评分计算"""
        df = self.analyzer.calculate_composite_score(data=self.test_data.copy())
        
        # 检查评分列存在
        self.assertIn('pe_score', df.columns)
        self.assertIn('pb_score', df.columns)
        self.assertIn('roe_score', df.columns)
        self.assertIn('dividend_score', df.columns)
        self.assertIn('liquidity_score', df.columns)
        self.assertIn('composite_score', df.columns)
    
    def test_pe_score_calculation(self):
        """测试PE评分计算"""
        df = self.analyzer.calculate_composite_score(data=self.test_data.copy())
        
        # PE越低评分越高
        # 浦发银行PE=8，万科PE=20
        pufa = df[df['code'] == 'sh.600000'].iloc[0]
        vanke = df[df['code'] == 'sh.600004'].iloc[0]
        
        self.assertGreater(pufa['pe_score'], vanke['pe_score'])
    
    def test_pb_score_calculation(self):
        """测试PB评分计算"""
        df = self.analyzer.calculate_composite_score(data=self.test_data.copy())
        
        # PB越低评分越高
        pufa = df[df['code'] == 'sh.600000'].iloc[0]  # PB=1.0
        vanke = df[df['code'] == 'sh.600004'].iloc[0]  # PB=2.0
        
        self.assertGreater(pufa['pb_score'], vanke['pb_score'])
    
    def test_roe_score_calculation(self):
        """测试ROE评分计算"""
        df = self.analyzer.calculate_composite_score(data=self.test_data.copy())
        
        # ROE越高评分越高
        vanke = df[df['code'] == 'sh.600004'].iloc[0]  # ROE=18 (满分100)
        qilu = df[df['code'] == 'sh.600002'].iloc[0]  # ROE=10
        
        self.assertGreaterEqual(vanke['roe_score'], qilu['roe_score'])
    
    def test_dividend_score_calculation(self):
        """测试股息评分计算"""
        df = self.analyzer.calculate_composite_score(data=self.test_data.copy())
        
        # 股息率越高评分越高
        vanke = df[df['code'] == 'sh.600004'].iloc[0]  # dv=5.0
        qilu = df[df['code'] == 'sh.600002'].iloc[0]  # dv=2.0
        
        self.assertGreater(vanke['dividend_score'], qilu['dividend_score'])
    
    def test_liquidity_score_calculation(self):
        """测试流动性评分计算"""
        df = self.analyzer.calculate_composite_score(data=self.test_data.copy())
        
        # 适中换手率评分最高
        # 齐鲁石化 turnover=1.5 (适中)
        qilu = df[df['code'] == 'sh.600002'].iloc[0]
        
        # 评分应该在合理范围内
        self.assertGreaterEqual(qilu['liquidity_score'], 0)
        self.assertLessEqual(qilu['liquidity_score'], 100)
    
    def test_custom_weights(self):
        """测试自定义权重"""
        custom_weights = {
            'pe_weight': 0.40,
            'pb_weight': 0.10,
            'roe_weight': 0.20,
            'dividend_weight': 0.20,
            'liquidity_weight': 0.10
        }
        
        df = self.analyzer.calculate_composite_score(
            weights=custom_weights,
            data=self.test_data.copy()
        )
        
        # 检查评分
        self.assertIn('composite_score', df.columns)
        
        # 验证权重总和为1
        total = sum(custom_weights.values())
        self.assertAlmostEqual(total, 1.0, places=5)
    
    # ==================== 单只股票评分测试 ====================
    
    def test_get_stock_score(self):
        """测试单只股票评分"""
        stock_data = {
            'pe': 10.0,
            'pb': 1.5,
            'roe': 15.0,
            'dv_ratio': 4.0,
            'turnover_rate': 3.0
        }
        
        score = self.analyzer.get_stock_score(stock_data)
        
        self.assertIsInstance(score, CompositeScore)
        self.assertIsInstance(score.total_score, float)
        self.assertGreaterEqual(score.total_score, 0)
        self.assertLessEqual(score.total_score, 100)
    
    def test_stock_score_breakdown(self):
        """测试评分明细"""
        stock_data = {
            'pe': 10.0,
            'pb': 1.5,
            'roe': 15.0,
            'dv_ratio': 4.0,
            'turnover_rate': 3.0
        }
        
        score = self.analyzer.get_stock_score(stock_data)
        
        self.assertIn('pe_score', score.score_breakdown)
        self.assertIn('pb_score', score.score_breakdown)
        self.assertIn('roe_score', score.score_breakdown)
        self.assertIn('dividend_score', score.score_breakdown)
        self.assertIn('liquidity_score', score.score_breakdown)
    
    # ==================== 排名功能测试 ====================
    
    def test_rank_by_roe(self):
        """测试按ROE排名"""
        df = self.analyzer.rank_by_roe(
            data=self.test_data.copy(),
            ascending=False,
            top_n=3
        )
        
        # 应该按ROE降序排列
        self.assertEqual(len(df), 3)
        roe_values = df['roe'].values
        self.assertTrue(all(roe_values[i] >= roe_values[i+1] for i in range(len(roe_values)-1)))
    
    def test_rank_by_pe(self):
        """测试按PE排名"""
        df = self.analyzer.rank_by_pe(
            data=self.test_data.copy(),
            ascending=True,
            top_n=3
        )
        
        # 应该按PE升序排列（低估值优先）
        self.assertEqual(len(df), 3)
        pe_values = df['pe'].values
        self.assertTrue(all(pe_values[i] <= pe_values[i+1] for i in range(len(pe_values)-1)))
    
    def test_rank_by_dividend(self):
        """测试按股息率排名"""
        df = self.analyzer.rank_by_dividend(
            data=self.test_data.copy(),
            ascending=False,
            top_n=3
        )
        
        self.assertEqual(len(df), 3)
    
    def test_rank_by_composite(self):
        """测试按综合评分排名"""
        df = self.analyzer.rank_by_composite(
            data=self.test_data.copy(),
            ascending=False,
            top_n=3
        )
        
        self.assertEqual(len(df), 3)
        
        # 检查评分降序
        score_values = df['composite_score'].values
        self.assertTrue(all(score_values[i] >= score_values[i+1] for i in range(len(score_values)-1)))
    
    # ==================== 估值分析测试 ====================
    
    def test_get_valuation_status_low(self):
        """测试低估状态"""
        stock_data = {'pe': 8.0, 'pb': 0.8}
        status, details = self.analyzer.get_valuation_status(stock_data)
        
        self.assertEqual(details['pe_status'], '低估')
        self.assertEqual(details['pb_status'], '低估')
    
    def test_get_valuation_status_high(self):
        """测试高估状态"""
        stock_data = {'pe': 70.0, 'pb': 8.0}  # 使用更高的值
        status, details = self.analyzer.get_valuation_status(stock_data)
        
        self.assertEqual(details['pe_status'], '高估')
        self.assertEqual(details['pb_status'], '高估')
    
    def test_get_valuation_status_normal(self):
        """测试正常估值"""
        stock_data = {'pe': 25.0, 'pb': 3.0}
        status, details = self.analyzer.get_valuation_status(stock_data)
        
        self.assertIn(details['pe_status'], ['合理', '合理偏低'])
        self.assertIn(details['pb_status'], ['合理'])
    
    # ==================== 股息分析测试 ====================
    
    def test_analyze_dividend_excellent(self):
        """测试优秀股息"""
        result = self.analyzer.analyze_dividend(dividend_ratio=6.0)
        
        self.assertEqual(result['rating'], '优秀')
    
    def test_analyze_dividend_good(self):
        """测试良好股息"""
        result = self.analyzer.analyze_dividend(dividend_ratio=4.0)
        
        self.assertEqual(result['rating'], '良好')
    
    def test_analyze_dividend_normal(self):
        """测试一般股息"""
        result = self.analyzer.analyze_dividend(dividend_ratio=2.0)
        
        self.assertEqual(result['rating'], '一般')
    
    def test_analyze_dividend_with_payout(self):
        """测试股息可持续性"""
        result = self.analyzer.analyze_dividend(
            dividend_ratio=5.0,
            payout_ratio=30.0
        )
        
        self.assertEqual(result['rating'], '优秀')
        self.assertEqual(result['sustainability'], '健康')
    
    # ==================== 财务健康度测试 ====================
    
    def test_check_financial_health_excellent(self):
        """测试优秀财务健康度"""
        stock_data = {
            'roe': 20.0,
            'netprofit_margin': 25.0,
            'grossprofit_margin': 60.0
        }
        
        result = self.analyzer.check_financial_health(stock_data)
        
        self.assertGreaterEqual(result['health_score'], 80)
        self.assertEqual(result['health_rating'], '优秀')
    
    def test_check_financial_health_poor(self):
        """测试较差财务健康度"""
        stock_data = {
            'roe': -5.0,
            'netprofit_margin': -10.0,
            'grossprofit_margin': -5.0
        }
        
        result = self.analyzer.check_financial_health(stock_data)
        
        self.assertLess(result['health_score'], 60)
    
    # ==================== 完整分析测试 ====================
    
    def test_full_analysis(self):
        """测试完整分析流程"""
        result = self.analyzer.full_analysis(
            data=self.test_data.copy(),
            top_n=5
        )
        
        self.assertEqual(result['status'], 'success')
        self.assertIn('stocks', result)
        self.assertLessEqual(len(result['stocks']), 5)  # 可能被筛选掉
    
    def test_full_analysis_with_filters(self):
        """测试带筛选的完整分析"""
        filters = {
            'pe_max': 20,
            'roe_min': 10
        }
        
        result = self.analyzer.full_analysis(
            data=self.test_data.copy(),
            filters=filters,
            top_n=10
        )
        
        self.assertEqual(result['status'], 'success')
        self.assertIn('filters_used', result)
    
    # ==================== 便捷函数测试 ====================
    
    def test_calculate_pe(self):
        """测试PE计算"""
        pe = calculate_pe(price=100, eps=10)
        self.assertEqual(pe, 10.0)
        
        # EPS为0
        pe_zero = calculate_pe(price=100, eps=0)
        self.assertEqual(pe_zero, 0)
    
    def test_calculate_pb(self):
        """测试PB计算"""
        pb = calculate_pb(price=20, bvps=10)
        self.assertEqual(pb, 2.0)
    
    def test_calculate_roe(self):
        """测试ROE计算"""
        roe = calculate_roe(net_profit=150, equity=1000)
        self.assertEqual(roe, 15.0)
    
    def test_calculate_dividend_yield(self):
        """测试股息率计算"""
        dy = calculate_dividend_yield(dividend=0.5, price=10)
        self.assertEqual(dy, 5.0)
    
    def test_calculate_payout_ratio(self):
        """测试分红比例计算"""
        pr = calculate_payout_ratio(dividend=0.5, eps=1.0)
        self.assertEqual(pr, 50.0)


class TestDataFrameOperations(unittest.TestCase):
    """DataFrame操作测试"""
    
    def test_empty_data(self):
        """测试空数据"""
        analyzer = FundamentalAnalyzer()
        empty_df = pd.DataFrame()
        
        with self.assertRaises(ValueError):
            analyzer.filter_stocks(data=empty_df)
    
    def test_missing_columns(self):
        """测试缺失列"""
        analyzer = FundamentalAnalyzer()
        df = pd.DataFrame({'code': ['sh.600000'], 'close': [10.0]})
        
        # 应该能够处理（只是没有筛选条件）
        result = analyzer.filter_stocks(data=df)
        self.assertEqual(len(result), 1)


if __name__ == '__main__':
    unittest.main(verbosity=2)
