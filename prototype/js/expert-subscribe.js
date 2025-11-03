/**
 * 專家訂閱頁面邏輯
 */

let currentExpertKey = null;
let currentSourceName = null;

// 初始化頁面
function initExpertSubscribePage() {
  // 檢查是否有從 URL 參數傳入的專家資訊
  const urlParams = new URLSearchParams(window.location.search);
  const expertKey = urlParams.get('expert');
  const sourceName = urlParams.get('source');
  
  if (expertKey && sourceName) {
    currentExpertKey = expertKey;
    currentSourceName = sourceName;
  }
  
  loadExperts();
  setupModalHandlers();
}

// 載入所有專家卡片
function loadExperts() {
  const grid = document.getElementById('expertGrid');
  if (!grid) return;
  
  grid.innerHTML = '';
  
  // 取得流量來源與專家的對應關係
  const sourceExpertMap = {
    'search': { source: '搜尋', key: 'search' },
    'ads': { source: '廣告', key: 'ads' },
    'email': { source: 'Email', key: 'email' },
    'ai': { source: 'AI', key: 'ai' },
    'social': { source: '社群', key: 'social' }
  };
  
  Object.entries(mockData.expertSupport).forEach(([key, expert]) => {
    const sourceInfo = sourceExpertMap[key];
    if (!sourceInfo) return;
    
    const card = createExpertCard(key, expert, sourceInfo.source);
    grid.appendChild(card);
  });
}

// 建立專家卡片
function createExpertCard(expertKey, expert, sourceName) {
  const card = document.createElement('div');
  card.className = `expert-card-full ${expert.isSubscribed ? 'expert-subscribed' : ''}`;
  
  card.innerHTML = `
    <div class="expert-tag">${sourceName} 流量專屬</div>
    <div class="expert-card-header">
      <div class="expert-avatar-large">${expert.avatar}</div>
      <div class="expert-info-full">
        <div class="expert-name-large">${expert.name}</div>
        <div class="expert-subtitle-full">${expert.expertName} · ${expert.title}</div>
        <div class="expert-rating-full">
          <span class="rating-stars-large">
            ⭐ ${expert.rating}
          </span>
          <span class="rating-count-full">${expert.subscribers} 位訂閱中</span>
        </div>
      </div>
    </div>
    <div class="expert-description-full">
      ${expert.description}
    </div>
    <div class="expert-features-full">
      <div class="features-title-full">訂閱包含服務</div>
      <ul class="features-list-full">
        ${expert.features.map(feature => `<li>${feature}</li>`).join('')}
      </ul>
    </div>
    <div class="expert-pricing-full">
      <div class="pricing-amount-full">
        <span class="price-value-large">NT$${utils.formatNumber(expert.price)}</span>
        <span class="price-period-full">/${expert.period}</span>
      </div>
      ${expert.isSubscribed ? `
        <button class="btn btn-success btn-sm expert-subscribe-btn-full" disabled>
          ✓ 已訂閱
        </button>
      ` : `
        <button class="btn btn-primary btn-sm expert-subscribe-btn-full" onclick="openSubscribeModal('${expertKey}', '${sourceName}')">
          ＋ 立即訂閱
        </button>
      `}
    </div>
  `;
  
  return card;
}

// 開啟訂閱 Modal
function openSubscribeModal(expertKey, sourceName) {
  const expert = mockData.expertSupport[expertKey];
  if (!expert) return;
  
  currentExpertKey = expertKey;
  currentSourceName = sourceName;
  
  const modal = document.getElementById('subscribeModal');
  const modalBody = document.getElementById('subscribeModalBody');
  
  modalBody.innerHTML = `
    <div class="subscribe-summary">
      <div class="subscribe-summary-item">
        <span class="summary-label">專家服務</span>
        <span class="summary-value">${expert.name}</span>
      </div>
      <div class="subscribe-summary-item">
        <span class="summary-label">專家姓名</span>
        <span class="summary-value">${expert.expertName}</span>
      </div>
      <div class="subscribe-summary-item">
        <span class="summary-label">適用流量來源</span>
        <span class="summary-value">${sourceName}</span>
      </div>
      <div class="subscribe-summary-item">
        <span class="summary-label">訂閱週期</span>
        <span class="summary-value">${expert.period}</span>
      </div>
      <div class="subscribe-total">
        <span class="total-label">訂閱費用</span>
        <span class="total-value">NT$${utils.formatNumber(expert.price)}/${expert.period}</span>
      </div>
    </div>
    <div class="subscribe-note">
      <strong>📋 訂閱說明：</strong><br>
      • 訂閱後將立即開始計算費用<br>
      • 專家將於 ${expert.period} 內提供相關服務與建議<br>
      • 可隨時取消訂閱，已付費用不予退還<br>
      • 訂閱期間內可透過系統與專家進行溝通
    </div>
  `;
  
  modal.style.display = 'flex';
}

// 關閉訂閱 Modal
function closeSubscribeModal() {
  const modal = document.getElementById('subscribeModal');
  modal.style.display = 'none';
  currentExpertKey = null;
  currentSourceName = null;
}

// 確認訂閱
function confirmSubscribe() {
  if (!currentExpertKey) return;
  
  const expert = mockData.expertSupport[currentExpertKey];
  if (!expert) return;
  
  // 更新訂閱狀態
  expert.isSubscribed = true;
  expert.subscribers += 1;
  
  // 關閉 Modal
  closeSubscribeModal();
  
  // 重新載入專家列表
  loadExperts();
  
  // 顯示成功訊息
  if (window.utils) {
    window.utils.showNotification(`成功訂閱「${expert.name}」！專家將開始提供支援服務。`, 'success');
  }
  
  // 3 秒後重新載入頁面以顯示已訂閱狀態
  setTimeout(() => {
    loadExperts();
  }, 500);
}

// 設定 Modal 事件處理
function setupModalHandlers() {
  const modal = document.getElementById('subscribeModal');
  const confirmBtn = document.getElementById('confirmSubscribeBtn');
  
  // 點擊遮罩層關閉
  modal.addEventListener('click', (e) => {
    if (e.target.classList.contains('modal-overlay')) {
      closeSubscribeModal();
    }
  });
  
  // 確認訂閱按鈕
  if (confirmBtn) {
    confirmBtn.addEventListener('click', confirmSubscribe);
  }
}

// 頁面載入完成後初始化
document.addEventListener('DOMContentLoaded', function() {
  initExpertSubscribePage();
});

// 將函數暴露到全域
window.openSubscribeModal = openSubscribeModal;
window.closeSubscribeModal = closeSubscribeModal;
window.confirmSubscribe = confirmSubscribe;
