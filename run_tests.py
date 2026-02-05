#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
运行所有单元测试
"""

import unittest
import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 发现并运行所有测试
loader = unittest.TestLoader()
suite = unittest.TestSuite()

# 加载测试模块
from tests.test_technical_indicators import TestTechnicalIndicators, TestEdgeCases
from tests.test_fundamental_analysis import TestFundamentalAnalyzer, TestDataFrameOperations
from tests.test_stock_analyzer import TestStockAnalyzer, TestStockAnalyzerFilters, TestConvenienceFunctions

# 添加测试用例
suite.addTests(loader.loadTestsFromTestCase(TestTechnicalIndicators))
suite.addTests(loader.loadTestsFromTestCase(TestEdgeCases))
suite.addTests(loader.loadTestsFromTestCase(TestFundamentalAnalyzer))
suite.addTests(loader.loadTestsFromTestCase(TestDataFrameOperations))
suite.addTests(loader.loadTestsFromTestCase(TestStockAnalyzer))
suite.addTests(loader.loadTestsFromTestCase(TestStockAnalyzerFilters))
suite.addTests(loader.loadTestsFromTestCase(TestConvenienceFunctions))

# 运行测试
runner = unittest.TextTestRunner(verbosity=2)
result = runner.run(suite)

# 输出测试摘要
print("\n" + "=" * 60)
print("测试摘要")
print("=" * 60)
print(f"运行测试: {result.testsRun}")
print(f"失败: {len(result.failures)}")
print(f"错误: {len(result.errors)}")
print(f"跳过: {len(result.skipped)}")

if result.wasSuccessful():
    print("\n✅ 所有测试通过!")
    sys.exit(0)
else:
    print("\n❌ 存在失败的测试")
    sys.exit(1)
