# 中文说明

<div align="center">

![许可证](https://img.shields.io/badge/License-MIT-blue.svg)
![Python](https://img.shields.io/badge/Python-3.8+-green.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-cyan.svg)

**开源股票分析工具和文档**

</div>

## 📊 项目概述

Stock Analysis SaaS 是一个开源项目，提供股票分析工具、API 和全面的文档。本仓库专注于核心分析功能和文档，便于开发者理解和贡献。

## 🚀 功能特性

- **股票分析 API** - 基于 FastAPI 的 REST API 用于股票数据分析
- **技术指标** - MA、MACD、RSI、布林带等
- **基本面分析** - PE、PB、ROE、分红分析，附带评分系统
- **股票筛选** - 根据多个财务指标筛选股票
- **完整文档** - PRD、部署指南和 API 文档

## 📁 项目结构

```
stock-analysis-saas/
├── core/                    # 核心分析模块
│   ├── stock_analyzer.py   # 股票分析主逻辑
│   ├── technical_indicators.py
│   └── fundamental_analysis.py
├── docs/                    # 文档
│   ├── prd.md              # 产品需求文档
│   ├── DEPLOYMENT.md       # 部署指南
│   └── API.md              # API 文档
├── tests/                   # 单元测试
├── web/                     # Web 界面（如果适用）
├── main.py                  # FastAPI 应用入口
├── requirements.txt         # Python 依赖
└── README.md               # 本文件
```

## 🛠️ 安装

```bash
# 克隆仓库
git clone https://github.com/openclaw/stock-analysis-saas.git
cd stock-analysis-saas

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Windows 系统使用: venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 运行应用
python main.py
```

## 📖 文档

- [产品需求文档 (PRD)](./docs/prd.md)
- [部署指南](./docs/DEPLOYMENT.md)
文档](https://github.com/openclaw/stock-analysis-sa- [API as/wiki/API-Documentation)
- [贡献指南](./CONTRIBUTING.md)

## 🎯 快速开始

### 启动 API 服务器

```bash
python main.py
```

API 将在 `http://localhost:8000` 可访问

### API 端点

- `GET /` - API 根信息
- `GET /api/health` - 健康检查
- `GET /api/stocks` - 获取股票列表
- `POST /api/stocks/filter` - 根据条件筛选股票
- `POST /api/stocks/analyze` - 分析特定股票
- `POST /api/stocks/technical` - 获取技术分析
- `POST /api/stocks/score` - 计算股票评分

### 示例请求

```bash
curl -X POST "http://localhost:8000/api/stocks/filter" \
  -H "Content-Type: application/json" \
  -d '{
    "pe_max": 30,
    "pb_max": 5,
    "roe_min": 10,
    "dividend_min": 1,
    "turnover_rate_min": 0.5,
    "turnover_rate_max": 10
  }'
```

## 📊 技术栈

- **框架**: FastAPI 0.104+
- **语言**: Python 3.8+
- **数据处理**: Pandas, NumPy
- **股票数据**: Baostock
- **数据验证**: Pydantic 2.5+
- **服务器**: Uvicorn

## 🤝 贡献

欢迎贡献！请阅读我们的 [贡献指南](./CONTRIBUTING.md) 了解代码行为准则和提交 Pull Request 的流程。

### 如何贡献

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m '添加某个很棒的功能'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开一个 Pull Request

## 📜 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 🐛 问题反馈

如果您发现 bug 或有功能请求，请在 GitHub 上 [打开 issue](https://github.com/openclaw/stock-analysis-saas/issues)。

## 📧 联系方式

- **组织**: OpenClaw
- **项目**: [https://github.com/openclaw/stock-analysis-saas](https://github.com/openclaw/stock-analysis-saas)

---

<div align="center">

**由 OpenClaw 团队用 ❤️ 构建**

</div>
