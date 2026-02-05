# Stock Analysis SaaS

<div align="center">

![License](https://img.shields.io/badge/License-MIT-blue.svg)
![Python](https://img.shields.io/badge/Python-3.8+-green.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-cyan.svg)

**Open source stock analysis tools and documentation**

[English](./README.md) | [中文](./README_CN.md)

</div>

## 📊 Overview

Stock Analysis SaaS is an open-source project providing stock analysis tools, APIs, and comprehensive documentation. This repository focuses on the core analysis functionality and documentation, making it easy for developers to understand and contribute.

## 🚀 Features

- **Stock Analysis API** - FastAPI-based REST API for stock data analysis
- **Technical Indicators** - MA, MACD, RSI, Bollinger Bands, and more
- **Fundamental Analysis** - PE, PB, ROE, Dividend analysis with scoring system
- **Stock Filtering** - Filter stocks by multiple financial metrics
- **Comprehensive Documentation** - PRD, deployment guides, and API docs

## 📁 Project Structure

```
stock-analysis-saas/
├── core/                    # Core analysis modules
│   ├── stock_analyzer.py   # Main stock analysis logic
│   ├── technical_indicators.py
│   └── fundamental_analysis.py
├── docs/                    # Documentation
│   ├── prd.md              # Product Requirements Document
│   ├── DEPLOYMENT.md       # Deployment guide
│   └── API.md              # API documentation
├── tests/                   # Unit tests
├── web/                     # Web interface (if applicable)
├── main.py                  # FastAPI application entry point
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## 🛠️ Installation

```bash
# Clone the repository
git clone https://github.com/openclaw/stock-analysis-saas.git
cd stock-analysis-saas

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

## 📖 Documentation

- [Product Requirements Document (PRD)](./docs/prd.md)
- [Deployment Guide](./docs/DEPLOYMENT.md)
- [API Documentation](https://github.com/openclaw/stock-analysis-saas/wiki/API-Documentation)
- [Contributing Guide](./CONTRIBUTING.md)

## 🎯 Quick Start

### Start the API Server

```bash
python main.py
```

The API will be available at `http://localhost:8000`

### API Endpoints

- `GET /` - API root information
- `GET /api/health` - Health check
- `GET /api/stocks` - Get stock list
- `POST /api/stocks/filter` - Filter stocks by criteria
- `POST /api/stocks/analyze` - Analyze a specific stock
- `POST /api/stocks/technical` - Get technical analysis
- `POST /api/stocks/score` - Calculate stock score

### Example Request

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

## 📊 Technical Stack

- **Framework**: FastAPI 0.104+
- **Language**: Python 3.8+
- **Data Processing**: Pandas, NumPy
- **Stock Data**: Baostock
- **Validation**: Pydantic 2.5+
- **Server**: Uvicorn

## 🤝 Contributing

Contributions are welcome! Please read our [Contributing Guide](./CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

### How to Contribute

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🐛 Issues

If you find a bug or have a feature request, please [open an issue](https://github.com/openclaw/stock-analysis-saas/issues) on GitHub.

## 📧 Contact

- **Organization**: OpenClaw
- **Project**: [https://github.com/openclaw/stock-analysis-saas](https://github.com/openclaw/stock-analysis-saas)

---

<div align="center">

**Built with ❤️ by OpenClaw Team**

</div>
