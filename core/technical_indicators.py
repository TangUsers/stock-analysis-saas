#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
技术指标库
提供各种股票技术指标计算功能

支持的指标:
- MA (移动平均线)
- MACD (指数平滑异同移动平均线)
- RSI (相对强弱指标)
- 布林带 (Bollinger Bands)
- 成交量分析

作者: Stock Analysis SaaS
版本: 1.0.0
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple, Union
from dataclasses import dataclass


@dataclass
class MAResult:
    """移动平均线结果"""
    ma5: float
    ma10: float
    ma20: float
    ma60: Optional[float] = None
    ma120: Optional[float] = None


@dataclass
class MACDResult:
    """MACD指标结果"""
    dif: float  # 快线 EMA12 - EMA26
    dea: float  # 慢线 DEA9
    macd: float  # 柱状图 (DIF - DEA) * 2
    hist: float  # 柱状图数值


@dataclass
class RSIResult:
    """RSI指标结果"""
    rsi6: float
    rsi12: float
    rsi24: float


@dataclass
class BollingerResult:
    """布林带结果"""
    upper: float
    middle: float
    lower: float
    bandwidth: float  # 带宽
    percent: float  # %B 指标


@dataclass
class VolumeResult:
    """成交量分析结果"""
    avg_volume: float
    latest_volume: float
    volume_change: float  # 百分比变化
    volume_trend: str  # 量价关系描述


class TechnicalIndicators:
    """
    技术指标计算器
    
    提供完整的技术分析指标计算功能，
    兼容pandas DataFrame和numpy数组输入
    """
    
    def __init__(self, price_data: Union[pd.DataFrame, np.ndarray, List]):
        """
        初始化技术指标计算器
        
        Args:
            price_data: 价格数据
                - pd.DataFrame: 需要包含 'close' 列
                - np.ndarray: 一维数组，假设为收盘价
                - List: 收盘价列表
        """
        self._validate_input(price_data)
        
        if isinstance(price_data, pd.DataFrame):
            if 'close' not in price_data.columns:
                raise ValueError("DataFrame必须包含 'close' 列")
            self.close = price_data['close'].values
            self.volume = price_data.get('vol', price_data.get('volume', None))
        else:
            self.close = np.array(price_data)
            self.volume = None
    
    def _validate_input(self, data) -> None:
        """验证输入数据"""
        if isinstance(data, (list, np.ndarray)):
            if len(data) == 0:
                raise ValueError("输入数据不能为空")
        elif isinstance(data, pd.DataFrame):
            if data.empty:
                raise ValueError("DataFrame不能为空")
        else:
            raise TypeError("输入类型必须是 list, np.ndarray 或 pd.DataFrame")
    
    # ==================== 移动平均线 (MA) ====================
    
    def calculate_ma(self, windows: List[int] = None) -> MAResult:
        """
        计算移动平均线
        
        Args:
            windows: 周期列表，默认 [5, 10, 20, 60, 120]
        
        Returns:
            MAResult对象，包含各周期MA值
        """
        if windows is None:
            windows = [5, 10, 20, 60, 120]
        
        ma_values = {}
        close_series = pd.Series(self.close)
        
        for window in windows:
            if len(self.close) >= window:
                ma_values[f'ma{window}'] = round(close_series.rolling(window=window).mean().iloc[-1], 2)
            else:
                # 数据不足时使用全部数据的平均值
                ma_values[f'ma{window}'] = round(close_series.mean(), 2)
        
        return MAResult(
            ma5=ma_values.get('ma5', 0),
            ma10=ma_values.get('ma10', 0),
            ma20=ma_values.get('ma20', 0),
            ma60=ma_values.get('ma60'),
            ma120=ma_values.get('ma120')
        )
    
    def calculate_ma_dict(self, windows: List[int] = None) -> Dict[str, float]:
        """
        计算移动平均线（返回字典格式）
        
        Returns:
            dict: {ma5: value, ma10: value, ...}
        """
        ma = self.calculate_ma(windows)
        result = {
            'MA5': ma.ma5,
            'MA10': ma.ma10,
            'MA20': ma.ma20
        }
        if ma.ma60:
            result['MA60'] = ma.ma60
        if ma.ma120:
            result['MA120'] = ma.ma120
        return result
    
    def get_ma_signal(self, ma_data: Dict[str, float] = None) -> Tuple[str, str]:
        """
        获取MA交易信号
        
        Args:
            ma_data: MA数据字典
        
        Returns:
            tuple: (信号类型, 描述)
                - 'bullish': 多头排列
                - 'bearish': 空头排列
                - 'neutral': 震荡整理
        """
        if ma_data is None:
            ma_data = self.calculate_ma_dict()
        
        ma5 = ma_data.get('MA5', 0)
        ma10 = ma_data.get('MA10', 0)
        ma20 = ma_data.get('MA20', 0)
        
        if ma5 > ma10 > ma20:
            return 'bullish', 'MA多头排列 - 短期上升趋势'
        elif ma5 < ma10 < ma20:
            return 'bearish', 'MA空头排列 - 短期下降趋势'
        else:
            return 'neutral', 'MA震荡整理 - 方向不明确'
    
    # ==================== MACD ====================
    
    def calculate_macd(self, fast: int = 12, slow: int = 26, signal: int = 9) -> MACDResult:
        """
        计算MACD指标
        
        Args:
            fast: 快速EMA周期，默认12
            slow: 慢速EMA周期，默认26
            signal: 信号线周期，默认9
        
        Returns:
            MACDResult对象
        """
        close_series = pd.Series(self.close)
        
        # 计算EMA
        ema_fast = close_series.ewm(span=fast, adjust=False).mean()
        ema_slow = close_series.ewm(span=slow, adjust=False).mean()
        
        dif = ema_fast.iloc[-1] - ema_slow.iloc[-1]
        dea = close_series.ewm(span=signal, adjust=False).mean().iloc[-1]
        hist = (dif - dea) * 2
        
        return MACDResult(
            dif=round(dif, 4),
            dea=round(dea, 4),
            macd=round(hist, 4),
            hist=round(hist, 4)
        )
    
    def calculate_macd_dict(self, fast: int = 12, slow: int = 26, signal: int = 9) -> Dict[str, float]:
        """
        计算MACD指标（返回字典格式）
        
        Returns:
            dict: {DIF: value, DEA: value, MACD: value}
        """
        macd = self.calculate_macd(fast, slow, signal)
        return {
            'DIF': macd.dif,
            'DEA': macd.dea,
            'MACD': macd.macd
        }
    
    def get_macd_signal(self, macd_data: Dict[str, float] = None) -> Tuple[str, str]:
        """
        获取MACD交易信号
        
        Args:
            macd_data: MACD数据字典
        
        Returns:
            tuple: (信号类型, 描述)
        """
        if macd_data is None:
            macd_data = self.calculate_macd_dict()
        
        dif = macd_data.get('DIF', 0)
        dea = macd_data.get('DEA', 0)
        macd = macd_data.get('MACD', 0)
        
        # 判断金叉死叉
        if dif > dea and macd > 0:
            return 'bullish', 'MACD金叉多头 - 上升趋势确认'
        elif dif < dea and macd < 0:
            return 'bearish', 'MACD死叉空头 - 下降趋势确认'
        elif macd > 0:
            return 'bullish', 'MACD柱为正 - 多方市场'
        elif macd < 0:
            return 'bearish', 'MACD柱为负 - 空方市场'
        else:
            return 'neutral', 'MACD零轴附近 - 震荡整理'
    
    # ==================== RSI ====================
    
    def calculate_rsi(self, periods: List[int] = None) -> RSIResult:
        """
        计算RSI指标
        
        Args:
            periods: 周期列表，默认 [6, 12, 24]
        
        Returns:
            RSIResult对象
        """
        if periods is None:
            periods = [6, 12, 24]
        
        close_series = pd.Series(self.close)
        delta = close_series.diff()
        
        rsi_values = {}
        
        for period in periods:
            if len(self.close) >= period:
                gain = delta.where(delta > 0, 0).rolling(window=period).mean()
                loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
                
                rs = gain / loss
                rsi = 100 - (100 / (1 + rs))
                rsi_values[f'rsi{period}'] = round(rsi.iloc[-1], 2)
            else:
                rsi_values[f'rsi{period}'] = 50.0
        
        return RSIResult(
            rsi6=rsi_values.get('rsi6', 50),
            rsi12=rsi_values.get('rsi12', 50),
            rsi24=rsi_values.get('rsi24', 50)
        )
    
    def calculate_rsi_dict(self, periods: List[int] = None) -> Dict[str, float]:
        """
        计算RSI指标（返回字典格式）
        
        Returns:
            dict: {RSI6: value, RSI12: value, RSI24: value}
        """
        rsi = self.calculate_rsi(periods)
        return {
            'RSI6': rsi.rsi6,
            'RSI12': rsi.rsi12,
            'RSI24': rsi.rsi24
        }
    
    def get_rsi_signal(self, rsi_data: Dict[str, float] = None, period: int = 6) -> Tuple[str, str]:
        """
        获取RSI交易信号
        
        Args:
            rsi_data: RSI数据字典
            period: 参考周期，默认6
        
        Returns:
            tuple: (信号类型, 描述)
        """
        if rsi_data is None:
            rsi_data = self.calculate_rsi_dict()
        
        rsi_key = f'RSI{period}'
        rsi = rsi_data.get(rsi_key, 50)
        
        if rsi >= 80:
            return 'overbought', f'RSI超买 ({rsi:.1f}) - 严重超买，注意回调'
        elif rsi >= 70:
            return 'overbought', f'RSI超买 ({rsi:.1f}) - 警惕回调风险'
        elif rsi <= 20:
            return 'oversold', f'RSI超卖 ({rsi:.1f}) - 严重超卖，可能反弹'
        elif rsi <= 30:
            return 'oversold', f'RSI超卖 ({rsi:.1f}) - 关注反弹机会'
        elif 40 <= rsi <= 60:
            return 'neutral', f'RSI中性 ({rsi:.1f}) - 多空平衡'
        elif rsi > 60:
            return 'bullish', f'RSI偏多 ({rsi:.1f}) - 多方占优'
        else:
            return 'bearish', f'RSI偏空 ({rsi:.1f}) - 空方占优'
    
    # ==================== 布林带 ====================
    
    def calculate_bollinger_bands(self, window: int = 20, std_dev: float = 2.0) -> BollingerResult:
        """
        计算布林带
        
        Args:
            window: 周期，默认20
            std_dev: 标准差倍数，默认2
        
        Returns:
            BollingerResult对象
        """
        close_series = pd.Series(self.close)
        
        if len(self.close) >= window:
            middle = close_series.rolling(window=window).mean().iloc[-1]
            rolling_std = close_series.rolling(window=window).std().iloc[-1]
        else:
            middle = close_series.mean()
            rolling_std = close_series.std()
        
        upper = middle + (std_dev * rolling_std)
        lower = middle - (std_dev * rolling_std)
        
        # 计算%B (价格在布林带中的位置)
        latest_close = self.close[-1]
        if upper != lower:
            percent_b = (latest_close - lower) / (upper - lower)
        else:
            percent_b = 0.5
        
        # 计算带宽
        bandwidth = (upper - middle) / middle * 100 if middle != 0 else 0
        
        return BollingerResult(
            upper=round(upper, 2),
            middle=round(middle, 2),
            lower=round(lower, 2),
            bandwidth=round(bandwidth, 2),
            percent=round(percent_b, 4)
        )
    
    def calculate_bollinger_dict(self, window: int = 20, std_dev: float = 2.0) -> Dict[str, float]:
        """
        计算布林带（返回字典格式）
        
        Returns:
            dict: {BB_UPPER: value, BB_MIDDLE: value, BB_LOWER: value}
        """
        bb = self.calculate_bollinger_bands(window, std_dev)
        return {
            'BB_UPPER': bb.upper,
            'BB_MIDDLE': bb.middle,
            'BB_LOWER': bb.lower
        }
    
    def get_bollinger_signal(self, bb_data: Dict[str, float] = None, price: float = None) -> Tuple[str, str]:
        """
        获取布林带交易信号
        
        Args:
            bb_data: 布林带数据字典
            price: 最新价格
        
        Returns:
            tuple: (信号类型, 描述)
        """
        if bb_data is None:
            bb_data = self.calculate_bollinger_dict()
        
        if price is None:
            price = self.close[-1]
        
        upper = bb_data.get('BB_UPPER', 0)
        lower = bb_data.get('BB_LOWER', 0)
        
        if price >= upper:
            return 'overbought', '价格触及上轨 - 超买风险'
        elif price <= lower:
            return 'oversold', '价格触及下轨 - 超卖机会'
        else:
            # 计算价格在布林带中的相对位置
            position = (price - lower) / (upper - lower) if upper != lower else 0.5
            
            if position > 0.75:
                return 'bullish', f'价格偏上轨 ({position*100:.0f}%) - 偏多'
            elif position < 0.25:
                return 'bearish', f'价格偏下轨 ({position*100:.0f}%) - 偏空'
            else:
                return 'neutral', f'价格中轨附近 ({position*100:.0f}%) - 震荡整理'
    
    # ==================== 成交量分析 ====================
    
    def analyze_volume(self, volume_data: np.ndarray = None) -> VolumeResult:
        """
        成交量分析
        
        Args:
            volume_data: 成交量数组，如果为None则使用初始化时的成交量
        
        Returns:
            VolumeResult对象
        """
        if volume_data is not None:
            volume = np.array(volume_data)
        elif self.volume is not None:
            volume = np.array(self.volume)
        else:
            raise ValueError("未提供成交量数据")
        
        if len(volume) < 2:
            return VolumeResult(
                avg_volume=volume[0] if len(volume) > 0 else 0,
                latest_volume=volume[0] if len(volume) > 0 else 0,
                volume_change=0,
                volume_trend='数据不足'
            )
        
        avg_volume = np.mean(volume[:-1])  # 除了最新一天的平均
        latest_volume = volume[-1]
        prev_volume = volume[-2]
        
        volume_change = ((latest_volume - prev_volume) / prev_volume * 100) if prev_volume > 0 else 0
        
        # 量价关系分析
        close = self.close
        if len(close) >= 2:
            price_change = (close[-1] - close[-2]) / close[-2] * 100
        else:
            price_change = 0
        
        if volume_change > 20 and price_change > 0:
            volume_trend = "量价齐升（健康上涨）"
        elif volume_change > 20 and price_change < 0:
            volume_trend = "量增价跌（主力出货）"
        elif volume_change < -20 and price_change < 0:
            volume_trend = "量价齐跌（筑底整理）"
        elif volume_change < -20 and price_change > 0:
            volume_trend = "无量上涨（虚涨诱多）"
        elif abs(volume_change) <= 20:
            volume_trend = "量价平稳（正常整理）"
        else:
            volume_trend = "量能异动"
        
        return VolumeResult(
            avg_volume=round(avg_volume, 0),
            latest_volume=round(latest_volume, 0),
            volume_change=round(volume_change, 2),
            volume_trend=volume_trend
        )
    
    def analyze_volume_dict(self, volume_data: np.ndarray = None) -> Dict:
        """
        成交量分析（返回字典格式）
        """
        vol = self.analyze_volume(volume_data)
        return {
            'avg_volume': vol.avg_volume,
            'latest_volume': vol.latest_volume,
            'volume_change': vol.volume_change,
            'volume_trend': vol.volume_trend
        }
    
    # ==================== 综合分析 ====================
    
    def get_all_indicators(self) -> Dict:
        """
        获取所有技术指标
        
        Returns:
            dict: 包含所有指标的字典
        """
        return {
            'ma': self.calculate_ma_dict(),
            'macd': self.calculate_macd_dict(),
            'rsi': self.calculate_rsi_dict(),
            'bollinger': self.calculate_bollinger_dict(),
            'volume': self.analyze_volume_dict()
        }
    
    def get_composite_signal(self) -> Dict:
        """
        获取综合交易信号
        
        Returns:
            dict: 综合信号分析结果
        """
        ma_signal, ma_desc = self.get_ma_signal()
        macd_signal, macd_desc = self.get_macd_signal()
        rsi_signal, rsi_desc = self.get_rsi_signal()
        bb_signal, bb_desc = self.get_bollinger_signal()
        
        # 计算综合评分
        score = 50  # 基础分
        
        # MA评分
        if ma_signal == 'bullish':
            score += 15
        elif ma_signal == 'bearish':
            score -= 15
        
        # MACD评分
        if macd_signal == 'bullish':
            score += 10
        elif macd_signal == 'bearish':
            score -= 10
        
        # RSI评分
        rsi_data = self.calculate_rsi_dict()
        rsi6 = rsi_data.get('RSI6', 50)
        if 40 < rsi6 < 70:
            score += 5
        elif rsi6 >= 70:
            score -= 10
        elif rsi6 <= 30:
            score -= 10
        
        # 布林带评分
        bb_data = self.calculate_bollinger_dict()
        price = self.close[-1]
        if price < bb_data.get('BB_LOWER', price):
            score += 5  # 超卖反弹机会
        elif price > bb_data.get('BB_UPPER', price):
            score -= 5  # 超买风险
        
        # 限制分数范围
        score = max(0, min(100, score))
        
        # 判断整体趋势
        if score >= 70:
            trend = '看多'
        elif score <= 30:
            trend = '看空'
        else:
            trend = '震荡'
        
        return {
            'composite_score': score,
            'trend': trend,
            'ma_signal': ma_signal,
            'ma_description': ma_desc,
            'macd_signal': macd_signal,
            'macd_description': macd_desc,
            'rsi_signal': rsi_signal,
            'rsi_description': rsi_desc,
            'bollinger_signal': bb_signal,
            'bollinger_description': bb_desc,
            'signals': [ma_desc, macd_desc, rsi_desc, bb_desc]
        }


# ==================== 便捷函数 ====================

def calculate_ma(prices: List[float], window: int) -> float:
    """
    便捷函数：计算单个MA值
    
    Args:
        prices: 价格列表
        window: 周期
    
    Returns:
        float: MA值
    """
    if len(prices) < window:
        return round(np.mean(prices), 2)
    return round(np.mean(prices[-window:]), 2)


def calculate_rsi(prices: List[float], period: int = 14) -> float:
    """
    便捷函数：计算单个RSI值
    
    Args:
        prices: 价格列表
        period: 周期
    
    Returns:
        float: RSI值
    """
    if len(prices) < period + 1:
        return 50.0
    
    close_series = pd.Series(prices)
    delta = close_series.diff()
    gain = delta.where(delta > 0, 0).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return round(rsi.iloc[-1], 2)


def calculate_macd(prices: List[float], fast: int = 12, slow: int = 26) -> Dict[str, float]:
    """
    便捷函数：计算MACD值
    
    Args:
        prices: 价格列表
        fast: 快速EMA周期
        slow: 慢速EMA周期
    
    Returns:
        dict: {DIF: value, DEA: value, MACD: value}
    """
    close_series = pd.Series(prices)
    
    ema_fast = close_series.ewm(span=fast, adjust=False).mean()
    ema_slow = close_series.ewm(span=slow, adjust=False).mean()
    
    dif = ema_fast.iloc[-1] - ema_slow.iloc[-1]
    dea = close_series.ewm(span=9, adjust=False).mean().iloc[-1]
    macd = (dif - dea) * 2
    
    return {
        'DIF': round(dif, 4),
        'DEA': round(dea, 4),
        'MACD': round(macd, 4)
    }
