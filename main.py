#!/usr/bin/env python3
"""
StockVision Pro - FastAPI 后端服务
"""

from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime
import uvicorn
import os

# 导入内部模块
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.stock_analyzer import StockAnalyzer
from core.technical_indicators import TechnicalIndicators
from core.fundamental_analysis import FundamentalAnalyzer

app = FastAPI(
    title="StockVision Pro API",
    description="AI驱动的智能股票分析平台API",
    version="1.0.0"
)

# CORS配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 初始化分析器
stock_analyzer = StockAnalyzer()

# ============ 数据模型 ============

class StockQuery(BaseModel):
    """股票查询请求"""
    ts_code: Optional[str] = None
    stock_name: Optional[str] = None

class FilterRequest(BaseModel):
    """筛选请求"""
    pe_max: float = 50
    pb_max: float = 5
    roe_min: float = 5
    dividend_min: float = 0
    turnover_rate_min: float = 0.5
    turnover_rate_max: float = 15

class ScoreRequest(BaseModel):
    """评分请求"""
    pe: float
    pb: float
    roe: float
    dividend: float
    turnover_rate: float

class UserCreate(BaseModel):
    """用户创建"""
    email: EmailStr
    username: str
    password: str

class UserLogin(BaseModel):
    """用户登录"""
    email: EmailStr
    password: str

# ============ API 端点 ============

@app.get("/")
async def root():
    """根路径"""
    return {
        "name": "StockVision Pro API",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs"
    }

@app.get("/api/health")
async def health_check():
    """健康检查"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

# ============ 股票接口 ============

@app.get("/api/stocks")
async def get_stocks():
    """获取股票列表"""
    try:
        stocks = stock_analyzer.get_stock_list()
        return {
            "success": True,
            "data": stocks,
            "count": len(stocks)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/stocks/filter")
async def filter_stocks(request: FilterRequest):
    """筛选股票"""
    try:
        stocks = stock_analyzer.filter_stocks(
            pe_max=request.pe_max,
            pb_max=request.pb_max,
            roe_min=request.roe_min,
            dividend_min=request.dividend_min,
            turnover_rate_min=request.turnover_rate_min,
            turnover_rate_max=request.turnover_rate_max
        )
        return {
            "success": True,
            "data": stocks,
            "count": len(stocks)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/stocks/analyze")
async def analyze_stock(query: StockQuery):
    """分析单只股票"""
    try:
        if query.ts_code:
            stock = stock_analyzer.get_stock_info(query.ts_code)
        elif query.stock_name:
            stock = stock_analyzer.get_stock_by_name(query.stock_name)
        else:
            raise HTTPException(status_code=400, detail="需要提供股票代码或名称")
        
        if stock is None:
            raise HTTPException(status_code=404, detail="股票未找到")
        
        return {
            "success": True,
            "data": stock
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/stocks/technical")
async def get_technical_analysis(stock_code: str):
    """获取技术分析"""
    try:
        # 获取股票数据
        stock = stock_analyzer.get_stock_info(stock_code)
        if stock is None:
            raise HTTPException(status_code=404, detail="股票未找到")
        
        # 计算技术指标
        ti = TechnicalIndicators(stock['price_data'])
        ta = {
            'ma': {
                'ma5': ti.calculate_ma(5),
                'ma10': ti.calculate_ma(10),
                'ma20': ti.calculate_ma(20)
            },
            'macd': ti.calculate_macd(),
            'rsi': {
                'rsi6': ti.calculate_rsi(6),
                'rsi12': ti.calculate_rsi(12),
                'rsi24': ti.calculate_rsi(24)
            },
            'bollinger': ti.calculate_bollinger_bands(20, 2)
        }
        
        return {
            "success": True,
            "data": {
                "stock": stock,
                "technical_analysis": ta
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/stocks/score")
async def calculate_score(request: ScoreRequest):
    """计算综合评分"""
    try:
        fa = FundamentalAnalyzer()
        score = fa.calculate_score(
            pe=request.pe,
            pb=request.pb,
            roe=request.roe,
            dividend=request.dividend,
            turnover_rate=request.turnover_rate
        )
        
        return {
            "success": True,
            "data": {
                "score": score,
                "grade": "A" if score >= 80 else "B" if score >= 60 else "C" if score >= 40 else "D"
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ============ 用户接口 (占位) ============

@app.post("/api/users/register")
async def register_user(user: UserCreate):
    """用户注册 (占位)"""
    return {
        "success": True,
        "message": "用户注册功能开发中",
        "data": {
            "user_id": "user_" + datetime.now().strftime("%Y%m%d%H%M%S")
        }
    }

@app.post("/api/users/login")
async def login_user(user: UserLogin):
    """用户登录 (占位)"""
    return {
        "success": True,
        "message": "用户登录功能开发中",
        "data": {
            "token": "demo_token",
            "expires_in": 3600
        }
    }

# ============ 启动 ============

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
