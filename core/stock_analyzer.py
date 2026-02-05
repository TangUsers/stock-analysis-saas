#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
股票分析器
整合技术分析和基本面分析的综合选股系统

核心功能:
- 股票筛选引擎
- 评分算法优化
- 实时数据获取 (使用Baostock)

作者: Stock Analysis SaaS
版本: 1.0.0
"""

import baostock as bs
import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple, Union
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.technical_indicators import TechnicalIndicators
from core.fundamental_analysis import FundamentalAnalyzer


@dataclass
class StockData:
    """股票数据结构"""
    ts_code: str
    name: str
    date: str
    close: float
    open: float
    high: float
    low: float
    volume: float
    turnover_rate: float
    pe: float
    pb: float
    roe: float
    dv_ratio: float
    market_cap: float


class StockAnalyzer:
    """
    股票分析器
    
    整合技术分析和基本面分析，提供完整的选股功能
    """
    
    def __init__(self):
        """初始化股票分析器"""
        self.lg = None  # Baostock登录对象
        self.analyzer = FundamentalAnalyzer()
    
    # ==================== Baostock连接 ====================
    
    def connect(self) -> bool:
        """
        连接Baostock
        
        Returns:
            bool: 连接是否成功
        """
        try:
            self.lg = bs.login()
            return self.lg.error_code == '0'
        except Exception as e:
            print(f"Baostock连接失败: {e}")
            return False
    
    def disconnect(self) -> None:
        """断开Baostock连接"""
        if self.lg:
            bs.logout()
            self.lg = None
    
    def __enter__(self):
        """上下文管理器入口"""
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """上下文管理器退出"""
        self.disconnect()
    
    # ==================== 数据获取 ====================
    
    def get_latest_trade_date(self) -> str:
        """
        获取最近的交易日
        
        Returns:
            str: 日期字符串 (YYYY-MM-DD)
        """
        # 获取最近30天的交易日历
        end_date = (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d')
        start_date = (datetime.now() - timedelta(days=60)).strftime('%Y-%m-%d')
        
        rs = bs.query_trade_cal(
            start_date=start_date,
            end_date=end_date,
            fields='cal_date,is_open'
        )
        
        open_days = []
        while rs.error_code == '0' and rs.next():
            if rs.get_row_data()[1] == '1':
                open_days.append(rs.get_row_data()[0])
        
        if open_days:
            return open_days[-1]
        
        # 默认返回最近的前一个工作日
        return (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    
    def get_market_stocks(self) -> pd.DataFrame:
        """
        获取全市场股票列表
        
        Returns:
            pd.DataFrame: 股票列表
        """
        print("📋 获取全市场股票列表...")
        
        # 获取沪市股票
        rs_sh = bs.query_sh_a_sse()
        stocks_sh = []
        while rs_sh.error_code == '0' and rs_sh.next():
            stocks_sh.append(rs_sh.get_row_data())
        
        # 获取深市股票
        rs_sz = bs.query_sz_a_sse()
        stocks_sz = []
        while rs_sz.error_code == '0' and rs_sz.next():
            stocks_sz.append(rs_sz.get_row_data())
        
        all_stocks = stocks_sh + stocks_sz
        
        if all_stocks:
            columns = rs_sh.fields if stocks_sh else rs_sz.fields
            df = pd.DataFrame(all_stocks, columns=columns)
            
            # 过滤掉ST、新股等
            if 'name' in df.columns:
                df = df[~df['name'].str.contains('ST|N天|退', na=False)]
            
            print(f"  筛选后股票数量: {len(df)}")
            return df
        
        print("  ⚠️ 获取股票列表失败")
        return pd.DataFrame()
    
    def get_daily_basic(
        self,
        trade_date: str = None,
        codes: List[str] = None
    ) -> pd.DataFrame:
        """
        获取每日基本面数据
        
        Args:
            trade_date: 交易日期，默认为最近交易日
            codes: 股票代码列表
        
        Returns:
            pd.DataFrame: 基本面数据
        """
        if trade_date is None:
            trade_date = self.get_latest_trade_date()
        
        print(f"📊 获取基本面数据 (交易日: {trade_date})...")
        
        if codes:
            # 批量获取
            all_data = []
            batch_size = 500
            
            for i in range(0, len(codes), batch_size):
                batch = codes[i:i+batch_size]
                code_str = ','.join(batch)
                
                rs = bs.query_daily_basic(
                    trade_date=trade_date,
                    code=code_str,
                    fields='code,close,pe,pb,ps,pcf,dv_ratio,dv_ttm,turnover_rate,volume,market_cap'
                )
                
                while rs.error_code == '0' and rs.next():
                    all_data.append(rs.get_row_data())
                
                print(f"  批次 {i//batch_size + 1}: {len([r for r in all_data])} 条")
            
            if all_data:
                return pd.DataFrame(all_data, columns=rs.fields)
        else:
            # 获取全市场
            rs = bs.query_daily_basic(
                trade_date=trade_date,
                fields='code,close,pe,pb,ps,pcf,dv_ratio,dv_ttm,turnover_rate,volume,market_cap'
            )
            
            data = []
            while rs.error_code == '0' and rs.next():
                data.append(rs.get_row_data())
            
            if data:
                print(f"  获取成功: {len(data)} 条")
                return pd.DataFrame(data, columns=rs.fields)
        
        print("  ⚠️ 未能获取基本面数据")
        return pd.DataFrame()
    
    def get_kline_data(
        self,
        code: str,
        start_date: str = None,
        end_date: str = None,
        frequency: str = 'd',
        adjust_type: str = 'qfq'
    ) -> pd.DataFrame:
        """
        获取K线数据
        
        Args:
            code: 股票代码 (sh.600000 或 sz.000001)
            start_date: 开始日期
            end_date: 结束日期
            frequency: 频率 ('d'=日线, 'w'=周线, 'm'=月线)
            adjust_type: 复权类型 ('qfq'=前复权, 'hfq'=后复权, 'none'=不复权)
        
        Returns:
            pd.DataFrame: K线数据
        """
        if start_date is None:
            start_date = (datetime.now() - timedelta(days=120)).strftime('%Y-%m-%d')
        
        if end_date is None:
            end_date = datetime.now().strftime('%Y-%m-%d')
        
        rs = bs.query_history_k_data_plus(
            code,
            fields='date,code,open,high,low,close,volume,amount,adjustflag',
            start_date=start_date,
            end_date=end_date,
            frequency=frequency,
            adjustflag=adjust_type
        )
        
        data = []
        while rs.error_code == '0' and rs.next():
            data.append(rs.get_row_data())
        
        if data:
            df = pd.DataFrame(data, columns=rs.fields)
            # 转换数值类型
            numeric_cols = ['open', 'high', 'low', 'close', 'volume']
            for col in numeric_cols:
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors='coerce')
            return df
        
        return pd.DataFrame()
    
    def get_financial_indicator(
        self,
        codes: List[str],
        report_date: str = None
    ) -> pd.DataFrame:
        """
        获取财务指标
        
        Args:
            codes: 股票代码列表
            report_date: 报告期
        
        Returns:
            pd.DataFrame: 财务指标数据
        """
        if report_date is None:
            # 默认使用最新报告期
            report_date = (datetime.now() - timedelta(days=90)).strftime('%Y-%m-%d')
        
        all_data = []
        
        for code in codes:
            rs = bs.query_fina_indicator(
                code,
                start_date=report_date,
                fields='code,roe,netprofit_margin,grossprofit_margin'
            )
            
            while rs.error_code == '0' and rs.next():
                all_data.append(rs.get_row_data())
        
        if all_data:
            return pd.DataFrame(all_data, columns=rs.fields)
        
        return pd.DataFrame()
    
    # ==================== 股票分析 ====================
    
    def analyze_stock(
        self,
        code: str,
        name: str = None
    ) -> Dict:
        """
        分析单只股票
        
        Args:
            code: 股票代码
            name: 股票名称
        
        Returns:
            dict: 完整分析结果
        """
        # 获取K线数据
        df = self.get_kline_data(code)
        
        if df.empty or len(df) < 20:
            return {'error': f'无法获取 {code} 的数据'}
        
        # 技术分析
        ti = TechnicalIndicators(df)
        tech_indicators = ti.get_all_indicators()
        tech_signal = ti.get_composite_signal()
        
        # 提取最新价格数据
        latest = df.iloc[-1]
        prev = df.iloc[-2] if len(df) >= 2 else latest
        
        price_data = {
            'close': float(latest['close']),
            'open': float(latest['open']),
            'high': float(latest['high']),
            'low': float(latest['low']),
            'pct_change': float((latest['close'] - prev['close']) / prev['close'] * 100) if prev['close'] > 0 else 0
        }
        
        return {
            'code': code,
            'name': name or code,
            'date': latest['date'],
            'price': price_data,
            'technical_analysis': {
                'indicators': tech_indicators,
                'composite_signal': tech_signal
            }
        }
    
    def screen_stocks(
        self,
        criteria: Dict = None,
        data: pd.DataFrame = None
    ) -> pd.DataFrame:
        """
        股票筛选
        
        Args:
            criteria: 筛选条件
            data: 股票数据
        
        Returns:
            pd.DataFrame: 筛选后的股票
        """
        # 使用基本面分析器的筛选功能
        df_filtered = self.analyzer.filter_stocks(filters=criteria, data=data)
        
        # 计算评分
        df_scored = self.analyzer.calculate_composite_score(data=df_filtered)
        
        # 按综合评分排序
        df_ranked = df_scored.sort_values('composite_score', ascending=False)
        
        return df_ranked
    
    def get_top_recommendations(
        self,
        data: pd.DataFrame = None,
        top_n: int = 10,
        filters: Dict = None,
        weights: Dict = None
    ) -> List[Dict]:
        """
        获取Top推荐股票
        
        Args:
            data: 股票数据
            top_n: 返回前N只
            filters: 筛选条件
            weights: 评分权重
        
        Returns:
            list: 推荐股票列表
        """
        if data is None:
            # 需要先获取数据
            if not self.lg:
                self.connect()
            
            data = self.get_daily_basic()
        
        if data.empty:
            return []
        
        # 筛选
        df_filtered = self.analyzer.filter_stocks(filters=filters, data=data)
        
        if df_filtered.empty:
            print("⚠️ 筛选后无股票，尝试放宽条件...")
            df_filtered = data.copy()
            df_filtered = df_filtered[df_filtered['pe'].notna() & (df_filtered['pe'] > 0)]
            df_filtered = df_filtered[df_filtered['pe'] < 100]
        
        # 评分
        df_scored = self.analyzer.calculate_composite_score(weights=weights, data=df_filtered)
        
        # 排序取Top N
        df_top = df_scored.sort_values('composite_score', ascending=False).head(top_n)
        
        # 转换为字典列表
        recommendations = []
        for idx, row in df_top.iterrows():
            stock = row.to_dict()
            stock['rank'] = len(recommendations) + 1
            recommendations.append(stock)
        
        return recommendations
    
    # ==================== 报告生成 ====================
    
    def generate_recommendation_report(
        self,
        recommendations: List[Dict],
        filename: str = None
    ) -> Dict:
        """
        生成推荐报告
        
        Args:
            recommendations: 推荐股票列表
            filename: 文件名
        
        Returns:
            dict: 报告内容
        """
        report = {
            'report_date': datetime.now().strftime('%Y-%m-%d'),
            'report_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'total_recommendations': len(recommendations),
            'recommendations': []
        }
        
        for stock in recommendations:
            rec = {
                'rank': stock['rank'],
                'code': stock.get('code', ''),
                'close': round(float(stock.get('close', 0)), 2),
                'pe': round(float(stock.get('pe', 0)), 2),
                'pb': round(float(stock.get('pb', 0)), 2),
                'roe': round(float(stock.get('roe', 0)), 2),
                'dividend_ratio': round(float(stock.get('dv_ratio', 0)), 2),
                'turnover_rate': round(float(stock.get('turnover_rate', 0)), 2),
                'market_cap': stock.get('market_cap', None),
                'composite_score': round(float(stock['composite_score']), 2),
                'score_breakdown': {
                    'pe_score': round(float(stock['pe_score']), 2),
                    'pb_score': round(float(stock['pb_score']), 2),
                    'roe_score': round(float(stock['roe_score']), 2),
                    'dividend_score': round(float(stock['dividend_score']), 2),
                    'liquidity_score': round(float(stock['liquidity_score']), 2)
                }
            }
            report['recommendations'].append(rec)
        
        # 保存文件
        if filename:
            import json
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(report, f, ensure_ascii=False, indent=2)
            print(f"✅ 报告已保存: {filename}")
        
        return report
    
    def generate_markdown_report(
        self,
        recommendations: List[Dict],
        filename: str = None
    ) -> str:
        """
        生成Markdown格式报告
        
        Args:
            recommendations: 推荐股票列表
            filename: 文件名
        
        Returns:
            str: Markdown内容
        """
        gen_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        date_str = datetime.now().strftime('%Y-%m-%d')
        
        md = f"""# 每日股票推荐报告

**生成时间**: {gen_time}

## 📊 报告摘要

- **分析日期**: {date_str}
- **推荐股票数量**: {len(recommendations)} 只

---

## 🏆 推荐股票

| 排名 | 代码 | 收盘价 | PE | PB | ROE(%) | 股息率(%) | 换手率(%) | 综合评分 |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:"""

        for stock in recommendations:
            code = stock.get('code', '')
            close = f"{stock.get('close', 0):.2f}"
            pe = f"{stock.get('pe', 0):.2f}"
            pb = f"{stock.get('pb', 0):.2f}"
            roe = f"{stock.get('roe', 0):.2f}"
            dv = f"{stock.get('dv_ratio', 0):.2f}"
            tr = f"{stock.get('turnover_rate', 0):.2f}"
            score = f"**{stock['composite_score']:.1f}**"
            
            md += f"\n| {stock['rank']} | {code} | {close} | {pe} | {pb} | {roe} | {dv} | {tr} | {score} |"

        md += """

---

## 📈 评分详情

### 评分体系说明

| 指标 | 权重 | 说明 |
|:---|:---:|:---|
| PE (市盈率) | 25% | 越低越好 |
| PB (市净率) | 20% | 越低越好 |
| ROE (净资产收益率) | 25% | 越高越好 |
| 股息率 | 20% | 越高越好 |
| 流动性 (换手率) | 10% | 适中为佳 |

---

## ⚠️ 风险提示

1. **市场风险**: 股市有风险，投资需谨慎
2. **模型局限**: 本推荐基于量化模型，不构成投资建议
3. **数据延迟**: 数据可能存在延迟，请以交易所公告为准
4. **个人判断**: 请结合个人风险承受能力和投资目标做出决策

---

*报告由 Stock Analysis SaaS 自动生成*
"""
        
        # 保存文件
        if filename:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(md)
            print(f"✅ Markdown报告已保存: {filename}")
        
        return md
    
    # ==================== 主流程 ====================
    
    def run_daily_analysis(
        self,
        output_dir: str = None,
        top_n: int = 10
    ) -> Dict:
        """
        执行每日股票分析
        
        Args:
            output_dir: 输出目录
            top_n: 推荐Top N
        
        Returns:
            dict: 分析结果
        """
        print("=" * 60)
        print("🚀 每日股票推荐系统启动")
        print("=" * 60)
        
        # 确保已连接
        if not self.lg:
            self.connect()
        
        # 1. 获取全市场股票
        stocks = self.get_market_stocks()
        
        if stocks.empty:
            print("❌ 获取股票列表失败")
            return {'status': 'error', 'message': '获取股票列表失败'}
        
        # 2. 获取基本面数据
        trade_date = self.get_latest_trade_date()
        daily_basic = self.get_daily_basic(trade_date=trade_date)
        
        if daily_basic.empty:
            print("❌ 获取基本面数据失败")
            return {'status': 'error', 'message': '获取基本面数据失败'}
        
        # 合并数据
        if 'code' in daily_basic.columns and 'code' in stocks.columns:
            df = daily_basic.merge(
                stocks[['code', 'name']],
                on='code',
                how='left'
            )
        else:
            df = daily_basic.copy()
            df['name'] = ''
        
        print(f"📊 合并后股票数量: {len(df)}")
        
        # 3. 获取Top推荐
        recommendations = self.get_top_recommendations(
            data=df,
            top_n=top_n
        )
        
        if not recommendations:
            print("⚠️ 未找到符合条件的股票")
            return {'status': 'warning', 'message': '未找到符合条件的股票'}
        
        print(f"\n🏆 Top {top_n} 推荐股票:")
        print("-" * 60)
        for stock in recommendations[:5]:
            print(f"  {stock['rank']}. {stock.get('code', '')} {stock.get('name', '')}")
            print(f"     评分: {stock['composite_score']:.1f} | PE: {stock.get('pe', 0):.1f} | PB: {stock.get('pb', 0):.2f}")
        
        # 4. 生成报告
        if output_dir:
            import os
            os.makedirs(output_dir, exist_ok=True)
            
            date_str = datetime.now().strftime('%Y-%m-%d')
            
            json_file = f"{output_dir}/recommendations-{date_str}.json"
            md_file = f"{output_dir}/recommendations-{date_str}.md"
            
            self.generate_recommendation_report(recommendations, json_file)
            self.generate_markdown_report(recommendations, md_file)
        
        print("\n" + "=" * 60)
        print("✅ 每日股票分析完成!")
        print("=" * 60)
        
        return {
            'status': 'success',
            'trade_date': trade_date,
            'total_analyzed': len(df),
            'recommendations': recommendations
        }


# ==================== 便捷函数 ====================

def quick_analyze(code: str, name: str = None) -> Dict:
    """
    快速分析单只股票
    
    Args:
        code: 股票代码
        name: 股票名称
    
    Returns:
        dict: 分析结果
    """
    analyzer = StockAnalyzer()
    
    with analyzer:
        return analyzer.analyze_stock(code, name)


def get_recommendations(top_n: int = 10, filters: Dict = None) -> List[Dict]:
    """
    获取推荐股票
    
    Args:
        top_n: 推荐数量
        filters: 筛选条件
    
    Returns:
        list: 推荐股票列表
    """
    analyzer = StockAnalyzer()
    
    with analyzer:
        return analyzer.get_top_recommendations(top_n=top_n, filters=filters)


# ==================== 主程序 ====================

if __name__ == '__main__':
    import os
    
    # 创建分析器
    analyzer = StockAnalyzer()
    
    # 执行每日分析
    output_dir = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        'outputs', 'recommendations'
    )
    
    result = analyzer.run_daily_analysis(output_dir=output_dir, top_n=10)
    
    if result['status'] == 'success':
        print(f"\n📊 共推荐 {len(result['recommendations'])} 只股票")
