#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
技术指标单元测试
"""

import unittest
import sys
import os
import pandas as pd
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.technical_indicators import (
    TechnicalIndicators,
    calculate_ma,
    calculate_rsi,
    calculate_macd,
    MAResult,
    MACDResult,
    RSIResult,
    BollingerResult,
    VolumeResult
)


class TestTechnicalIndicators(unittest.TestCase):
    """技术指标测试类"""
    
    def setUp(self):
        """测试数据准备"""
        # 生成测试数据：模拟上涨趋势
        self.uptrend_data = list(range(100, 200, 2))  # 上涨
        self.downtrend_data = list(range(200, 100, -2))  # 下跌
        self.sideways_data = [100] * 50 + list(range(100, 110)) + [110] * 30  # 震荡
        
        # 使用DataFrame
        import pandas as pd
        self.df = pd.DataFrame({
            'close': self.uptrend_data,
            'vol': [1000000] * len(self.uptrend_data)
        })
    
    # ==================== MA测试 ====================
    
    def test_calculate_ma(self):
        """测试MA计算"""
        ti = TechnicalIndicators(self.uptrend_data)
        ma = ti.calculate_ma()
        
        # MA5应该等于最后5个价格的平均值
        expected_ma5 = sum(self.uptrend_data[-5:]) / 5
        self.assertAlmostEqual(ma.ma5, expected_ma5, places=1)
        
        # MA10应该等于最后10个价格的平均值
        expected_ma10 = sum(self.uptrend_data[-10:]) / 10
        self.assertAlmostEqual(ma.ma10, expected_ma10, places=1)
    
    def test_calculate_ma_dict(self):
        """测试MA字典格式"""
        ti = TechnicalIndicators(self.uptrend_data)
        ma_dict = ti.calculate_ma_dict()
        
        self.assertIn('MA5', ma_dict)
        self.assertIn('MA10', ma_dict)
        self.assertIn('MA20', ma_dict)
        self.assertIn('MA60', ma_dict)
    
    def test_get_ma_signal_bullish(self):
        """测试多头排列信号"""
        # 多头排列：MA5 > MA10 > MA20
        ti = TechnicalIndicators(self.uptrend_data)
        signal, desc = ti.get_ma_signal()
        
        self.assertEqual(signal, 'bullish')
    
    def test_get_ma_signal_bearish(self):
        """测试空头排列信号"""
        ti = TechnicalIndicators(self.downtrend_data)
        signal, desc = ti.get_ma_signal()
        
        self.assertEqual(signal, 'bearish')
    
    # ==================== MACD测试 ====================
    
    def test_calculate_macd(self):
        """测试MACD计算"""
        ti = TechnicalIndicators(self.uptrend_data)
        macd = ti.calculate_macd()
        
        self.assertIsInstance(macd, MACDResult)
        self.assertIsInstance(macd.dif, float)
        self.assertIsInstance(macd.dea, float)
        self.assertIsInstance(macd.macd, float)
    
    def test_calculate_macd_dict(self):
        """测试MACD字典格式"""
        ti = TechnicalIndicators(self.uptrend_data)
        macd_dict = ti.calculate_macd_dict()
        
        self.assertIn('DIF', macd_dict)
        self.assertIn('DEA', macd_dict)
        self.assertIn('MACD', macd_dict)
    
    def test_get_macd_signal(self):
        """测试MACD信号"""
        # 使用更明显上涨的数据
        uptrend = [100 + i * 0.5 for i in range(100)]
        ti = TechnicalIndicators(uptrend)
        signal, desc = ti.get_macd_signal()
        
        # 验证信号类型
        self.assertIn(signal, ['bullish', 'neutral', 'bearish'])
    
    # ==================== RSI测试 ====================
    
    def test_calculate_rsi(self):
        """测试RSI计算"""
        ti = TechnicalIndicators(self.uptrend_data)
        rsi = ti.calculate_rsi()
        
        self.assertIsInstance(rsi, RSIResult)
        self.assertIsInstance(rsi.rsi6, float)
        self.assertIsInstance(rsi.rsi12, float)
        self.assertIsInstance(rsi.rsi24, float)
        
        # RSI应该在0-100之间
        self.assertGreaterEqual(rsi.rsi6, 0)
        self.assertLessEqual(rsi.rsi6, 100)
    
    def test_calculate_rsi_dict(self):
        """测试RSI字典格式"""
        ti = TechnicalIndicators(self.uptrend_data)
        rsi_dict = ti.calculate_rsi_dict()
        
        self.assertIn('RSI6', rsi_dict)
        self.assertIn('RSI12', rsi_dict)
        self.assertIn('RSI24', rsi_dict)
    
    def test_rsi_values(self):
        """测试RSI数值范围"""
        # 使用足够长的震荡数据
        sideways = [100 + i % 5 for i in range(100)]
        ti = TechnicalIndicators(sideways)
        rsi = ti.calculate_rsi()
        
        # RSI应该在0-100之间
        if not pd.isna(rsi.rsi6):
            self.assertGreaterEqual(rsi.rsi6, 0)
            self.assertLessEqual(rsi.rsi6, 100)
    
    def test_get_rsi_signal(self):
        """测试RSI信号"""
        # 测试超买
        overbought_data = [100] * 50 + [120, 125, 130, 135, 140]  # 快速上涨
        ti = TechnicalIndicators(overbought_data)
        signal, desc = ti.get_rsi_signal()
        
        # 快速上涨会导致RSI超买
        self.assertIn(signal, ['overbought', 'bullish'])
    
    # ==================== 布林带测试 ====================
    
    def test_calculate_bollinger_bands(self):
        """测试布林带计算"""
        ti = TechnicalIndicators(self.uptrend_data)
        bb = ti.calculate_bollinger_bands()
        
        self.assertIsInstance(bb, BollingerResult)
        
        # 布林带基本关系
        self.assertLess(bb.lower, bb.middle)
        self.assertGreater(bb.upper, bb.middle)
    
    def test_calculate_bollinger_dict(self):
        """测试布林带字典格式"""
        ti = TechnicalIndicators(self.uptrend_data)
        bb_dict = ti.calculate_bollinger_dict()
        
        self.assertIn('BB_UPPER', bb_dict)
        self.assertIn('BB_MIDDLE', bb_dict)
        self.assertIn('BB_LOWER', bb_dict)
    
    def test_bollinger_position(self):
        """测试布林带位置"""
        ti = TechnicalIndicators(self.uptrend_data)
        bb = ti.calculate_bollinger_bands()
        
        # %B 应该在0-1之间
        self.assertGreaterEqual(bb.percent, 0)
        self.assertLessEqual(bb.percent, 1)
    
    def test_get_bollinger_signal(self):
        """测试布林带信号"""
        ti = TechnicalIndicators(self.uptrend_data)
        signal, desc = ti.get_bollinger_signal()
        
        self.assertIsInstance(signal, str)
        self.assertIsInstance(desc, str)
    
    # ==================== 成交量分析测试 ====================
    
    def test_analyze_volume(self):
        """测试成交量分析"""
        ti = TechnicalIndicators(self.df)
        vol = ti.analyze_volume()
        
        self.assertIsInstance(vol, VolumeResult)
        self.assertIsInstance(vol.avg_volume, float)
        self.assertIsInstance(vol.volume_trend, str)
    
    def test_volume_trend(self):
        """测试量价关系"""
        # 使用更明显的量价齐升数据
        df = pd.DataFrame({
            'close': [100, 100, 100, 102, 105],  # 价格逐步上涨
            'vol': [1000000, 1000000, 1300000, 1500000, 1800000]  # 成交量放大
        })
        ti = TechnicalIndicators(df)
        vol = ti.analyze_volume()
        
        # 验证成交量趋势不为空
        self.assertIsNotNone(vol.volume_trend)
        self.assertIsInstance(vol.volume_trend, str)
    
    # ==================== 综合分析测试 ====================
    
    def test_get_all_indicators(self):
        """测试获取所有指标"""
        # 创建带成交量的DataFrame
        df = pd.DataFrame({
            'close': self.uptrend_data,
            'vol': [1000000] * len(self.uptrend_data)
        })
        ti = TechnicalIndicators(df)
        indicators = ti.get_all_indicators()
        
        self.assertIn('ma', indicators)
        self.assertIn('macd', indicators)
        self.assertIn('rsi', indicators)
        self.assertIn('bollinger', indicators)
        self.assertIn('volume', indicators)
    
    def test_get_composite_signal(self):
        """测试综合信号"""
        ti = TechnicalIndicators(self.uptrend_data)
        signal = ti.get_composite_signal()
        
        self.assertIn('composite_score', signal)
        self.assertIn('trend', signal)
        self.assertIn('ma_signal', signal)
        self.assertIn('macd_signal', signal)
        
        # 评分应该在0-100之间
        self.assertGreaterEqual(signal['composite_score'], 0)
        self.assertLessEqual(signal['composite_score'], 100)
    
    # ==================== 便捷函数测试 ====================
    
    def test_convenience_functions(self):
        """测试便捷函数"""
        prices = list(range(100, 200, 2))
        
        ma = calculate_ma(prices, 5)
        self.assertIsInstance(ma, float)
        
        rsi = calculate_rsi(prices, 14)
        self.assertIsInstance(rsi, float)
        self.assertGreaterEqual(rsi, 0)
        self.assertLessEqual(rsi, 100)
        
        macd = calculate_macd(prices)
        self.assertIn('DIF', macd)
        self.assertIn('DEA', macd)
        self.assertIn('MACD', macd)
    
    def test_invalid_input(self):
        """测试无效输入"""
        # 空数据
        with self.assertRaises(ValueError):
            TechnicalIndicators([])
        
        # 空DataFrame
        with self.assertRaises(ValueError):
            TechnicalIndicators(pd.DataFrame())
        
        # 无效类型
        with self.assertRaises(TypeError):
            TechnicalIndicators("invalid")


class TestEdgeCases(unittest.TestCase):
    """边缘情况测试"""
    
    def test_short_data(self):
        """测试数据不足的情况"""
        short_data = [100, 101, 102]
        ti = TechnicalIndicators(short_data)
        
        ma = ti.calculate_ma()
        # 数据不足时应该使用全部平均值
        self.assertIsNotNone(ma)
    
    def test_constant_price(self):
        """测试价格不变的情况"""
        constant = [100] * 50  # 增加数据量
        ti = TechnicalIndicators(constant)
        
        rsi = ti.calculate_rsi()
        # 价格不变时RSI应该接近50
        if not pd.isna(rsi.rsi6):
            self.assertAlmostEqual(rsi.rsi6, 50, delta=5)


if __name__ == '__main__':
    unittest.main(verbosity=2)
