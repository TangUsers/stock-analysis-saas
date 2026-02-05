/**
 * StockVision Pro - API配置
 * 
 * 在此处配置API地址
 * 部署后将your-api.railway.app替换为实际的API地址
 */

const API_CONFIG = {
    // API基础地址
    // 开发环境: http://localhost:8000
    // 生产环境: https://your-api.railway.app
    baseUrl: process.env.API_URL || 'https://your-api.railway.app',
    
    // API版本
    version: 'v1',
    
    // 超时设置 (毫秒)
    timeout: 30000,
    
    // 重试次数
    retry: 3
};

// API端点
const API_ENDPOINTS = {
    health: '/api/health',
    stocks: '/api/stocks',
    stocksFilter: '/api/stocks/filter',
    stocksAnalyze: '/api/stocks/analyze',
    stocksTechnical: '/api/stocks/technical',
    stocksScore: '/api/stocks/score',
    usersRegister: '/api/users/register',
    usersLogin: '/api/users/login'
};

// 导出配置
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { API_CONFIG, API_ENDPOINTS };
}
