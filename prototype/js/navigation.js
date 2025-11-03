/**
 * 導航系統與頁面路由邏輯
 */

// 頁面路由配置
const routeConfig = {
  'dashboard': {
    path: 'dashboard.html',
    title: 'Dashboard - AI 營運顧問系統',
    navId: 'nav-dashboard'
  },
  'data': {
    path: 'data.html',
    title: '數據分析 - AI 營運顧問系統',
    navId: 'nav-data'
  },
  'insights': {
    path: 'insights.html',
    title: '洞察中心 - AI 營運顧問系統',
    navId: 'nav-insights'
  },
  'actions': {
    path: 'actions.html',
    title: '行動方案 - AI 營運顧問系統',
    navId: 'nav-actions'
  },
  'consultants': {
    path: 'consultants.html',
    title: '角色/顧問池 - AI 營運顧問系統',
    navId: 'nav-consultants'
  },
  'reports': {
    path: 'reports.html',
    title: '報告設定 - AI 營運顧問系統',
    navId: 'nav-reports'
  },
  'settings': {
    path: 'settings.html',
    title: '基本設定 - AI 營運顧問系統',
    navId: 'nav-settings'
  }
};

// 取得當前頁面
function getCurrentPage() {
  const path = window.location.pathname;
  const filename = path.split('/').pop() || 'dashboard.html';
  
  for (const [key, config] of Object.entries(routeConfig)) {
    if (config.path === filename) {
      return key;
    }
  }
  
  return 'dashboard'; // 預設為 dashboard
}

// 初始化導航
function initNavigation() {
  const currentPage = getCurrentPage();
  
  // 設定當前頁面的導航項目為 active
  const navLinks = document.querySelectorAll('.nav-link');
  navLinks.forEach(link => {
    link.classList.remove('active');
    if (link.id === routeConfig[currentPage]?.navId) {
      link.classList.add('active');
    }
  });
  
  // 設定頁面標題
  if (routeConfig[currentPage]) {
    document.title = routeConfig[currentPage].title;
  }
}

// 導航到指定頁面
function navigateTo(page, params = {}) {
  if (!routeConfig[page]) {
    console.error(`頁面 ${page} 不存在`);
    return;
  }
  
  const config = routeConfig[page];
  let url = config.path;
  
  // 如果有參數，加入 URL 參數
  if (Object.keys(params).length > 0) {
    const searchParams = new URLSearchParams(params);
    url += `?${searchParams.toString()}`;
  }
  
  window.location.href = url;
}

// 初始化麵包屑
function initBreadcrumb(breadcrumbItems) {
  const breadcrumb = document.getElementById('breadcrumb');
  if (!breadcrumb || !breadcrumbItems) return;
  
  breadcrumb.innerHTML = breadcrumbItems.map((item, index) => {
    const isLast = index === breadcrumbItems.length - 1;
    
    if (isLast) {
      return `<span class="breadcrumb-item"><span class="breadcrumb-current">${item.label}</span></span>`;
    } else {
      return `
        <span class="breadcrumb-item">
          <a href="${item.url || '#'}" class="breadcrumb-link">${item.label}</a>
          <span class="breadcrumb-separator">/</span>
        </span>
      `;
    }
  }).join('');
}

// 頁面載入完成後初始化
document.addEventListener('DOMContentLoaded', function() {
  initNavigation();
  
  // 為所有導航連結綁定點擊事件（如果不在正確頁面）
  const navLinks = document.querySelectorAll('.nav-link[data-page]');
  navLinks.forEach(link => {
    link.addEventListener('click', function(e) {
      const page = this.dataset.page;
      if (page && getCurrentPage() !== page) {
        navigateTo(page);
      }
    });
  });
});

// 暴露到全域
window.navigation = {
  navigateTo,
  getCurrentPage,
  initBreadcrumb
};

