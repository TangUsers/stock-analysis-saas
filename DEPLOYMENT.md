# 🚀 StockVision Pro 部署方案

**创建时间**: 2026-02-05  
**目标**: 将StockVision Pro V1.0部署上线

---

## 📊 当前状态

### 已完成部分
```
✅ 前端: HTML/CSS/JS (4个文件)
✅ 后端: Python模块 (2200+行代码)
✅ 文档: PRD、运营、营销文档
```

### 待部署部分
```
❌ API服务 (Python Web服务)
❌ 数据存储 (用户数据、自选股)
❌ 前端托管 (可访问的URL)
❌ 域名绑定
```

---

## 🎯 部署目标

| 目标 | 说明 |
|------|------|
| **可访问** | 用户可通过URL访问 |
| **数据持久化** | 用户数据、自选股保存 |
| **API可用** | 后端接口正常调用 |
| **免费/低成本** | 月费用 < ¥100 |

---

## 💰 成本对比方案

### 方案1：纯静态演示版 (最快)

| 项目 | 方案 | 费用 |
|------|------|------|
| 前端托管 | Vercel / Netlify / GitHub Pages | 免费 |
| 后端 | 暂不支持 (纯静态演示) | - |
| 域名 | 无 (使用免费子域名) | ¥0 |

**特点**：
- ✅ 5分钟可上线
- ✅ 完全免费
- ❌ 无后端功能
- ❌ 纯演示用途

**适用**：演示、演示PPT、截图分享

---

### 方案2：最小可用版 (推荐)

| 项目 | 方案 | 费用 |
|------|------|------|
| 前端托管 | Vercel | 免费 |
| 后端API | Railway / Render | 免费 |
| 数据存储 | Railway PostgreSQL | 免费 |
| 域名 | stockvision.ai | ¥50/年 |

**特点**：
- ✅ 完整功能可用
- ✅ 免费额度足够小团队
- ✅ 1-2天可完成
- ⚠️ 需要一些技术配置

**预估月费用**: ¥0-50

---

### 方案3：生产级部署

| 项目 | 方案 | 费用 |
|------|------|------|
| 前端托管 | Vercel Pro | ¥200/月 |
| 后端API | Railway Pro | ¥500/月 |
| 数据存储 | Railway Pro | ¥200/月 |
| CDN | Cloudflare | 免费 |
| 域名 | stockvision.ai | ¥50/年 |

**特点**：
- ✅ 高性能、高可用
- ✅ 完整生产环境
- ❌ 费用较高
- ❌ 需要DevOps经验

**预估月费用**: ¥1,000+

---

## 🎯 推荐方案：方案2 (最小可用版)

### 架构图

```
用户浏览器
    │
    ▼
┌─────────────────┐
│   Vercel        │  ← 免费 CDN + 托管
│   (前端静态资源) │
└────────┬────────┘
         │ HTTPS
         ▼
┌─────────────────┐
│   Railway       │  ← 免费 Python 服务
│   (后端 API)    │
└────────┬────────┘
         │ HTTPS
         ▼
┌─────────────────┐
│   Railway       │  ← 免费 PostgreSQL
│   (数据库)      │
└─────────────────┘
```

---

## 📋 部署步骤

### Step 1: 准备代码仓库

```bash
# 1. 创建 GitHub 仓库
# 访问 https://github.com/new
# 仓库名: stockvision-pro

# 2. 本地初始化
cd products/stock-analysis-saas
git init
git add .
git commit -m "Initial commit: StockVision Pro V1.0"
git remote add origin https://github.com/YOUR_USERNAME/stockvision-pro.git
git push -u origin main
```

### Step 2: 部署后端 (Railway)

1. **注册 Railway**
   - 访问 https://railway.app
   - 用 GitHub 登录

2. **创建项目**
   - 点击 "New Project"
   - 选择 "Deploy from GitHub repo"
   - 选择 stockvision-pro 仓库

3. **配置服务**
   ```
   Root Directory: products/stock-analysis-saas
   Start Command: uvicorn main:app --host 0.0.0.0 --port $PORT
   ```

4. **设置环境变量**
   ```
   DATABASE_URL= (Railway自动创建)
   BAOSTOCK_USERNAME= (可选)
   BAOSTOCK_PASSWORD= (可选)
   ```

### Step 3: 部署前端 (Vercel)

1. **注册 Vercel**
   - 访问 https://vercel.com
   - 用 GitHub 登录

2. **导入项目**
   - 点击 "Add New..."
   - 选择 "Project"
   - 选择 stockvision-pro 仓库

3. **配置**
   ```
   Framework Preset: Other
   Root Directory: products/stock-analysis-saas/web
   Build Command: (留空)
   Output Directory: (留空)
   ```

4. **设置环境变量**
   ```
   API_URL= https://your-api.railway.app
   ```

### Step 4: 绑定域名 (可选)

1. **购买域名**
   - 推荐: Namecheap / 阿里云 / 腾讯云
   - 价格: ¥50-100/年
   - 建议域名: stockvision.ai

2. **配置 DNS**
   ```
   # 在域名服务商后台添加
   A记录: @ -> Vercel IP
   CNAME: www -> cname.vercel-dns.com
   ```

---

## 📁 目录结构要求

当前需要调整的目录结构：

```
stockvision-pro/
├── README.md
├── requirements.txt          # 后端依赖
├── main.py                  # FastAPI 入口
├── products/
│   └── stock-analysis-saas/
│       ├── web/             # Vercel 部署
│       │   ├── index.html
│       │   ├── dashboard.html
│       │   ├── styles.css
│       │   └── app.js
│       └── core/            # Railway 部署
│           ├── stock_analyzer.py
│           ├── technical_indicators.py
│           └── fundamental_analysis.py
└── railway.json            # Railway 配置
```

---

## 🔧 快速部署脚本

创建 `deploy.sh`：

```bash
#!/bin/bash
# StockVision Pro 一键部署脚本

echo "🚀 StockVision Pro 部署脚本"
echo "=============================="

# 1. 检查 Git
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    echo "❌ 请先初始化 Git 仓库"
    exit 1
fi

# 2. 询问部署平台
echo "选择部署方式:"
echo "1) 纯静态演示版 (Vercel, 5分钟)"
echo "2) 完整版 (Vercel + Railway, 1-2天)"
read -p "请选择 (1/2): " choice

case $choice in
    1)
        echo "📦 部署静态演示版..."
        echo "请访问: https://vercel.com/new"
        ;;
    2)
        echo "📦 部署完整版..."
        echo "后端: https://railway.app/new"
        echo "前端: https://vercel.com/new"
        ;;
esac

echo "✅ 部署指南已完成，请参考文档"
```

---

## 💰 成本估算 (方案2)

| 项目 | 方案 | 月费用 | 年费用 |
|------|------|--------|--------|
| 前端托管 | Vercel Free | ¥0 | ¥0 |
| 后端服务 | Railway Free | ¥0 | ¥0 |
| 数据库 | Railway Free | ¥0 | ¥0 |
| 域名 | Namecheap | ¥4 | ¥50 |
| **总计** | | **¥4/月** | **¥50/年** |

---

## ⏱️ 预计时间

| 阶段 | 时间 | 说明 |
|------|------|------|
| 准备代码 | 30分钟 | 整理目录结构 |
| 后端部署 | 2小时 | Railway 配置 |
| 前端部署 | 1小时 | Vercel 配置 |
| 域名绑定 | 24小时 | DNS 生效 |
| **总计** | **1-2天** | 可访问上线 |

---

## 🎯 第一步建议

**先部署静态演示版** (今天完成)：

```bash
# 1. 整理前端文件
cp -r products/stock-analysis-saas/web/* /tmp/stockvision-static/

# 2. 部署到 Vercel
# 访问 https://vercel.com/new
# 上传 web 目录
```

**预计5分钟后得到一个可访问的URL！**

---

**下一步**:
1. 确认部署方案 (1=静态演示 / 2=完整版)
2. 我帮您准备代码结构
3. 开始部署

您想选择哪个方案？