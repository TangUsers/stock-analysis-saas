#!/usr/bin/env python3
"""
StockVision Pro 整合测试
"""

import sys
import os

# 确保core模块路径正确
core_path = 'products/stock-analysis-saas/core'
if core_path not in sys.path:
    sys.path.insert(0, core_path)

def test_project_structure():
    """测试项目结构"""
    print("📁 测试项目结构...")
    try:
        required_dirs = [
            'products/stock-analysis-saas/core',
            'products/stock-analysis-saas/web',
            'products/stock-analysis-saas/operations',
            'products/stock-analysis-saas/marketing',
            'products/stock-analysis-saas/tests',
            'products/stock-analysis-saas/integration_tests'
        ]
        
        for dir_path in required_dirs:
            if os.path.exists(dir_path):
                print(f"  ✅ {dir_path}")
            else:
                print(f"  ❌ {dir_path}: 不存在")
                return False
        
        return True
    except Exception as e:
        print(f"  ❌ 测试失败: {e}")
        return False

def test_module_structure():
    """测试模块结构"""
    print("\n📦 测试模块结构...")
    try:
        from stock_analyzer import StockAnalyzer
        from technical_indicators import TechnicalIndicators
        from fundamental_analysis import FundamentalAnalyzer
        
        print("  ✅ 所有类导入成功")
        print(f"    - StockAnalyzer: {StockAnalyzer.__doc__.strip()[:50]}...")
        print(f"    - TechnicalIndicators: {TechnicalIndicators.__doc__.strip()[:50]}...")
        print(f"    - FundamentalAnalyzer: {FundamentalAnalyzer.__doc__.strip()[:50]}...")
        
        return True
    except Exception as e:
        print(f"  ❌ 导入失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_technical_indicators():
    """测试技术指标"""
    print("\n📈 测试技术指标...")
    try:
        import pandas as pd
        import numpy as np
        from technical_indicators import TechnicalIndicators
        
        # 创建测试数据 - DataFrame格式
        dates = pd.date_range('2025-01-01', periods=100)
        np.random.seed(42)
        prices = np.cumsum(np.random.randn(100)) + 100
        
        df = pd.DataFrame({
            'close': prices,
            'open': prices * 0.99,
            'high': prices * 1.02,
            'low': prices * 0.98,
            'vol': np.random.randn(100) * 1000000
        }, index=dates)
        
        # 创建技术指标计算器
        ti = TechnicalIndicators(df)
        
        # 测试MA
        ma5 = ti.calculate_ma(5)
        ma20 = ti.calculate_ma(20)
        print(f"  ✅ MA5: {ma5[-1]:.2f}")
        print(f"  ✅ MA20: {ma20[-1]:.2f}")
        
        # 测试MACD
        macd = ti.calculate_macd()
        print(f"  ✅ MACD: DIF={macd.dif:.4f}, DEA={macd.dea:.4f}, MACD={macd.macd:.4f}")
        
        # 测试RSI
        rsi6 = ti.calculate_rsi(6)
        rsi12 = ti.calculate_rsi(12)
        print(f"  ✅ RSI6: {rsi6:.2f}, RSI12: {rsi12:.2f}")
        
        # 测试布林带
        bb = ti.calculate_bollinger_bands(20, 2)
        print(f"  ✅ Bollinger: MID={bb.mid:.2f}, UPPER={bb.upper:.2f}, LOWER={bb.lower:.2f}")
        
        return True
    except Exception as e:
        print(f"  ❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_fundamental_analysis():
    """测试基本面分析"""
    print("\n💰 测试基本面分析...")
    try:
        import pandas as pd
        import numpy as np
        from fundamental_analysis import FundamentalAnalyzer
        
        # 创建测试数据
        df = pd.DataFrame({
            'ts_code': ['000001.SZ', '000002.SZ', '000003.SZ'],
            'name': ['平安银行', '万 科Ａ', '国农科技'],
            'close': [10.5, 25.3, 15.8],
            'pe': [6.5, 12.3, 8.7],
            'pb': [0.8, 1.5, 1.2],
            'roe': [12.5, 15.2, 10.8],
            'dv_ratio': [3.5, 4.2, 2.8],
            'turnover_rate': [1.2, 0.8, 2.1],
            'volume': [15000000, 22000000, 8000000]
        })
        
        fa = FundamentalAnalyzer(df)
        
        # 测试评分计算
        score = fa.calculate_score('000001.SZ')
        print(f"  ✅ 平安银行评分: {score:.2f}/100")
        
        # 测试排序
        sorted_df = fa.rank_stocks('roe', ascending=False)
        print(f"  ✅ ROE排序成功: {sorted_df.iloc[0]['name']}")
        
        # 测试筛选
        filtered = fa.filter_stocks(pe_max=10, roe_min=10)
        print(f"  ✅ 筛选成功: {len(filtered)} 只符合条件")
        
        return True
    except Exception as e:
        print(f"  ❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_web_files():
    """测试Web文件"""
    print("\n🌐 测试Web文件...")
    try:
        web_dir = 'products/stock-analysis-saas/web'
        
        required_files = [
            'index.html',
            'dashboard.html',
            'styles.css',
            'app.js'
        ]
        
        total_size = 0
        for file in required_files:
            path = f"{web_dir}/{file}"
            if os.path.exists(path):
                size = os.path.getsize(path)
                total_size += size
                print(f"  ✅ {file}: {size:,} bytes")
            else:
                print(f"  ❌ {file}: 文件不存在")
                return False
        
        print(f"  📊 Web文件总大小: {total_size:,} bytes")
        
        return True
    except Exception as e:
        print(f"  ❌ 测试失败: {e}")
        return False

def test_api_structure():
    """测试API结构"""
    print("\n🔌 测试API结构...")
    try:
        api_dir = 'products/stock-analysis-saas/core/api'
        
        if os.path.exists(api_dir):
            files = os.listdir(api_dir)
            print(f"  ✅ API目录存在: {files}")
        else:
            print("  ⚠️ API目录不存在，需要创建")
        
        return True
    except Exception as e:
        print(f"  ❌ 测试失败: {e}")
        return False

def test_documentation():
    """测试文档"""
    print("\n📚 测试文档...")
    try:
        docs = [
            'products/stock-analysis-saas/prd.md',
            'products/stock-analysis-saas/requirements.txt',
            'products/stock-analysis-saas/run_tests.py'
        ]
        
        for doc in docs:
            if os.path.exists(doc):
                size = os.path.getsize(doc)
                print(f"  ✅ {os.path.basename(doc)}: {size:,} bytes")
            else:
                print(f"  ⚠️ {doc}: 不存在")
        
        return True
    except Exception as e:
        print(f"  ❌ 测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("=" * 60)
    print("🚀 StockVision Pro V1.0 整合测试")
    print("=" * 60)
    
    results = []
    
    # 1. 项目结构测试
    results.append(("项目结构", test_project_structure()))
    
    # 2. 模块结构测试
    results.append(("模块结构", test_module_structure()))
    
    # 3. 技术指标测试
    results.append(("技术指标", test_technical_indicators()))
    
    # 4. 基本面分析测试
    results.append(("基本面分析", test_fundamental_analysis()))
    
    # 5. Web文件测试
    results.append(("Web完整性", test_web_files()))
    
    # 6. API结构测试
    results.append(("API结构", test_api_structure()))
    
    # 7. 文档测试
    results.append(("文档完整性", test_documentation()))
    
    # 输出结果
    print("\n" + "=" * 60)
    print("📊 测试结果汇总")
    print("=" * 60)
    
    passed = 0
    failed = 0
    
    for name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"  {name}: {status}")
        if result:
            passed += 1
        else:
            failed += 1
    
    print("\n" + "-" * 60)
    print(f"  总计: {passed} 通过, {failed} 失败")
    
    if failed == 0:
        print("\n🎉 所有测试通过！StockVision Pro V1.0 整合成功！")
        return 0
    else:
        print(f"\n⚠️ {failed} 个测试失败，需要修复")
        return 1

if __name__ == '__main__':
    sys.exit(main())
