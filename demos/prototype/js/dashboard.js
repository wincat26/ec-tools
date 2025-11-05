/**
 * AI 營運顧問系統 — Dashboard 主要邏輯
 */

// 初始化 Dashboard
function initDashboard() {
  // 載入使用者資訊
  const userEmail = sessionStorage.getItem('userEmail') || 'demo@reddoor.com';
  const emailElement = document.getElementById('userEmailNav');
  if (emailElement) emailElement.textContent = userEmail;
  
  loadSummaryData();
  loadDashboardCards().then(() => {
    setupAiFeedNavigator();
    loadAiActionHighlights();
  });
  setupSummaryControls();
  
  // 設定事件監聽
  setupEventListeners();
  
  // 設定 KPI 點擊事件
  setupKPIClickHandlers();
  
  // 預設顯示總營收分解分析
  setTimeout(() => {
    const revenueCard = document.querySelector('.clickable-kpi[data-kpi="revenue"]');
    if (revenueCard) {
      showKPIDetail('revenue');
    }
  }, 300);
}

// 載入首屏卡片內容
function loadDashboardCards() {
  return Promise.all([
    loadDataCard(),
    loadInsightCard(),
    loadActionCard()
  ]);
}

function setupSummaryControls() {
  const rangeSelect = document.getElementById('summaryRangeSelect');
  const customBtn = document.getElementById('summaryCustomRangeBtn');
  const rangeLabel = document.getElementById('summaryRangeLabel');

  if (rangeSelect) {
    rangeSelect.addEventListener('change', (event) => {
      const value = event.target.value;
      switch (value) {
        case 'yesterday':
          rangeLabel.textContent = '昨天 · 與前一天比較';
          break;
        case '30d':
          rangeLabel.textContent = '最近 30 天 · 與前 30 天比較';
          break;
        case '7d':
          rangeLabel.textContent = '最近 7 天 · 與上週同期比較';
          break;
        case 'custom':
          rangeLabel.textContent = '自訂範圍 · 可選擇最多一年';
          break;
        default:
          rangeLabel.textContent = '最近 7 天 · 與上週同期比較';
      }
    });
  }

  if (customBtn) {
    customBtn.addEventListener('click', () => {
      window.alert('自訂日期功能正在規劃中，正式版將提供日期選擇器。');
    });
  }

  const dataBtn = document.getElementById('summaryToDataBtn');
  if (dataBtn) {
    dataBtn.addEventListener('click', () => {
      window.location.href = 'data.html';
    });
  }

  const insightsBtn = document.getElementById('summaryToInsightsBtn');
  if (insightsBtn) {
    insightsBtn.addEventListener('click', () => {
      window.location.href = 'insights.html';
    });
  }
}

// 設定 AI 資訊流左右滾動控制
function setupAiFeedNavigator() {
  const container = document.getElementById('aiFeedContainer');
  const prevBtn = document.querySelector('.ai-feed-nav--prev');
  const nextBtn = document.querySelector('.ai-feed-nav--next');

  if (!container || !prevBtn || !nextBtn) return;

  const scrollStep = () => Math.max(container.clientWidth * 0.8, 320);

  const updateNavState = () => {
    const scrollable = container.scrollWidth > container.clientWidth + 8;
    if (!scrollable) {
      prevBtn.disabled = true;
      nextBtn.disabled = true;
      return;
    }

    const maxScrollLeft = container.scrollWidth - container.clientWidth - 4;
    prevBtn.disabled = container.scrollLeft <= 4;
    nextBtn.disabled = container.scrollLeft >= maxScrollLeft;
  };

  prevBtn.addEventListener('click', () => {
    container.scrollBy({ left: -scrollStep(), behavior: 'smooth' });
  });

  nextBtn.addEventListener('click', () => {
    container.scrollBy({ left: scrollStep(), behavior: 'smooth' });
  });

  container.addEventListener('scroll', updateNavState, { passive: true });
  window.addEventListener('resize', updateNavState);

  updateNavState();
}

function loadAiActionHighlights() {
  const container = document.getElementById('aiActionList');
  if (!container) return;

  const priorityOrder = { high: 3, medium: 2, low: 1 };
  const actionableTasks = (mockData.tasks || [])
    .filter(task => task.status !== '已完成')
    .sort((a, b) => {
      const priorityDiff = (priorityOrder[b.priority] || 0) - (priorityOrder[a.priority] || 0);
      if (priorityDiff !== 0) return priorityDiff;
      return new Date(a.dueDate) - new Date(b.dueDate);
    })
    .slice(0, 2);

  if (actionableTasks.length === 0) {
    container.innerHTML = `
      <div class="ai-action-empty">
        <p>目前沒有新的高優先行動，建議前往「行動方案」頁面檢視任務進度。</p>
      </div>
    `;
    return;
  }

  container.innerHTML = actionableTasks.map(task => {
    const priorityClass = `ai-action-priority ${task.priority}`;
    const priorityLabel = task.priority === 'high' ? '高' : task.priority === 'medium' ? '中' : '低';
    const dueText = task.dueDate ? `截止：${task.dueDate}` : '無截止日期';
    const sourceGuideline = (mockData.guidelines || []).find(g => g.id === task.sourceGuidelineId);
    const insightText = sourceGuideline ? sourceGuideline.insight : '';

    return `
      <article class="ai-action-item">
        <span class="${priorityClass}">${priorityLabel}</span>
        <div class="ai-action-content">
          <h5>${task.title}</h5>
          <p>${task.description}</p>
          ${insightText ? `<p class="ai-action-meta">洞察來源：${insightText}</p>` : ''}
          <p class="ai-action-meta">${task.category} · ${dueText}</p>
        </div>
      </article>
    `;
  }).join('');
}

// 載入數據分析卡片
function loadDataCard() {
  return new Promise((resolve) => {
    const content = document.getElementById('dataCardContent');
    if (!content) {
      resolve();
      return;
    }
    
    const summary = mockData.summary || {};
    const aov = (mockData.kpiPyramid && mockData.kpiPyramid.aov && mockData.kpiPyramid.aov.value) || 0;
    
    const revenueChange = summary.revenueChange !== undefined ? summary.revenueChange : 0;
    const changeClass = revenueChange >= 0 ? 'success' : 'danger';
    const changeIcon = revenueChange >= 0 ? '↑' : '↓';
    const revenue = summary.revenue || 0;
    const traffic = summary.traffic || 0;
    const conversionRate = summary.conversionRate !== undefined ? summary.conversionRate : 0;
    const orderCount = aov > 0 ? Math.round(revenue / aov) : 0;
    
    content.innerHTML = `
      <div class="card-main-value">
        ${utils.formatCurrency(revenue)}
        <span class="value-change ${changeClass}">
          ${changeIcon} ${Math.abs(revenueChange)}%
        </span>
      </div>
      <div class="card-secondary-info">
        本週總營收 · vs 上週
      </div>
      <div class="data-summary-grid">
        <div class="data-summary-item">
          <div class="data-summary-label">流量</div>
          <div class="data-summary-value">${utils.formatNumber(traffic)}</div>
        </div>
        <div class="data-summary-item">
          <div class="data-summary-label">轉換率</div>
          <div class="data-summary-value">${conversionRate}%</div>
        </div>
        <div class="data-summary-item">
          <div class="data-summary-label">平均訂單</div>
          <div class="data-summary-value">${aov > 0 ? utils.formatCurrency(aov) : '--'}</div>
        </div>
        <div class="data-summary-item">
          <div class="data-summary-label">訂單數</div>
          <div class="data-summary-value">${utils.formatNumber(orderCount)}</div>
        </div>
      </div>
      <div style="flex: 1 1 0; min-height: 0;"></div>
    `;
    resolve();
  });
}

// 載入洞察中心卡片
function loadInsightCard() {
  return new Promise((resolve) => {
    const content = document.getElementById('insightCardContent');
    if (!content) {
      resolve();
      return;
    }
    
    const guidelines = mockData.guidelines || [];
    const displayGuidelines = guidelines.slice(0, 3);
    
    if (guidelines.length === 0) {
      content.innerHTML = `
        <div class="insight-badge">AI 智能分析</div>
        <div class="card-description" style="color: #9ca3af; font-style: italic;">
          暫無資料，請稍候
        </div>
        <div class="card-secondary-info">
          等待 AI 生成分析中...
        </div>
        <div style="flex: 1 1 0; min-height: 0;"></div>
      `;
      resolve();
      return;
    }
    
    content.innerHTML = `
      <div class="insight-badge">AI 智能分析</div>
      <ul class="insight-list">
        ${displayGuidelines.map(guideline => {
          const title = guideline.title || '未命名建議';
          return `
            <li class="insight-list-item">
              <span class="insight-list-text">${title}</span>
            </li>
          `;
        }).join('')}
      </ul>
      <div class="card-secondary-info">
        共有 ${guidelines.length} 項智能建議待查看
      </div>
      <div style="flex: 1 1 0; min-height: 0;"></div>
    `;
    resolve();
  });
}

// 載入行動方案卡片
function loadActionCard() {
  return new Promise((resolve) => {
    const content = document.getElementById('actionCardContent');
    if (!content) {
      resolve();
      return;
    }
    
    const tasks = mockData.tasks || [];
    const completedTasks = tasks.filter(t => t && t.status === '已完成').length;
    const totalTasks = tasks.length;
    const progressPercentage = totalTasks > 0 ? Math.round((completedTasks / totalTasks) * 100) : 0;
    
    const inProgressTasks = tasks.filter(t => t && t.status === '進行中').length;
    const pendingTasks = tasks.filter(t => t && t.status === '未開始').length;
    
    content.innerHTML = `
      <div class="action-progress">
        <div class="progress-header">
          <span class="progress-label">任務完成進度</span>
          <span class="progress-percentage">${progressPercentage}%</span>
        </div>
        <div class="progress-bar-container">
          <div class="progress-bar" style="width: ${progressPercentage}%;"></div>
        </div>
      </div>
      <div class="action-task-count">
        <div class="task-count-item">
          <span class="task-count-number">${totalTasks}</span>
          <span class="task-count-label">總任務</span>
        </div>
        <div class="task-count-item">
          <span class="task-count-number" style="color: #10b981;">${completedTasks}</span>
          <span class="task-count-label">已完成</span>
        </div>
        <div class="task-count-item">
          <span class="task-count-number" style="color: #f59e0b;">${inProgressTasks}</span>
          <span class="task-count-label">進行中</span>
        </div>
        <div class="task-count-item">
          <span class="task-count-number" style="color: #6b7280;">${pendingTasks}</span>
          <span class="task-count-label">待處理</span>
        </div>
      </div>
      <div style="flex: 1 1 0; min-height: 0;"></div>
    `;
    resolve();
  });
}

// 設定 KPI 點擊事件
function setupKPIClickHandlers() {
  const kpiCards = document.querySelectorAll('.clickable-kpi');
  kpiCards.forEach(card => {
    card.addEventListener('click', function() {
      const kpiType = this.dataset.kpi;
      showKPIDetail(kpiType);
    });

    card.addEventListener('keydown', function(event) {
      if (event.key === 'Enter' || event.key === ' ') {
        event.preventDefault();
        const kpiType = this.dataset.kpi;
        showKPIDetail(kpiType);
      }
    });
  });
  
  // 關閉按鈕（預設行為是隱藏，但會在顯示總營收時被覆蓋）
  const closeBtn = document.getElementById('closeKpiDetailBtn');
  if (closeBtn && !closeBtn.onclick) {
    closeBtn.addEventListener('click', () => {
      hideKPIDetail();
    });
  }
}

// 顯示 KPI 詳細資訊
function showKPIDetail(kpiType) {
  const section = document.getElementById('kpiDetailSection');
  const title = document.getElementById('kpiDetailTitle');
  const subtitle = document.getElementById('kpiDetailSubtitle');
  const content = document.getElementById('kpiDetailContent');
  
  if (!section || !title || !content) return;
  
  switch(kpiType) {
    case 'revenue':
      showRevenueDetail(title, subtitle, content);
      break;
    case 'traffic':
      showTrafficDetail(title, subtitle, content);
      break;
    case 'conversion':
      showConversionDetail(title, subtitle, content);
      break;
    case 'aov':
      showAOVDetail(title, subtitle, content);
      break;
  }
  
  section.style.display = 'block';
  section.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

// 隱藏 KPI 詳細資訊
function hideKPIDetail() {
  const section = document.getElementById('kpiDetailSection');
  if (section) {
    section.style.display = 'none';
  }
}

// 顯示總營收詳細分析
function showRevenueDetail(title, subtitle, content) {
  title.textContent = '總營收分解分析';
  subtitle.textContent = '全營收 - 取消退貨金額 = 總營收';
  
  const summary = mockData.summary;
  const grossRevenue = summary.revenue * 1.15; // 假設取消率約15%
  const refundAmount = grossRevenue - summary.revenue;
  const cancellationRate = (refundAmount / grossRevenue * 100).toFixed(2);
  const orderCount = Math.round(summary.revenue / mockData.kpiPyramid.aov.value);
  
  content.innerHTML = `
    <div class="revenue-breakdown">
      <div class="revenue-formula">
        <div class="formula-row">
          <div class="formula-item">
            <div class="formula-label">全營收</div>
            <div class="formula-value">${utils.formatCurrency(grossRevenue)}</div>
          </div>
          <div class="formula-operator">-</div>
          <div class="formula-item">
            <div class="formula-label">取消退貨金額</div>
            <div class="formula-value text-danger">${utils.formatCurrency(refundAmount)}</div>
          </div>
          <div class="formula-operator">=</div>
          <div class="formula-item highlight">
            <div class="formula-label">總營收</div>
            <div class="formula-value">${utils.formatCurrency(summary.revenue)}</div>
          </div>
        </div>
      </div>
      
      <div class="revenue-stats mt-6">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div class="stat-card">
            <div class="stat-label">取消率</div>
            <div class="stat-value">${cancellationRate}%</div>
            <div class="stat-description">取消退貨金額 / 全營收</div>
          </div>
          <div class="stat-card">
            <div class="stat-label">訂單筆數</div>
            <div class="stat-value">${utils.formatNumber(orderCount)}</div>
            <div class="stat-description">總營收 / 平均訂單金額</div>
          </div>
        </div>
      </div>
      
      <div class="revenue-insights mt-6">
        <h4 class="text-lg font-semibold mb-3">💡 觀察與建議</h4>
        <div class="insight-card">
          <p>取消率 ${cancellationRate}% 屬於${cancellationRate > 10 ? '偏高' : '正常'}範圍。建議：</p>
          <ul class="insight-list">
            <li>加強商品描述準確性，降低退貨率</li>
            <li>優化物流時效，減少取消訂單</li>
            <li>建立客戶服務快速響應機制</li>
          </ul>
        </div>
      </div>
    </div>
  `;
  
  // 更新按鈕文字
  const closeBtn = document.getElementById('closeKpiDetailBtn');
  if (closeBtn) {
    closeBtn.textContent = '觀察流量拆解';
    closeBtn.onclick = () => {
      showKPIDetail('traffic');
    };
  }
}

// 顯示流量詳細分析（七大流量策略表）
function showTrafficDetail(title, subtitle, content) {
  title.textContent = '流量詳細分析';
  subtitle.textContent = '各流量來源的會員結構與成效表現';
  
  content.innerHTML = `
    <!-- 觀察視圖切換 -->
    <div class="traffic-view-switcher mb-4">
      <div class="view-tabs">
        <button class="view-tab-btn active" data-view="table">
          <span>📊 流量策略表</span>
        </button>
        <button class="view-tab-btn" data-view="conversion">
          <span>📈 轉換率觀察</span>
        </button>
      </div>
    </div>
    
    <!-- 七大流量策略表 -->
    <div class="traffic-strategy-table" id="trafficTableView">
      <h3 class="text-lg font-semibold mb-4">🌐 七大流量策略表</h3>
      <p class="text-sm text-gray-600 mb-4">分析各流量來源的成效表現與會員結構，點擊任一行可展開詳細分析</p>
      <div class="table-responsive">
        <table class="table traffic-detail-table" id="trafficDetailTable">
          <thead>
            <tr>
              <th style="width: 12%;">流量來源</th>
              <th style="width: 10%;">Sessions</th>
              <th style="width: 8%;">CVR</th>
              <th style="width: 12%;">AOV</th>
              <th style="width: 12%;">營收貢獻</th>
              <th style="width: 46%;">會員結構</th>
              <th style="width: 10%;">趨勢</th>
            </tr>
          </thead>
          <tbody id="trafficDetailTableBody">
            <!-- 由 JavaScript 動態生成 -->
          </tbody>
        </table>
      </div>
    </div>
    
    <!-- 轉換率觀察視圖 -->
    <div class="traffic-conversion-view" id="trafficConversionView" style="display: none;">
      <h3 class="text-lg font-semibold mb-4">📈 轉換率觀察分析</h3>
      <p class="text-sm text-gray-600 mb-4">比較各流量來源的轉換率表現與會員轉換差異</p>
      <div class="conversion-analysis-grid" id="conversionAnalysisGrid">
        <!-- 由 JavaScript 動態生成 -->
      </div>
    </div>
  `;
  
  // 設定視圖切換
  setupTrafficViewSwitching();
  
  // 載入流量資料並綁定點擊事件
  loadTrafficDataForDetail();
  
  // 載入轉換率觀察視圖
  loadConversionAnalysis();
}

// 載入流量詳細表格資料
function loadTrafficDataForDetail() {
  const tbody = document.getElementById('trafficDetailTableBody');
  if (!tbody) return;
  
  tbody.innerHTML = '';
  
  mockData.trafficSources.forEach((source, index) => {
    const memberBreakdown = source.memberBreakdown || {
      newUsers: { registered: 0, purchased: 0, purchaseRate: 0 },
      returningUsers: { visited: 0, purchased: 0, purchaseRate: 0 }
    };
    
    // 計算新客與舊客佔比
    const newUserRatio = source.sessions > 0 ? ((memberBreakdown.newUsers.registered / source.sessions) * 100).toFixed(1) : 0;
    const returningUserRatio = source.sessions > 0 ? ((memberBreakdown.returningUsers.visited / source.sessions) * 100).toFixed(1) : 0;
    
    const tr = document.createElement('tr');
    tr.className = 'traffic-row clickable-row';
    tr.dataset.sourceIndex = index;
    
    tr.innerHTML = `
      <td>
        <span class="expand-icon">▶</span>
        <strong>${source.source}</strong>
      </td>
      <td>${utils.formatNumber(source.sessions)}</td>
      <td>${source.cvr}%</td>
      <td>${utils.formatCurrency(source.aov)}</td>
      <td>${utils.formatCurrency(source.revenue)}</td>
      <td>
        <div class="member-breakdown-inline">
          <div class="member-breakdown-item">
            <div class="breakdown-header">
              <span class="breakdown-icon">🆕</span>
              <span class="breakdown-label">新註冊</span>
            </div>
            <div class="breakdown-main">${utils.formatNumber(memberBreakdown.newUsers.registered)}</div>
            <div class="breakdown-secondary">
              <span class="secondary-text">購買: ${utils.formatNumber(memberBreakdown.newUsers.purchased)}</span>
              <span class="secondary-rate">(${memberBreakdown.newUsers.purchaseRate}%)</span>
            </div>
          </div>
          <div class="member-breakdown-item">
            <div class="breakdown-header">
              <span class="breakdown-icon">👥</span>
              <span class="breakdown-label">舊會員</span>
            </div>
            <div class="breakdown-main">${utils.formatNumber(memberBreakdown.returningUsers.visited)}</div>
            <div class="breakdown-secondary">
              <span class="secondary-text">購買: ${utils.formatNumber(memberBreakdown.returningUsers.purchased)}</span>
              <span class="secondary-rate">(${memberBreakdown.returningUsers.purchaseRate}%)</span>
            </div>
          </div>
          <div class="member-breakdown-summary">
            <div class="summary-item">
              <span>新客 ${newUserRatio}%</span>
            </div>
            <div class="summary-item">
              <span>舊客 ${returningUserRatio}%</span>
            </div>
          </div>
        </div>
      </td>
      <td>
        <span class="badge ${source.trend === 'up' ? 'badge-success' : source.trend === 'down' ? 'badge-danger' : 'badge-secondary'}">
          ${source.trend === 'up' ? '↑' : source.trend === 'down' ? '↓' : '→'} ${Math.abs(source.change)}%
        </span>
      </td>
    `;
    
    tr.style.cursor = 'pointer';
    tr.addEventListener('click', () => {
      toggleSourceDetail(index, source);
    });
    
    tbody.appendChild(tr);
    
    // 展開詳情行（預設隱藏）
    const detailTr = document.createElement('tr');
    detailTr.className = 'traffic-detail-row';
    detailTr.dataset.sourceIndex = index;
    detailTr.style.display = 'none';
    
    // 判斷是否有對應的專家支援
    const expertKey = getExpertKeyForSource(source.source);
    const expert = expertKey ? mockData.expertSupport[expertKey] : null;
    
    detailTr.innerHTML = `
      <td colspan="7">
        <div class="traffic-detail-content">
          <h4>${source.source} 詳細分析</h4>
          <div class="detail-grid">
            <div class="detail-item">
              <div class="detail-label">Sessions</div>
              <div class="detail-value">${utils.formatNumber(source.sessions)}</div>
            </div>
            <div class="detail-item">
              <div class="detail-label">CVR</div>
              <div class="detail-value">${source.cvr}%</div>
            </div>
            <div class="detail-item">
              <div class="detail-label">AOV</div>
              <div class="detail-value">${utils.formatCurrency(source.aov)}</div>
            </div>
            <div class="detail-item">
              <div class="detail-label">營收貢獻</div>
              <div class="detail-value">${utils.formatCurrency(source.revenue)}</div>
            </div>
          </div>
          <div class="traffic-insight">📊 觀察結果: ${getSourceInsight(source)}</div>
          <div class="traffic-recommendation">💡 建議: ${getSourceRecommendation(source)}</div>
          
          ${expert ? `
          <!-- 專家支援區塊（簡化版） -->
          <div class="expert-support-section">
            <div class="expert-support-cta">
              <div class="expert-cta-content">
                <div class="expert-cta-icon">${expert.avatar}</div>
                <div class="expert-cta-info">
                  <div class="expert-cta-title">${expert.name} - ${expert.expertName}</div>
                  <div class="expert-cta-subtitle">${expert.isSubscribed ? '✓ 已訂閱' : `NT$${utils.formatNumber(expert.price)}/${expert.period}`}</div>
                </div>
              </div>
              ${expert.isSubscribed ? `
                <button class="btn btn-success btn-sm" disabled>
                  ✓ 已訂閱
                </button>
              ` : `
                <button class="btn btn-primary btn-sm" onclick="openExpertSubscribePage('${expertKey}', '${source.source}')">
                  👨‍💼 查看專家服務
                </button>
              `}
            </div>
          </div>
          
          <!-- 專家建議區塊（僅在廣告區塊顯示） -->
          ${source.source === '廣告' ? `
          <div class="expert-advice-section">
            <div class="expert-advice-header">
              <div class="expert-advice-title">
                <span>💡</span>
                <span>${expert.name}的建議</span>
              </div>
              ${expert.isSubscribed ? `
                <span class="badge badge-success">已訂閱</span>
              ` : `
                <button class="btn btn-secondary btn-sm" onclick="openExpertSubscribePage('${expertKey}', '${source.source}')">
                  訂閱查看完整建議
                </button>
              `}
            </div>
            ${expert.isSubscribed ? `
              <div class="expert-advice-content">
                ${getExpertAdvice(expertKey, source).map(advice => `
                  <div class="advice-item">
                    <div class="advice-label">${advice.type}</div>
                    <div class="advice-text">${advice.content}</div>
                  </div>
                `).join('')}
              </div>
            ` : `
              <div class="expert-advice-content">
                <div class="advice-item">
                  <div class="advice-label">預覽</div>
                  <div class="advice-text">${getExpertAdvicePreview(expertKey, source)}</div>
                </div>
                <div class="expert-advice-action">
                  <button class="btn btn-primary btn-sm" onclick="openExpertSubscribePage('${expertKey}', '${source.source}')">
                    訂閱解鎖完整建議
                  </button>
                </div>
              </div>
            `}
          </div>
          ` : ''}
          ` : ''}
          
          <div class="traffic-actions">
            <button class="btn btn-primary btn-sm" onclick="addTaskFromTraffic('${source.source}')">
              ＋ 根據此分析建立任務
            </button>
          </div>
        </div>
      </td>
    `;
    
    tbody.appendChild(detailTr);
  });
}

// 切換流量來源詳情
function toggleSourceDetail(index, source) {
  const rows = document.querySelectorAll('#trafficDetailTableBody .traffic-row');
  const detailRows = document.querySelectorAll('#trafficDetailTableBody .traffic-detail-row');
  
  // 關閉其他展開的行
  detailRows.forEach((detailRow, i) => {
    if (i !== index && detailRow.style.display !== 'none') {
      detailRow.style.display = 'none';
      const row = rows[i];
      const icon = row.querySelector('.expand-icon');
      if (icon) icon.textContent = '▶';
      row.classList.remove('expanded');
    }
  });
  
  // 切換當前行
  const currentDetailRow = detailRows[index];
  const currentRow = rows[index];
  const icon = currentRow.querySelector('.expand-icon');
  
  if (currentDetailRow.style.display === 'none') {
    currentDetailRow.style.display = 'table-row';
    if (icon) icon.textContent = '▼';
    currentRow.classList.add('expanded');
  } else {
    currentDetailRow.style.display = 'none';
    if (icon) icon.textContent = '▶';
    currentRow.classList.remove('expanded');
  }
}

// 顯示轉換率詳細分析（轉換漏斗）
function showConversionDetail(title, subtitle, content) {
  title.textContent = '轉換漏斗分析';
  subtitle.textContent = '追蹤使用者從瀏覽到購買的轉換流程';
  
  content.innerHTML = `
    <div class="conversion-funnel" id="conversionFunnelDetail">
      <!-- 由 loadConversionFunnel 動態生成 -->
    </div>
  `;
  
  // 載入轉換漏斗資料
  loadConversionFunnelForDetail();
}

// 載入轉換漏斗（用於詳細視圖）
function loadConversionFunnelForDetail() {
  const container = document.getElementById('conversionFunnelDetail');
  if (!container) return;
  
  const funnel = mockData.conversionFunnel;
  
  container.innerHTML = `
    <div class="funnel-steps">
      ${funnel.steps.map((step, index) => {
        const dropoff = index > 0 ? ((funnel.steps[index-1].count - step.count) / funnel.steps[index-1].count * 100).toFixed(1) : 0;
        const width = (step.count / funnel.steps[0].count * 100).toFixed(1);
        
        return `
          <div class="funnel-step">
            <div class="funnel-step-header">
              <span class="funnel-step-label">${step.label}</span>
              <span class="funnel-step-count">${utils.formatNumber(step.count)}</span>
            </div>
            <div class="funnel-step-bar" style="width: ${width}%; background: ${step.color};">
              <div class="funnel-step-percentage">${width}%</div>
            </div>
            ${index > 0 ? `<div class="funnel-dropoff">流失 ${dropoff}%</div>` : ''}
          </div>
        `;
      }).join('')}
    </div>
    
    <div class="funnel-insights mt-6">
      <h4 class="text-lg font-semibold mb-3">💡 轉換率優化建議</h4>
      <div class="insight-card">
        <p>整體轉換率為 ${funnel.overallRate}%，主要流失階段：</p>
        <ul class="insight-list">
          <li>${funnel.steps[1].label} → ${funnel.steps[2].label} 流失最多，建議優化購物車頁面體驗</li>
          <li>${funnel.steps[0].label} → ${funnel.steps[1].label} 轉換率偏低，建議加強商品吸引力</li>
        </ul>
      </div>
    </div>
  `;
}

// 顯示平均訂單金額詳細分析
function showAOVDetail(title, subtitle, content) {
  title.textContent = '平均訂單金額分解分析';
  subtitle.textContent = '拆解訂單金額構成要素及商品結構分析';
  
  const aov = mockData.kpiPyramid.aov.value;
  const productPrice = aov * 0.65; // 商品本身約65%
  const shipping = aov * 0.10; // 運費約10%
  const upsell = aov * 0.25; // 加購商品約25%
  
  content.innerHTML = `
    <div class="aov-breakdown">
      <div class="aov-formula mb-6">
        <div class="formula-breakdown">
          <div class="breakdown-item">
            <div class="breakdown-label">商品金額</div>
            <div class="breakdown-value">${utils.formatCurrency(productPrice)}</div>
            <div class="breakdown-percentage">65%</div>
          </div>
          <div class="breakdown-item">
            <div class="breakdown-label">加購商品</div>
            <div class="breakdown-value">${utils.formatCurrency(upsell)}</div>
            <div class="breakdown-percentage">25%</div>
          </div>
          <div class="breakdown-item">
            <div class="breakdown-label">運費</div>
            <div class="breakdown-value">${utils.formatCurrency(shipping)}</div>
            <div class="breakdown-percentage">10%</div>
          </div>
          <div class="breakdown-separator"></div>
          <div class="breakdown-item highlight">
            <div class="breakdown-label">平均訂單金額</div>
            <div class="breakdown-value">${utils.formatCurrency(aov)}</div>
          </div>
        </div>
      </div>
      
      <!-- 商品結構分析 -->
      <div class="product-structure-analysis mt-6">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <!-- 熱銷商品 Top 5 -->
          <div class="card">
            <div class="card-header">
              <h2 class="card-title">熱銷商品 Top 5</h2>
            </div>
            <div class="card-body">
              <div id="aovTopProductsList">
                <!-- 由 JavaScript 動態生成 -->
              </div>
            </div>
          </div>
          
          <!-- 單價分佈 -->
          <div class="card">
            <div class="card-header">
              <h2 class="card-title">單價分佈</h2>
            </div>
            <div class="card-body">
              <div id="aovPriceDistribution">
                <!-- 由 JavaScript 動態生成 -->
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <div class="aov-recommendations mt-6">
        <h4 class="text-lg font-semibold mb-3">💡 提升平均訂單金額建議</h4>
        <div class="recommendation-grid">
          <div class="recommendation-card">
            <div class="recommendation-title">🎁 加購策略</div>
            <p>加購商品佔比 25%，可進一步優化：</p>
            <ul class="recommendation-list">
              <li>推薦相關配件與組合商品</li>
              <li>設定滿額免運門檻刺激加購</li>
              <li>推出限時加購優惠</li>
            </ul>
          </div>
          <div class="recommendation-card">
            <div class="recommendation-title">📦 商品組合</div>
            <p>提升商品組合價值：</p>
            <ul class="recommendation-list">
              <li>設計套餐組合方案</li>
              <li>提供批量購買折扣</li>
              <li>推薦高單價商品</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  `;
  
  // 載入商品資料
  loadAOVProductsData();
}

// 設定頁籤切換
function setupTabSwitching() {
  const tabButtons = document.querySelectorAll('.tab-btn');
  const tabContents = document.querySelectorAll('.tab-content');
  
  tabButtons.forEach(button => {
    button.addEventListener('click', () => {
      const targetTab = button.dataset.tab;
      
      // 移除所有active狀態
      tabButtons.forEach(btn => btn.classList.remove('active'));
      tabContents.forEach(content => {
        content.classList.remove('active');
        content.style.display = 'none';
      });
      
      // 啟用當前頁籤
      button.classList.add('active');
      const targetContent = document.getElementById(`${targetTab}Tab`);
      if (targetContent) {
        targetContent.classList.add('active');
        targetContent.style.display = 'block';
      }
    });
  });
}

// 設定流量觀察視圖切換
function setupTrafficViewSwitching() {
  const viewButtons = document.querySelectorAll('.view-tab-btn');
  
  viewButtons.forEach(button => {
    button.addEventListener('click', () => {
      const targetView = button.dataset.view;
      
      // 移除所有active狀態
      viewButtons.forEach(btn => btn.classList.remove('active'));
      
      // 顯示/隱藏對應視圖
      const tableView = document.getElementById('trafficTableView');
      const conversionView = document.getElementById('trafficConversionView');
      
      if (targetView === 'table') {
        button.classList.add('active');
        if (tableView) tableView.style.display = 'block';
        if (conversionView) conversionView.style.display = 'none';
      } else if (targetView === 'conversion') {
        button.classList.add('active');
        if (tableView) tableView.style.display = 'none';
        if (conversionView) conversionView.style.display = 'block';
      }
    });
  });
}

// 載入轉換率觀察視圖
function loadConversionAnalysis() {
  const container = document.getElementById('conversionAnalysisGrid');
  if (!container) return;
  
  container.innerHTML = '';
  
  mockData.trafficSources.forEach(source => {
    const memberBreakdown = source.memberBreakdown || {
      newUsers: { registered: 0, purchased: 0, purchaseRate: 0 },
      returningUsers: { visited: 0, purchased: 0, purchaseRate: 0 }
    };
    
    const conversionCard = document.createElement('div');
    conversionCard.className = 'conversion-analysis-card';
    
    conversionCard.innerHTML = `
      <div class="conversion-card-header">
        <h4 class="conversion-source-name">${source.source}</h4>
        <span class="conversion-overall-cvr">總 CVR: ${source.cvr}%</span>
      </div>
      <div class="conversion-breakdown">
        <div class="conversion-segment new-segment">
          <div class="segment-header">
            <span class="segment-icon">🆕</span>
            <span class="segment-label">新註冊轉換</span>
          </div>
          <div class="segment-value">${memberBreakdown.newUsers.purchaseRate}%</div>
          <div class="segment-detail">
            <span>${utils.formatNumber(memberBreakdown.newUsers.purchased)} / ${utils.formatNumber(memberBreakdown.newUsers.registered)}</span>
          </div>
          <div class="segment-bar">
            <div class="segment-bar-fill" style="width: ${Math.min(memberBreakdown.newUsers.purchaseRate / 3 * 100, 100)}%; background: var(--color-primary);"></div>
          </div>
        </div>
        <div class="conversion-segment returning-segment">
          <div class="segment-header">
            <span class="segment-icon">👥</span>
            <span class="segment-label">舊會員轉換</span>
          </div>
          <div class="segment-value">${memberBreakdown.returningUsers.purchaseRate}%</div>
          <div class="segment-detail">
            <span>${utils.formatNumber(memberBreakdown.returningUsers.purchased)} / ${utils.formatNumber(memberBreakdown.returningUsers.visited)}</span>
          </div>
          <div class="segment-bar">
            <div class="segment-bar-fill" style="width: ${Math.min(memberBreakdown.returningUsers.purchaseRate / 3 * 100, 100)}%; background: var(--color-success);"></div>
          </div>
        </div>
      </div>
      <div class="conversion-insight">
        ${memberBreakdown.newUsers.purchaseRate > memberBreakdown.returningUsers.purchaseRate ? 
          '🟢 新客轉換率優於舊客' : 
          memberBreakdown.newUsers.purchaseRate < memberBreakdown.returningUsers.purchaseRate ?
          '🔵 舊客轉換率優於新客' :
          '⚪ 新舊客轉換率相當'}
      </div>
    `;
    
    container.appendChild(conversionCard);
  });
}

// 載入營運摘要資料
function loadSummaryData() {
  const summary = mockData.summary;
  
  const rangeLabel = document.getElementById('summaryRangeLabel');
  if (rangeLabel) {
    rangeLabel.textContent = `${summary.dateRange} · 與上週 (${summary.previousWeek}) 比較`;
  }

  const revenueElement = document.getElementById('summaryRevenueValue');
  if (revenueElement) {
    revenueElement.textContent = utils.formatCurrency(summary.revenue);
  }

  const revenueChangeElement = document.getElementById('summaryRevenueChange');
  if (revenueChangeElement) {
    const isPositive = summary.revenueChange >= 0;
    revenueChangeElement.textContent = `${isPositive ? '↑' : '↓'} ${Math.abs(summary.revenueChange)}%`;
    revenueChangeElement.classList.toggle('positive', isPositive);
  }

  const trafficElement = document.getElementById('summaryTrafficValue');
  if (trafficElement) {
    trafficElement.textContent = utils.formatNumber(summary.traffic);
  }

  const trafficChangeElement = document.getElementById('summaryTrafficChange');
  if (trafficChangeElement && mockData.kpiPyramid.traffic) {
    const trafficChange = mockData.kpiPyramid.traffic.change;
    trafficChangeElement.textContent = `${trafficChange >= 0 ? '↑' : '↓'} ${Math.abs(trafficChange)}%`;
    trafficChangeElement.classList.toggle('positive', trafficChange >= 0);
  }

  const conversionElement = document.getElementById('summaryConversionValue');
  if (conversionElement) {
    conversionElement.textContent = `${mockData.kpiPyramid.conversion.value}%`;
  }

  const conversionChangeElement = document.getElementById('summaryConversionChange');
  if (conversionChangeElement) {
    const conversionChange = mockData.kpiPyramid.conversion.change;
    conversionChangeElement.textContent = `${conversionChange >= 0 ? '↑' : '↓'} ${Math.abs(conversionChange)}%`;
    conversionChangeElement.classList.toggle('positive', conversionChange >= 0);
  }

  const aovElement = document.getElementById('summaryAovValue');
  if (aovElement) {
    aovElement.textContent = utils.formatCurrency(mockData.kpiPyramid.aov.value);
  }

  const aovChangeElement = document.getElementById('summaryAovChange');
  if (aovChangeElement) {
    const aovChange = mockData.kpiPyramid.aov.change;
    aovChangeElement.textContent = `${aovChange >= 0 ? '↑' : '↓'} ${Math.abs(aovChange)}%`;
    aovChangeElement.classList.toggle('positive', aovChange >= 0);
  }

  const sortedGuidelines = [...mockData.guidelines].sort((a, b) => Math.abs(b.delta) - Math.abs(a.delta));
  const topGuideline = sortedGuidelines[0];
  const nextGuideline = sortedGuidelines[1];

  const alertTitle = document.getElementById('summaryAlertTitle');
  if (alertTitle && topGuideline) {
    alertTitle.textContent = `${topGuideline.source} · ${topGuideline.category} 異常`;
  }

  const alertDescription = document.getElementById('summaryAlertDescription');
  if (alertDescription && topGuideline) {
    alertDescription.textContent = topGuideline.insight;
  }

  const insightList = document.getElementById('summaryInsightList');
  if (insightList) {
    if (topGuideline) {
      const items = [topGuideline, nextGuideline].filter(Boolean).map(g => {
        return `
          <li>
            <strong>${g.category}｜${g.source}</strong>：${g.suggestion}
          </li>
        `;
      }).join('');
      insightList.innerHTML = items;
    } else {
      insightList.innerHTML = '<li>目前沒有偵測到異常指標，營運狀況穩定。</li>';
    }
  }

  const quickInsights = [topGuideline, nextGuideline, sortedGuidelines[2]].filter(Boolean);
  const quickInsightElements = [
    document.getElementById('quickInsightOne'),
    document.getElementById('quickInsightTwo'),
    document.getElementById('quickInsightThree')
  ];

  quickInsightElements.forEach((el, index) => {
    if (!el) return;
    const guideline = quickInsights[index];
    if (guideline) {
      el.textContent = `${guideline.source}：「${guideline.insight}」`;
    } else {
      el.textContent = '等待新的洞察資料...';
    }
  });
}

// 載入流量來源資料（原始版本，保留用於其他地方）
function loadTrafficData() {
  // 這個函數現在主要用於初始化，詳細表格由 loadTrafficDataForDetail 處理
}

// 載入轉換漏斗資料（原始版本）
function loadConversionFunnel() {
  // 這個函數現在主要用於初始化，詳細視圖由 loadConversionFunnelForDetail 處理
}

// 載入商品資料（用於平均訂單金額分析）
function loadAOVProductsData() {
  const products = mockData.products.topProducts;
  
  // Top 5 商品
  const topProductsList = document.getElementById('aovTopProductsList');
  if (topProductsList) {
    topProductsList.innerHTML = products.slice(0, 5).map(product => {
      const unitPrice = product.revenue / product.orders;
      return `
        <div class="product-item">
          <div class="product-info">
            <div class="product-name">${product.name}</div>
            <div class="product-meta">${utils.formatCurrency(unitPrice)} × ${product.orders}件</div>
          </div>
          <div class="product-revenue">${utils.formatCurrency(product.revenue)}</div>
        </div>
      `;
    }).join('');
  }
  
  // 單價分佈
  const priceDistribution = document.getElementById('aovPriceDistribution');
  if (priceDistribution) {
    const distribution = mockData.products.priceDistribution;
    const total = distribution.high.count + distribution.medium.count + distribution.low.count;
    
    priceDistribution.innerHTML = `
      <div class="price-distribution">
        <div class="distribution-item">
          <div class="distribution-header">
            <span class="distribution-label">高單價 (NT$2,000+)</span>
            <span class="distribution-count">${distribution.high.count} 件</span>
          </div>
          <div class="distribution-bar">
            <div class="distribution-fill" style="width: ${distribution.high.share}%; background: var(--color-primary);">
              <span class="distribution-percentage">${distribution.high.share}%</span>
            </div>
          </div>
        </div>
        <div class="distribution-item">
          <div class="distribution-header">
            <span class="distribution-label">中單價 (NT$1,000-2,000)</span>
            <span class="distribution-count">${distribution.medium.count} 件</span>
          </div>
          <div class="distribution-bar">
            <div class="distribution-fill" style="width: ${distribution.medium.share}%; background: var(--color-success);">
              <span class="distribution-percentage">${distribution.medium.share}%</span>
            </div>
          </div>
        </div>
        <div class="distribution-item">
          <div class="distribution-header">
            <span class="distribution-label">低單價 (NT$1,000以下)</span>
            <span class="distribution-count">${distribution.low.count} 件</span>
          </div>
          <div class="distribution-bar">
            <div class="distribution-fill" style="width: ${distribution.low.share}%; background: var(--color-warning);">
              <span class="distribution-percentage">${distribution.low.share}%</span>
            </div>
          </div>
        </div>
      </div>
    `;
  }
}

// 載入 Guideline 建議
function loadGuidelines() {
  const container = document.getElementById('guidelineList');
  if (!container) return;
  
  container.innerHTML = '';
  
  const countElement = document.getElementById('guidelineCount');
  if (countElement) {
    countElement.textContent = mockData.guidelines.length;
  }
  
  mockData.guidelines.forEach(guideline => {
    const card = document.createElement('div');
    card.className = 'guideline-card';
    card.innerHTML = `
      <div class="guideline-header">
        <div>
          <span class="guideline-category">${guideline.category}</span>
          <span class="guideline-source">・ ${guideline.source}</span>
        </div>
        <span class="text-xs text-gray-500">信心度 ${(guideline.confidenceScore * 100).toFixed(0)}%</span>
      </div>
      
      <div class="guideline-insight">
        <div class="guideline-insight-title">🧠 觀察結果</div>
        <div class="guideline-insight-text">${guideline.insight}</div>
      </div>
      
      <div class="guideline-suggestion">
        <div class="guideline-suggestion-title">💡 建議</div>
        <div class="guideline-suggestion-text">${guideline.suggestion}</div>
      </div>
      
      <div class="guideline-actions">
        <div class="guideline-meta">
          ${guideline.metric}: ${guideline.currentValue} (${guideline.delta > 0 ? '+' : ''}${guideline.delta})
        </div>
        <button class="btn-add-task" onclick="addTaskFromGuideline('${guideline.id}')">
          ＋ 加入任務清單
        </button>
      </div>
    `;
    
    container.appendChild(card);
  });
}

// 載入任務清單
function loadTasks() {
  const container = document.getElementById('taskList');
  if (!container) return;
  
  container.innerHTML = '';
  
  const countElement = document.getElementById('taskCount');
  if (countElement) {
    countElement.textContent = mockData.tasks.length;
  }
  
  mockData.tasks.forEach(task => {
    const taskItem = document.createElement('div');
    taskItem.className = 'task-item';
    taskItem.innerHTML = `
      <div class="task-main">
        <div class="task-info">
          <div class="task-title">${task.title}</div>
          <div class="task-meta">
            <span class="task-assignee">${task.assignee}</span>
            <span class="task-due">還剩${task.daysLeft}天</span>
          </div>
        </div>
        <div class="task-actions">
          <button class="task-status ${task.status === '已完成' ? 'status-completed' : task.status === '進行中' ? 'status-in-progress' : 'status-pending'}" 
                  onclick="toggleTaskStatus('${task.id}')">
            ${task.status}
          </button>
          <button class="task-btn" onclick="editTask('${task.id}')">✏️</button>
          <button class="task-btn" onclick="deleteTask('${task.id}')">🗑️</button>
        </div>
      </div>
      ${task.status === '已完成' && task.impactScore ? `
        <div class="task-impact">
          <span>成效影響: <strong>${task.impactScore > 0 ? '+' : ''}${task.impactScore.toFixed(1)}%</strong></span>
        </div>
      ` : ''}
    `;
    
    container.appendChild(taskItem);
  });
}

// 工具函數：取得流量來源洞察
function getSourceInsight(source) {
  if (source.trend === 'down') {
    return `${source.source}流量下降，可能與廣告投放策略調整或競爭對手影響有關。`;
  } else if (source.trend === 'up') {
    return `${source.source}流量表現良好，轉換率${source.cvr}%屬於正常範圍。`;
  }
  return `${source.source}流量穩定，建議持續監控。`;
}

// 工具函數：取得流量來源建議
function getSourceRecommendation(source) {
  if (source.trend === 'down') {
    return `建議調整${source.source}的廣告預算分配，優化受眾設定以提升轉換率。`;
  }
  return `可考慮增加${source.source}的投放預算，擴大流量規模。`;
}

// 取得對應的專家 key
function getExpertKeyForSource(sourceName) {
  const expertMap = {
    '搜尋': 'search',
    '廣告': 'ads',
    'Email': 'email',
    '社群': 'social',
    'AI': 'ai'
  };
  return expertMap[sourceName] || null;
}

// 開啟專家訂閱頁面
function openExpertSubscribePage(expertKey, sourceName) {
  window.location.href = `expert-subscribe.html?expert=${expertKey}&source=${encodeURIComponent(sourceName)}`;
}

// 取得專家建議（僅訂閱用戶可查看完整內容）
function getExpertAdvice(expertKey, source) {
  const expertMap = {
    'ads': [
      {
        type: '預算優化',
        content: `根據您的廣告數據，目前 CVR 為 ${source.cvr}%，建議將 ${source.trend === 'down' ? '部分' : '更多'} 預算分配到轉換率較高的受眾群體，可提升整體 ROAS。`
      },
      {
        type: '素材建議',
        content: `AOV 為 ${utils.formatCurrency(source.aov)}，建議測試更多強調價值感的廣告素材，例如產品組合優惠、限時折扣等，有助於提升訂單金額。`
      },
      {
        type: '受眾設定',
        content: `目前 Sessions 為 ${utils.formatNumber(source.sessions)}，會員結構顯示新客佔比 ${source.memberBreakdown?.newUsers?.registered > 0 ? Math.round((source.memberBreakdown.newUsers.registered / source.sessions) * 100) : 0}%。建議建立相似受眾（Lookalike Audience），針對高價值舊客進行再行銷。`
      },
      {
        type: '出價策略',
        content: `轉換成本相較產業平均 ${source.cvr < 1.2 ? '偏高' : '合理'}，建議調整出價策略，測試「最大化轉換價值」或「目標 ROAS」模式，以優化廣告成本。`
      }
    ]
  };
  
  return expertMap[expertKey] || [];
}

// 取得專家建議預覽（未訂閱用戶）
function getExpertAdvicePreview(expertKey, source) {
  if (expertKey === 'ads') {
    return `根據您的廣告數據，專家可以提供預算優化、素材建議、受眾設定、出價策略等多項專業建議。訂閱後即可查看完整分析內容。`;
  }
  return '訂閱專家服務後，可獲得專業的流量優化建議。';
}

// 從 Guideline 新增任務
function addTaskFromGuideline(guidelineId) {
  const guideline = mockData.guidelines.find(g => g.id === guidelineId);
  if (!guideline) return;
  
  // 開啟任務 Modal 並預填資料
  document.getElementById('modalTitle').textContent = '新增任務';
  document.getElementById('taskTitle').value = guideline.suggestion.split('。')[0];
  document.getElementById('taskDescription').value = guideline.insight;
  document.getElementById('taskForm').dataset.sourceGuideline = guidelineId;
  
  document.getElementById('taskModal').style.display = 'flex';
}

// 從流量分析新增任務
function addTaskFromTraffic(sourceName) {
  document.getElementById('modalTitle').textContent = '新增任務';
  document.getElementById('taskTitle').value = `優化 ${sourceName} 流量策略`;
  document.getElementById('taskDescription').value = `針對 ${sourceName} 流量來源進行策略優化`;
  document.getElementById('taskForm').dataset.sourceTraffic = sourceName;
  
  document.getElementById('taskModal').style.display = 'flex';
}

// 設定事件監聽
function setupEventListeners() {
  // 任務表單提交
  const taskForm = document.getElementById('taskForm');
  if (taskForm) {
    taskForm.addEventListener('submit', function(e) {
      e.preventDefault();
      
      const taskId = 'task_' + Date.now();
      const newTask = {
        id: taskId,
        title: document.getElementById('taskTitle').value,
        description: document.getElementById('taskDescription').value,
        assignee: document.getElementById('taskAssignee').value,
        priority: document.getElementById('taskPriority').value,
        status: '未開始',
        dueDate: document.getElementById('taskDueDate').value,
        daysLeft: Math.ceil((new Date(document.getElementById('taskDueDate').value) - new Date()) / (1000 * 60 * 60 * 24)),
        createdAt: new Date().toISOString(),
        completedAt: null,
        impactScore: null
      };
      
      mockData.tasks.unshift(newTask);
      loadTasks();
      closeTaskModal();
      
      // 給予積分獎勵（如果不在引導中）
      if (window.onboarding && !window.onboarding.isActive) {
        window.onboarding.giveReward({
          points: 20,
          message: '任務建立成功！獲得 +20 積分'
        });
      } else {
        if (window.utils) {
          window.utils.showNotification('任務已建立！', 'success');
        }
      }
    });
  }
  
  // 關閉 Modal
  const closeModalBtn = document.getElementById('closeModalBtn');
  const cancelBtn = document.getElementById('cancelTaskBtn');
  const modal = document.getElementById('taskModal');
  
  if (closeModalBtn) {
    closeModalBtn.addEventListener('click', closeTaskModal);
  }
  if (cancelBtn) {
    cancelBtn.addEventListener('click', closeTaskModal);
  }
  if (modal) {
    modal.addEventListener('click', function(e) {
      if (e.target.classList.contains('modal-overlay') || e.target.classList.contains('modal')) {
        closeTaskModal();
      }
    });
  }
  
  // 新增任務按鈕
  const addTaskBtn = document.getElementById('addTaskBtn');
  if (addTaskBtn) {
    addTaskBtn.addEventListener('click', () => {
      document.getElementById('modalTitle').textContent = '新增任務';
      document.getElementById('taskForm').reset();
      document.getElementById('taskForm').removeAttribute('data-source-guideline');
      document.getElementById('taskForm').removeAttribute('data-source-traffic');
      document.getElementById('taskModal').style.display = 'flex';
    });
  }
}

// 關閉任務 Modal
function closeTaskModal() {
  const modal = document.getElementById('taskModal');
  if (modal) {
    modal.style.display = 'none';
    document.getElementById('taskForm').reset();
  }
}

// 切換任務狀態
function toggleTaskStatus(taskId) {
  const task = mockData.tasks.find(t => t.id === taskId);
  if (!task) return;
  
  const statuses = ['未開始', '進行中', '已完成'];
  const currentIndex = statuses.indexOf(task.status);
  const nextIndex = (currentIndex + 1) % statuses.length;
  
  const previousStatus = task.status;
  task.status = statuses[nextIndex];
  
  if (task.status === '已完成' && !task.completedAt) {
    task.completedAt = new Date().toISOString();
    // 這裡可以計算成效（模擬）
    task.impactScore = Math.random() * 15 - 5; // 模擬 -5% 到 +10%
    
    // 給予積分獎勵
    if (window.onboarding && !window.onboarding.isActive) {
      window.onboarding.giveReward({
        points: 50,
        message: '任務完成！獲得 +50 積分'
      });
    }
  }
  
  loadTasks();
  
  if (window.utils) {
    window.utils.showNotification(`任務狀態已更新為「${task.status}」`, 'success');
  }
}

// 編輯任務
function editTask(taskId) {
  const task = mockData.tasks.find(t => t.id === taskId);
  if (!task) return;
  
  document.getElementById('modalTitle').textContent = '編輯任務';
  document.getElementById('taskTitle').value = task.title;
  document.getElementById('taskDescription').value = task.description || '';
  document.getElementById('taskAssignee').value = task.assignee;
  document.getElementById('taskPriority').value = task.priority || 'medium';
  document.getElementById('taskDueDate').value = task.dueDate;
  document.getElementById('taskForm').dataset.taskId = taskId;
  
  document.getElementById('taskModal').style.display = 'flex';
}

// 刪除任務
function deleteTask(taskId) {
  if (confirm('確定要刪除這個任務嗎？')) {
    mockData.tasks = mockData.tasks.filter(t => t.id !== taskId);
    loadTasks();
    if (window.utils) {
      window.utils.showNotification('任務已刪除', 'success');
    }
  }
}

// 頁面載入完成後初始化
document.addEventListener('DOMContentLoaded', function() {
  initDashboard();
});

// 將函數暴露到全域（供 HTML 直接呼叫）
window.addTaskFromGuideline = addTaskFromGuideline;
window.addTaskFromTraffic = addTaskFromTraffic;
window.editTask = editTask;
window.toggleTaskStatus = toggleTaskStatus;
window.deleteTask = deleteTask;
window.openExpertSubscribePage = openExpertSubscribePage;
