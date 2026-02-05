/**
 * StockAI - 股票分析SaaS前端逻辑
 */

// DOM加载完成后初始化
document.addEventListener('DOMContentLoaded', function() {
    initApp();
});

/**
 * 应用初始化
 */
function initApp() {
    initTheme();
    initMobileMenu();
    initCharts();
    initTabs();
    initSearch();
    initWatchlist();
}

/**
 * 主题切换
 */
function initTheme() {
    const themeToggle = document.getElementById('themeToggle');
    const themeIcon = themeToggle ? themeToggle.querySelector('i') : null;
    
    if (!themeToggle || !themeIcon) return;
    
    // 检查本地存储的主题设置
    const savedTheme = localStorage.getItem('theme') || 'light';
    document.documentElement.setAttribute('data-theme', savedTheme);
    updateThemeIcon(savedTheme, themeIcon);
    
    themeToggle.addEventListener('click', function() {
        const currentTheme = document.documentElement.getAttribute('data-theme');
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
        
        document.documentElement.setAttribute('data-theme', newTheme);
        localStorage.setItem('theme', newTheme);
        updateThemeIcon(newTheme, themeIcon);
    });
}

function updateThemeIcon(theme, icon) {
    if (theme === 'dark') {
        icon.className = 'fas fa-sun';
    } else {
        icon.className = 'fas fa-moon';
    }
}

/**
 * 移动端菜单
 */
function initMobileMenu() {
    const menuBtn = document.querySelector('.mobile-menu-btn');
    const navLinks = document.querySelector('.nav-links');
    const sidebarToggle = document.querySelector('.sidebar-toggle');
    const sidebar = document.querySelector('.sidebar');
    
    if (menuBtn && navLinks) {
        menuBtn.addEventListener('click', function() {
            navLinks.classList.toggle('active');
        });
    }
    
    if (sidebarToggle && sidebar) {
        sidebarToggle.addEventListener('click', function() {
            sidebar.classList.toggle('active');
        });
    }
}

/**
 * 初始化图表
 */
function initCharts() {
    // 如果在首页，初始化Hero图表
    if (document.getElementById('heroChart')) {
        initHeroChart();
    }
    
    // 如果在仪表盘，初始化仪表盘图表
    if (document.getElementById('portfolioChart')) {
        initDashboardCharts();
    }
}

/**
 * 首页Hero图表
 */
function initHeroChart() {
    const ctx = document.getElementById('heroChart');
    if (!ctx) return;
    
    const gradient = ctx.getContext('2d').createLinearGradient(0, 0, 0, 300);
    gradient.addColorStop(0, 'rgba(79, 70, 229, 0.3)');
    gradient.addColorStop(1, 'rgba(79, 70, 229, 0)');
    
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: ['1月', '2月', '3月', '4月', '5月', '6月'],
            datasets: [{
                label: '收益率',
                data: [0, 5, 8, 12, 10, 18],
                borderColor: '#4F46E5',
                backgroundColor: gradient,
                borderWidth: 3,
                fill: true,
                tension: 0.4,
                pointRadius: 4,
                pointBackgroundColor: '#4F46E5'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                x: {
                    grid: {
                        display: false
                    }
                },
                y: {
                    beginAtZero: true,
                    grid: {
                        color: 'rgba(0, 0, 0, 0.05)'
                    },
                    ticks: {
                        callback: function(value) {
                            return value + '%';
                        }
                    }
                }
            },
            interaction: {
                intersect: false,
                mode: 'index'
            }
        }
    });
}

/**
 * 仪表盘图表
 */
function initDashboardCharts() {
    // 市场指数迷你图表
    initMiniChart('shChart', [100, 102, 105, 103, 108, 110], '#10B981');
    initMiniChart('szChart', [100, 98, 97, 99, 101, 100], '#EF4444');
    initMiniChart('cyChart', [100, 103, 106, 104, 108, 112], '#10B981');
    
    // 持仓收益图表
    initPortfolioChart();
}

/**
 * 迷你图表
 */
function initMiniChart(canvasId, data, color) {
    const ctx = document.getElementById(canvasId);
    if (!ctx) return;
    
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: ['', '', '', '', '', ''],
            datasets: [{
                data: data,
                borderColor: color,
                borderWidth: 2,
                fill: false,
                tension: 0.4,
                pointRadius: 0
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    enabled: false
                }
            },
            scales: {
                x: {
                    display: false
                },
                y: {
                    display: false
                }
            }
        }
    });
}

/**
 * 持仓收益图表
 */
function initPortfolioChart() {
    const ctx = document.getElementById('portfolioChart');
    if (!ctx) return;
    
    const gradient = ctx.getContext('2d').createLinearGradient(0, 0, 0, 300);
    gradient.addColorStop(0, 'rgba(79, 70, 229, 0.3)');
    gradient.addColorStop(1, 'rgba(79, 70, 229, 0)');
    
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: ['9:30', '10:00', '10:30', '11:00', '11:30', '13:00', '13:30', '14:00', '14:30', '15:00'],
            datasets: [{
                label: '收益',
                data: [0, 0.5, 1.2, 0.8, 1.5, 2.0, 1.8, 2.5, 2.2, 3.0],
                borderColor: '#4F46E5',
                backgroundColor: gradient,
                borderWidth: 2,
                fill: true,
                tension: 0.4,
                pointRadius: 3,
                pointBackgroundColor: '#4F46E5'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                x: {
                    grid: {
                        color: 'rgba(0, 0, 0, 0.05)'
                    }
                },
                y: {
                    grid: {
                        color: 'rgba(0, 0, 0, 0.05)'
                    },
                    ticks: {
                        callback: function(value) {
                            return value + '%';
                        }
                    }
                }
            }
        }
    });
    
    // 周期按钮事件
    const periodBtns = document.querySelectorAll('.period-btn');
    periodBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            periodBtns.forEach(b => b.classList.remove('active'));
            this.classList.add('active');
            updateChartPeriod(this.textContent);
        });
    });
}

/**
 * 更新图表周期
 */
function updateChartPeriod(period) {
    // 模拟更新图表数据
    console.log('切换到' + period + '周期');
    showToast('已切换到' + period + '周期视图', 'success');
}

/**
 * 初始化标签页
 */
function initTabs() {
    const tabs = document.querySelectorAll('.tab');
    
    tabs.forEach(tab => {
        tab.addEventListener('click', function() {
            const tabGroup = this.closest('.tabs');
            const cardBody = this.closest('.card-body');
            if (!cardBody) return;
            
            const tabContents = cardBody.querySelectorAll('.tab-content');
            
            // 移除所有active状态
            tabGroup.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
            tabContents.forEach(content => content.classList.remove('active'));
            
            // 添加active状态
            this.classList.add('active');
            const targetId = this.getAttribute('data-tab');
            const targetContent = document.getElementById(targetId);
            if (targetContent) {
                targetContent.classList.add('active');
            }
        });
    });
}

/**
 * 初始化搜索功能
 */
function initSearch() {
    const searchInput = document.getElementById('stockSearchInput');
    
    if (searchInput) {
        searchInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                searchStock();
            }
        });
    }
    
    // 搜索框回车事件
    const headerSearch = document.getElementById('stockSearch');
    if (headerSearch) {
        headerSearch.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                searchStock(this.value);
            }
        });
    }
}

/**
 * 搜索股票
 */
function searchStock(query) {
    query = query || document.getElementById('stockSearchInput').value;
    
    if (!query.trim()) {
        showToast('请输入股票代码或名称', 'warning');
        return;
    }
    
    // 模拟搜索
    showToast('正在搜索: ' + query, 'success');
    console.log('搜索股票:', query);
}

/**
 * 初始化自选股
 */
function initWatchlist() {
    // 删除自选股事件
    const removeBtns = document.querySelectorAll('.icon-btn-sm.remove');
    removeBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            const row = this.closest('tr');
            const stockName = row.querySelector('.stock-name').textContent;
            row.remove();
            showToast('已从自选股移除: ' + stockName, 'success');
        });
    });
}

/**
 * 添加到自选股
 */
function addToWatchlist() {
    showToast('请选择要添加的股票', 'info');
}

/**
 * 显示提示消息
 */
function showToast(message, type = 'info') {
    const existingToast = document.querySelector('.toast');
    if (existingToast) {
        existingToast.remove();
    }
    
    const toast = document.createElement('div');
    toast.className = 'toast ' + type;
    
    let icon = 'info-circle';
    if (type === 'success') icon = 'check-circle';
    if (type === 'error') icon = 'times-circle';
    if (type === 'warning') icon = 'exclamation-triangle';
    
    toast.innerHTML = '<i class="fas fa-' + icon + '"></i><span>' + message + '</span>';
    document.body.appendChild(toast);
    
    setTimeout(function() {
        toast.style.animation = 'slideOut 0.3s ease forwards';
        setTimeout(function() { toast.remove(); }, 300);
    }, 3000);
}

/**
 * 格式化数字
 */
function formatNumber(num, decimals) {
    decimals = decimals || 2;
    return Number(num).toFixed(decimals);
}

/**
 * 格式化百分比
 */
function formatPercent(num) {
    return (num >= 0 ? '+' : '') + num.toFixed(2) + '%';
}

/**
 * 格式化金额
 */
function formatCurrency(num) {
    return '¥' + num.toLocaleString('zh-CN', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
}

/**
 * 模拟数据 - 排行榜数据
 */
const mockRankings = {
    gainers: [
        { rank: 1, name: '宁德时代', code: '300750', price: 245.67, change: 8.23 },
        { rank: 2, name: '比亚迪', code: '002594', price: 312.45, change: 6.78 },
        { rank: 3, name: '隆基绿能', code: '601012', price: 45.23, change: 5.67 },
        { rank: 4, name: '药明康德', code: '603259', price: 89.34, change: 4.56 },
        { rank: 5, name: '五粮液', code: '000858', price: 156.78, change: 3.89 }
    ],
    losers: [
        { rank: 1, name: '中国平安', code: '601318', price: 45.23, change: -5.67 },
        { rank: 2, name: '招商银行', code: '600036', price: 34.56, change: -4.23 },
        { rank: 3, name: '中信证券', code: '600030', price: 23.45, change: -3.89 },
        { rank: 4, name: '海通证券', code: '600837', price: 12.34, change: -3.21 },
        { rank: 5, name: '国泰君安', code: '601211', price: 15.67, change: -2.78 }
    ],
    volume: [
        { rank: 1, name: '贵州茅台', code: '600519', price: 1789.90, volume: '25.6亿' },
        { rank: 2, name: '五粮液', code: '000858', price: 156.78, volume: '18.2亿' },
        { rank: 3, name: '宁德时代', code: '300750', price: 245.67, volume: '15.8亿' },
        { rank: 4, name: '比亚迪', code: '002594', price: 312.45, volume: '12.3亿' },
        { rank: 5, name: '中信证券', code: '600030', price: 23.45, volume: '10.5亿' }
    ]
};

/**
 * 更新排行榜
 */
function updateRankings(type) {
    const tbody = document.getElementById(type + 'List');
    if (!tbody) return;
    
    const data = mockRankings[type];
    if (!data) return;
    
    tbody.innerHTML = data.map(function(item) {
        const changeClass = item.change >= 0 ? 'positive' : 'negative';
        const changeSymbol = item.change >= 0 ? '+' : '';
        return '<tr>' +
            '<td>' + item.rank + '</td>' +
            '<td><span class="stock-name">' + item.name + '</span> <span class="stock-code">' + item.code + '</span></td>' +
            '<td>¥' + item.price.toFixed(2) + '</td>' +
            '<td class="' + changeClass + '">' + changeSymbol + item.change.toFixed(2) + '%</td>' +
            '</tr>';
    }).join('');
}

/**
 * 获取股票实时数据（模拟API）
 */
async function getStockRealTime(code) {
    // 模拟API调用
    return {
        code: code,
        name: '示例股票',
        price: (Math.random() * 100 + 50).toFixed(2),
        change: (Math.random() * 10 - 5).toFixed(2),
        volume: (Math.random() * 10000000).toLocaleString(),
        amount: (Math.random() * 1000000000).toLocaleString(),
        high: (Math.random() * 100 + 100).toFixed(2),
        low: (Math.random() * 50 + 50).toFixed(2),
        open: (Math.random() * 80 + 60).toFixed(2),
        preClose: (Math.random() * 80 + 60).toFixed(2)
    };
}

/**
 * 导出功能
 */
function exportData(data, filename) {
    const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename + '.json';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    showToast('数据已导出', 'success');
}

// 添加slideOut动画样式
var style = document.createElement('style');
style.textContent = '@keyframes slideOut { from { transform: translateX(0); opacity: 1; } to { transform: translateX(100%); opacity: 0; } }';
document.head.appendChild(style);
