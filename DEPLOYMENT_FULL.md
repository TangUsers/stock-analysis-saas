# 🚀 StockVision Pro 部署指南 - 完整版

**版本**: V1.0  
**更新时间**: 2026-02-05

---

## 📋 目录

1. [概述](#概述)
2. [准备工作](#准备工作)
3. [步骤1：准备代码](#步骤1准备代码)
4. [步骤2：部署后端](#步骤2部署后端)
5. [步骤3：部署前端](#步骤3部署前端)
6. [步骤4：测试验证](#步骤4测试验证)
7. [常见问题](#常见问题)

---

## 概述

本指南将帮助您将 StockVision Pro V1.0 部署到生产环境。

### 部署架构

```
用户浏览器
    │
    ▼ HTTPS
┌─────────────────┐
│    Vercel       │  ← 免费CDN托管前端
│   (前端静态)    │
└────────┬────────┘
         │ HTTPS API调用
         ▼
┌─────────────────┐
│   Railway       │  ← 免费Python服务
│   (后端API)    │
└────────┬────────┘
         │ HTTPS
         ▼
┌─────────────────┐
│   Railway       │  ← 免费PostgreSQL
│   (数据库)     │
└─────────────────┘
```

### 预估成本

| 项目 | 方案 | 月费用 | 年费用 |
|------|------|--------|--------|
| 前端托管 | Vercel Free | ¥0 | ¥0 |
| 后端服务 | Railway Free | ¥0 | ¥0 |
| 数据库 | Railway Free | ¥0 | ¥0 |
| 域名 | Namecheap | ¥4 | ¥50 |
| **总计** | | **¥4/月** | **¥50/年** |

---

## 准备工作

### 1. 注册账号

| 平台 | 注册地址 | 用途 |
|------|----------|------|
| GitHub | github.com | 代码托管 |
| Railway | railway.app | 后端部署 |
| Vercel | vercel.com | 前端部署 |
| Namecheap | namecheap.com | 域名购买(可选) |

### 2. 准备工具

确保已安装：
```bash
# Git
git --version

# Node.js (用于Vercel CLI，可选)
node --version

# Python 3.8+
python --version
```

### 3. 检查代码

确认以下文件已存在：
```
stock-analysis-saas/
├── main.py                    # ✅ FastAPI入口
├── requirements.txt           # ✅ 依赖配置
├── railway.json             # ✅ Railway配置
├── web/
│   ├── index.html           # ✅ 首页
│   ├── dashboard.html       # ✅ 仪表盘
│   ├── styles.css          # ✅ 样式
│   ├── app.js              # ✅ 交互
│   ├── api_config.js       # ✅ API配置
│   └── vercel.json         # ✅ Vercel配置
└── core/
    ├── stock_analyzer.py    # ✅ 股票分析器
    ├── technical_indicators.py # ✅ 技术指标
    └── fundamental_analysis.py # ✅ 基本面分析
```

---

## 步骤1：准备代码

### 1.1 创建GitHub仓库

1. 打开 https://github.com/new
2. 填写仓库名：`stockvision-pro`
3. 选择 **Public** 或 **Private**
4. 不要勾选 "Add a README file"
5. 点击 "Create repository"

### 1.2 上传代码

```bash
# 打开终端，进入项目目录
cd /Users/tmini2/.openclaw/workspace-agent-company

# 初始化Git
git init

# 添加所有文件
git add .

# 提交代码
git commit -m "StockVision Pro V1.0 - Initial commit"

# 关联远程仓库
git remote add origin https://github.com/YOUR_USERNAME/stockvision-pro.git

# 推送到GitHub
git push -u origin main
```

> **注意**: 将 `YOUR_USERNAME` 替换为您的GitHub用户名

### 1.3 验证上传

访问 https://github.com/YOUR_USERNAME/stockvision-pro
确认所有文件已上传。

---

## 步骤2：部署后端

### 2.1 创建Railway项目

1. 打开 https://railway.app
2. 点击 "New Project"
3. 选择 "Deploy from GitHub repo"
4. 选择 `stockvision-pro` 仓库
5. 点击 "Deploy Now"

### 2.2 配置环境变量

Railway会自动创建PostgreSQL数据库，您需要添加以下环境变量：

1. 在Railway控制台，点击您的项目
2. 进入 "Variables" 标签
3. 添加以下变量：

```
# 可选：Baostock账号 (用于获取股票数据)
# BAOSTOCK_USERNAME=your_email@domain.com
# BAOSTOCK_PASSWORD=your_password

# 时区设置
TZ=Asia/Shanghai
```

### 2.3 等待部署

Railway会自动构建并部署您的后端服务。

**预计时间**: 3-5分钟

### 2.4 获取API地址

部署完成后：
1. 点击 "Settings"
2. 找到 "Domains"
3. 复制您的API地址，例如：
   ```
   https://stockvision-api.up.railway.app
   ```

### 2.5 测试后端

在浏览器中打开：
```
https://stockvision-api.up.railway.app/api/health
```

应该返回：
```json
{
  "status": "healthy",
  "timestamp": "2026-02-05T01:00:00.000000"
}
```

---

## 步骤3：部署前端

### 3.1 创建Vercel项目

1. 打开 https://vercel.com
2. 点击 "Add New..."
3. 选择 "Project"
4. 选择 `stockvision-pro` 仓库
5. 点击 "Import"

### 3.2 配置前端

在Vercel配置页面：

| 配置项 | 值 |
|--------|-----|
| Framework Preset | Other |
| Root Directory | products/stock-analysis-saas/web |
| Build Command | (留空) |
| Output Directory | (留空) |

### 3.3 添加环境变量

1. 找到 "Environment Variables"
2. 添加：

| 变量名 | 值 |
|--------|-----|
| API_URL | `https://stockvision-api.up.railway.app` |

3. 点击 "Deploy"

### 3.4 等待部署

Vercel会自动构建并部署前端。

**预计时间**: 2-3分钟

### 3.5 获取前端地址

部署完成后：
1. 找到 "Domains"
2. 您的网站地址，例如：
   ```
   https://stockvision-pro.vercel.app
   ```

---

## 步骤4：测试验证

### 4.1 测试前端

在浏览器中打开您的前端地址。

应该看到：
- ✅ 首页正常显示
- ✅ 图表加载正常
- ✅ 导航功能可用

### 4.2 测试API连接

打开浏览器控制台 (F12)，执行：

```javascript
// 测试API连接
fetch('https://stockvision-api.up.railway.app/api/health')
  .then(r => r.json())
  .then(console.log)
```

应该返回健康状态。

### 4.3 测试股票搜索

在搜索框中输入股票代码（如 `000001`），应该能返回股票信息。

---

## 常见问题

### Q1: 后端部署失败？

**可能原因**：
1. Python版本不兼容
2. 依赖安装失败

**解决方法**：
1. 检查 `requirements.txt` 语法
2. 查看Railway构建日志
3. 确保使用兼容的Python版本

### Q2: 前端无法连接后端？

**可能原因**：
1. API地址配置错误
2. CORS未配置

**解决方法**：
1. 检查 `api_config.js` 中的 `baseUrl`
2. 确认后端CORS配置正确

### Q3: 股票数据不显示？

**可能原因**：
1. Baostock未配置
2. 数据源不可用

**解决方法**：
1. 检查后端日志
2. 确认Baostock凭证正确
3. 可以使用模拟数据进行测试

### Q4: 如何更新代码？

**步骤**：
```bash
# 本地修改代码
git add .
git commit -m "Update description"
git push

# Railway/Vercel会自动重新部署
```

---

## 🎯 下一步

部署完成后，您可以：

1. **测试所有功能**
2. **分享给种子用户**
3. **收集反馈**
4. **持续优化**

---

## 📞 技术支持

- **文档**: 本部署指南
- **GitHub Issues**: https://github.com/your-username/stockvision-pro/issues
- **邮箱**: beta@stockvision.ai

---

**祝您部署顺利！** 🎉
