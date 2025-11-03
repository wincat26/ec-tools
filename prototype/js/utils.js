/**
 * AI 營運顧問系統 — 工具函數
 */

// 格式化數字（加入千分位）
function formatNumber(num) {
  return new Intl.NumberFormat('zh-TW').format(num);
}

// 格式化金額（新台幣）
function formatCurrency(amount) {
  return `NT$${formatNumber(amount)}`;
}

// 格式化百分比
function formatPercent(value, decimals = 1) {
  const sign = value >= 0 ? '+' : '';
  return `${sign}${value.toFixed(decimals)}%`;
}

// 獲取變化趨勢圖標
function getTrendIcon(trend) {
  const icons = {
    up: '↑',
    down: '↓',
    stable: '→'
  };
  return icons[trend] || '→';
}

// 獲取變化顏色類別
function getChangeColorClass(change) {
  if (change > 0) return 'text-green-600';
  if (change < 0) return 'text-red-600';
  return 'text-gray-600';
}

// 獲取狀態顏色類別
function getStatusColorClass(status) {
  const colors = {
    '未開始': 'bg-gray-100 text-gray-700',
    '進行中': 'bg-yellow-100 text-yellow-700',
    '已完成': 'bg-green-100 text-green-700',
    '延期': 'bg-red-100 text-red-700'
  };
  return colors[status] || 'bg-gray-100 text-gray-700';
}

// 獲取優先級顏色類別
function getPriorityColorClass(priority) {
  const colors = {
    'high': 'bg-red-100 text-red-700',
    'medium': 'bg-yellow-100 text-yellow-700',
    'low': 'bg-blue-100 text-blue-700'
  };
  return colors[priority] || 'bg-gray-100 text-gray-700';
}

// 格式化日期
function formatDate(dateString) {
  const date = new Date(dateString);
  return date.toLocaleDateString('zh-TW', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit'
  });
}

// 計算日期差異（天數）
function getDaysDifference(dateString) {
  const date = new Date(dateString);
  const today = new Date();
  const diffTime = date - today;
  const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
  return diffDays;
}

// 判斷任務是否逾期
function isTaskOverdue(dueDate, status) {
  if (status === '已完成') return false;
  return getDaysDifference(dueDate) < 0;
}

// 格式化任務截止日狀態
function formatTaskDueStatus(dueDate, status) {
  if (status === '已完成') return '已完成';
  
  const days = getDaysDifference(dueDate);
  if (days < 0) return `逾期 ${Math.abs(days)} 天`;
  if (days === 0) return '今日到期';
  if (days === 1) return '明日到期';
  return `還剩 ${days} 天`;
}

// 計算轉換漏斗掉落率
function calculateDropRate(current, previous) {
  if (previous === 0) return 0;
  return ((previous - current) / previous * 100).toFixed(1);
}

// 生成唯一 ID
function generateId(prefix = '') {
  return `${prefix}${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
}

// 防抖函數
function debounce(func, wait) {
  let timeout;
  return function executedFunction(...args) {
    const later = () => {
      clearTimeout(timeout);
      func(...args);
    };
    clearTimeout(timeout);
    timeout = setTimeout(later, wait);
  };
}

// 節流函數
function throttle(func, limit) {
  let inThrottle;
  return function(...args) {
    if (!inThrottle) {
      func.apply(this, args);
      inThrottle = true;
      setTimeout(() => inThrottle = false, limit);
    }
  };
}

// 複製到剪貼板
async function copyToClipboard(text) {
  try {
    await navigator.clipboard.writeText(text);
    return true;
  } catch (err) {
    console.error('複製失敗:', err);
    return false;
  }
}

// 顯示通知訊息
function showNotification(message, type = 'info') {
  // 創建通知元素
  const notification = document.createElement('div');
  notification.className = `fixed top-4 right-4 p-4 rounded-lg shadow-lg z-50 ${
    type === 'success' ? 'bg-green-500 text-white' :
    type === 'error' ? 'bg-red-500 text-white' :
    'bg-blue-500 text-white'
  }`;
  notification.textContent = message;
  
  document.body.appendChild(notification);
  
  // 3 秒後自動移除
  setTimeout(() => {
    notification.remove();
  }, 3000);
}

// 匯出所有函數
if (typeof window !== 'undefined') {
  window.utils = {
    formatNumber,
    formatCurrency,
    formatPercent,
    getTrendIcon,
    getChangeColorClass,
    getStatusColorClass,
    getPriorityColorClass,
    formatDate,
    getDaysDifference,
    isTaskOverdue,
    formatTaskDueStatus,
    calculateDropRate,
    generateId,
    debounce,
    throttle,
    copyToClipboard,
    showNotification
  };
}

