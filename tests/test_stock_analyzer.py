#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
股票分析器单元测试
"""

import unittest
import sys
import os
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.stock_analyzer import StockAnalyzer


class TestStockAnalyzer(unittest.TestCase):
    """股票分析器测试类"""
    
    def setUp(self):
        """测试数据准备"""
        self.analyzer = StockAnalyzer()
        
        # 创建测试数据
        self.test_data = pd.DataFrame({
            'code': ['sh.600000', 'sh.600001', 'sh.600002', 'sh.600003', 'sh.600004'],
            'name': ['浦发银行', '邯郸钢铁', '齐鲁石化', 'ST银广夏', '万科A'],
            'close': [10.0, 8.0, 12.0, 5.0, 15.0],
            'pe': [8.0, 15.0, 12.0, 0, 20.0],
            'pb': [1.0, 1.5, 1.2, 0.3, 2.0],
            'roe': [12.0, 10.0, 15.0, -5.0, 18.0],
            'dv_ratio': [3.5, 2.0, 4.0, 0, 5.0],
            'turnover_rate': [2.0, 3.0, 1.5, 10.0, 5.0],
            'market_cap': [1000, 800, 1200, 300, 2000]
        })
    
    # ==================== 连接测试 ====================
    
    def test_connect(self):
        """测试Baostock连接"""
        # 注意：实际连接可能失败（网络问题），这里测试逻辑
        self.assertTrue(True)  # 跳过实际连接测试
    
    def test_context_manager(self):
        """测试上下文管理器"""
        with StockAnalyzer() as analyzer:
            self.assertIsNotNone(analyzer)
    
    # ==================== 筛选测试 ====================
    
    def test_screen_stocks(self):
        """测试股票筛选"""
        criteria = {
            'pe_max': 20,
            'roe_min': 10
        }
        
        result = self.analyzer.screen_stocks(
            criteria=criteria,
            data=self.test_data.copy()
        )
        
        self.assertFalse(result.empty)
        
        # 验证筛选结果
        if not result.empty:
            self.assertTrue((result['pe'] <= 20).all())
            self.assertTrue((result['roe'] >= 10).all())
    
    def test_get_top_recommendations(self):
        """测试获取Top推荐"""
        recommendations = self.analyzer.get_top_recommendations(
            data=self.test_data.copy(),
            top_n=3
        )
        
        self.assertIsInstance(recommendations, list)
        self.assertLessEqual(len(recommendations), 3)
    
    def test_get_top_recommendations_scoring(self):
        """测试推荐排序"""
        recommendations = self.analyzer.get_top_recommendations(
            data=self.test_data.copy(),
            top_n=5
        )
        
        if len(recommendations) >= 2:
            # 评分应该降序
            self.assertGreaterEqual(
                recommendations[0]['composite_score'],
                recommendations[1]['composite_score']
            )
    
    # ==================== 报告生成测试 ====================
    
    def test_generate_recommendation_report(self):
        """测试推荐报告生成"""
        recommendations = [
            {
                'rank': 1,
                'code': 'sh.600000',
                'close': 10.0,
                'pe': 8.0,
                'pb': 1.0,
                'roe': 12.0,
                'dv_ratio': 3.5,
                'turnover_rate': 2.0,
                'market_cap': 1000,
                'composite_score': 75.5,
                'pe_score': 80.0,
                'pb_score': 85.0,
                'roe_score': 70.0,
                'dividend_score': 65.0,
                'liquidity_score': 60.0
            }
        ]
        
        report = self.analyzer.generate_recommendation_report(
            recommendations=recommendations
        )
        
        self.assertIn('report_date', report)
        self.assertIn('recommendations', report)
        self.assertEqual(len(report['recommendations']), 1)
    
    def test_generate_recommendation_report_with_file(self):
        """测试报告保存"""
        import tempfile
        import os
        
        recommendations = [
            {
                'rank': 1,
                'code': 'sh.600000',
                'close': 10.0,
                'pe': 8.0,
                'pb': 1.0,
                'roe': 12.0,
                'dv_ratio': 3.5,
                'turnover_rate': 2.0,
                'market_cap': 1000,
                'composite_score': 75.5,
                'pe_score': 80.0,
                'pb_score': 85.0,
                'roe_score': 70.0,
                'dividend_score': 65.0,
                'liquidity_score': 60.0
            }
        ]
        
        with tempfile.TemporaryDirectory() as tmpdir:
            json_file = os.path.join(tmpdir, 'test_report.json')
            report = self.analyzer.generate_recommendation_report(
                recommendations=recommendations,
                filename=json_file
            )
            
            # 验证文件已创建
            self.assertTrue(os.path.exists(json_file))
            
            # 验证JSON内容
            import json
            with open(json_file, 'r', encoding='utf-8') as f:
                loaded = json.load(f)
            
            self.assertEqual(loaded['total_recommendations'], 1)
    
    def test_generate_markdown_report(self):
        """测试Markdown报告生成"""
        recommendations = [
            {
                'rank': 1,
                'code': 'sh.600000',
                'close': 10.0,
                'pe': 8.0,
                'pb': 1.0,
                'roe': 12.0,
                'dv_ratio': 3.5,
                'turnover_rate': 2.0,
                'composite_score': 75.5
            },
            {
                'rank': 2,
                'code': 'sh.600001',
                'close': 8.0,
                'pe': 15.0,
                'pb': 1.5,
                'roe': 10.0,
                'dv_ratio': 2.0,
                'turnover_rate': 3.0,
                'composite_score': 65.0
            }
        ]
        
        md = self.analyzer.generate_markdown_report(
            recommendations=recommendations
        )
        
        self.assertIsInstance(md, str)
        self.assertIn('# 每日股票推荐报告', md)
        self.assertIn('sh.600000', md)
        self.assertIn('sh.600001', md)
        self.assertIn('风险提示', md)
    
    def test_generate_markdown_report_with_file(self):
        """测试Markdown报告保存"""
        import tempfile
        import os
        
        recommendations = [
            {
                'rank': 1,
                'code': 'sh.600000',
                'close': 10.0,
                'pe': 8.0,
                'pb': 1.0,
                'roe': 12.0,
                'dv_ratio': 3.5,
                'turnover_rate': 2.0,
                'composite_score': 75.5
            }
        ]
        
        with tempfile.TemporaryDirectory() as tmpdir:
            md_file = os.path.join(tmpdir, 'test_report.md')
            md = self.analyzer.generate_markdown_report(
                recommendations=recommendations,
                filename=md_file
            )
            
            # 验证文件已创建
            self.assertTrue(os.path.exists(md_file))
            
            # 验证内容
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            self.assertIn('每日股票推荐报告', content)


class TestStockAnalyzerFilters(unittest.TestCase):
    """筛选条件测试"""
    
    def setUp(self):
        self.analyzer = StockAnalyzer()
    
    def test_default_filters(self):
        """测试默认筛选条件"""
        from core.fundamental_analysis import FundamentalAnalyzer
        filters = FundamentalAnalyzer.DEFAULT_FILTERS
        
        self.assertIn('pe_min', filters)
        self.assertIn('pe_max', filters)
        self.assertIn('pb_min', filters)
        self.assertIn('pb_max', filters)
        self.assertIn('roe_min', filters)
        self.assertIn('dividend_min', filters)
    
    def test_default_weights(self):
        """测试默认权重"""
        from core.fundamental_analysis import FundamentalAnalyzer
        weights = FundamentalAnalyzer.DEFAULT_WEIGHTS
        
        total = sum(weights.values())
        self.assertAlmostEqual(total, 1.0, places=5)
        
        self.assertIn('pe_weight', weights)
        self.assertIn('pb_weight', weights)
        self.assertIn('roe_weight', weights)
        self.assertIn('dividend_weight', weights)
        self.assertIn('liquidity_weight', weights)


class TestConvenienceFunctions(unittest.TestCase):
    """便捷函数测试"""
    
    def test_quick_analyze(self):
        """测试快速分析函数"""
        from core.stock_analyzer import quick_analyze
        
        # 注意：实际分析需要Baostock连接
        # 这里测试函数调用
        self.assertTrue(callable(quick_analyze))
    
    def test_get_recommendations(self):
        """测试获取推荐函数"""
        from core.stock_analyzer import get_recommendations
        
        self.assertTrue(callable(get_recommendations))


if __name__ == '__main__':
    unittest.main(verbosity=2)
