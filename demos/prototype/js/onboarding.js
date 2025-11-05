/**
 * AI 營運顧問系統 — 引導流程與遊戲化系統
 */

// 引導步驟定義
const onboardingSteps = [
  {
    id: 'welcome',
    title: '歡迎使用 AI 營運顧問系統',
    description: '讓我們用 3 分鐘帶你了解如何讓數據變成行動',
    target: null,
    position: 'center',
    showModal: true
  },
  {
    id: 'summary',
    title: '營運摘要區',
    description: '這裡可以看到本週總營收、流量、轉換率和客單價。快速掌握整體營運狀況！',
    target: '.summary-section',
    position: 'bottom',
    action: 'explore',
    reward: { points: 10, message: '獲得 +10 積分！' }
  },
  {
    id: 'kpi',
    title: 'KPI 分解流程',
    description: '營收 = 流量 × 轉換率 × 客單價。點擊表格中的任一行可展開查看詳細分析。',
    target: '.kpi-section',
    position: 'bottom',
    action: 'click',
    actionTarget: '.kpi-table-row[data-metric="traffic"]',
    reward: { points: 10, message: '獲得 +10 積分！' }
  },
  {
    id: 'guideline',
    title: 'Guideline 智能建議',
    description: '這是 AI 根據數據異常自動生成的建議。點擊卡片可查看完整的觀察結果和行動建議。',
    target: '.guideline-section',
    position: 'bottom',
    action: 'read',
    reward: { points: 2, message: '獲得 +2 積分！' }
  },
  {
    id: 'create-task',
    title: '將建議轉為任務',
    description: '點擊「＋ 加入任務清單」按鈕，將 AI 建議轉為可追蹤的執行任務。',
    target: '.guideline-card:first-child',
    position: 'right',
    action: 'click',
    actionTarget: '.btn-add-task',
    reward: { points: 20, achievement: 'action_practitioner', message: '獲得 +20 積分 + 「行動實踐者」成就！' }
  },
  {
    id: 'tasks',
    title: '行動任務清單',
    description: '這裡可以追蹤所有任務的執行進度。點擊任務狀態可以更新進度。',
    target: '.tasks-section',
    position: 'bottom',
    action: 'explore',
    reward: { points: 15, message: '獲得 +15 積分！' }
  },
  {
    id: 'complete',
    title: '完成引導！',
    description: '恭喜完成引導！你已獲得 100 積分和「初學者」成就。現在可以完整使用系統了！',
    target: null,
    position: 'center',
    showModal: true,
    reward: { points: 100, achievement: 'beginner', message: '獲得 +100 積分 + 「初學者」成就！' }
  }
];

// 遊戲化系統狀態
const gamificationState = {
  points: 0,
  level: 1,
  achievements: [],
  weeklyGoals: {
    tasksCompleted: 0,
    tasksTarget: 3,
    guidelinesViewed: 0,
    guidelinesTarget: 5
  }
};

// 引導系統類
class OnboardingSystem {
  constructor() {
    this.currentStep = 0;
    this.isActive = false;
    this.isCompleted = this.loadOnboardingStatus();
  }

  // 載入引導狀態
  loadOnboardingStatus() {
    const saved = localStorage.getItem('onboarding_completed');
    return saved === 'true';
  }

  // 儲存引導狀態
  saveOnboardingStatus(completed) {
    localStorage.setItem('onboarding_completed', completed.toString());
  }

  // 開始引導
  start() {
    if (this.isCompleted) {
      return;
    }
    
    this.isActive = true;
    this.currentStep = 0;
    this.showStep(this.currentStep);
  }

  // 重新開始引導（重置狀態）
  restart() {
    // 重置完成狀態
    this.isCompleted = false;
    this.isActive = false;
    this.currentStep = 0;
    
    // 清除 localStorage 中的完成狀態
    localStorage.removeItem('onboarding_completed');
    
    // 移除現有的遮罩層和 Modal
    this.removeOverlay();
    this.removeModal();
    
    // 重新開始
    setTimeout(() => {
      this.start();
    }, 100);
  }

  // 顯示步驟
  showStep(stepIndex) {
    if (stepIndex >= onboardingSteps.length) {
      this.complete();
      return;
    }

    const step = onboardingSteps[stepIndex];
    this.currentStep = stepIndex;

    // 如果是 Modal 步驟
    if (step.showModal) {
      this.showModalStep(step);
      return;
    }

    // 特殊處理：步驟三（guideline）需要確保內容已載入
    if (step.id === 'guideline') {
      this.waitForGuidelinesContent().then(() => {
        this.showOverlay(step);
        this.showStepIndicator();
        if (step.action) {
          this.setupAction(step);
        }
      });
      return;
    }

    // 顯示引導遮罩層
    this.showOverlay(step);
    
    // 顯示步驟指示器
    this.showStepIndicator();
    
    // 執行動作（如果需要）
    if (step.action) {
      this.setupAction(step);
    }
  }

  // 等待 Guideline 內容載入完成
  waitForGuidelinesContent() {
    return new Promise((resolve) => {
      const guidelineList = document.getElementById('guidelineList');
      if (!guidelineList) {
        console.warn('找不到 guidelineList 元素');
        resolve();
        return;
      }

      // 檢查是否已經有內容
      if (guidelineList.children.length > 0) {
        resolve();
        return;
      }

      // 如果沒有內容，等待載入
      let attempts = 0;
      const maxAttempts = 30; // 最多等待 3 秒
      const checkInterval = setInterval(() => {
        attempts++;
        const hasContent = guidelineList && guidelineList.children.length > 0;
        
        if (hasContent) {
          clearInterval(checkInterval);
          // 再等待一小段時間確保渲染完成
          setTimeout(resolve, 200);
        } else if (attempts >= maxAttempts) {
          clearInterval(checkInterval);
          console.warn('等待 Guideline 內容載入超時，但繼續執行引導');
          resolve(); // 即使超時也繼續
        }
      }, 100);
    });
  }

  // 顯示遮罩層與工具提示
  showOverlay(step) {
    // 移除舊的遮罩層
    this.removeOverlay();

    // 創建遮罩層
    const overlay = document.createElement('div');
    overlay.id = 'onboarding-overlay';
    overlay.className = 'onboarding-overlay';
    
    document.body.appendChild(overlay);
    
    // 創建高亮區域
    let targetElement = null;
    let targetRect = null;
    
    if (step.target) {
      targetElement = document.querySelector(step.target);
      if (targetElement) {
        // 確保元素可見（如果是動態生成的內容，可能需要等待）
        this.ensureElementVisible(targetElement).then(() => {
          // 再次確認元素仍然存在
          const currentElement = document.querySelector(step.target);
          if (!currentElement) {
            console.warn(`目標元素在等待過程中消失: ${step.target}`);
            this.createAndPositionTooltip(overlay, step, null);
            return;
          }
          
          // 滾動到目標元素（確保元素在視窗中央）
          currentElement.scrollIntoView({ 
            behavior: 'smooth', 
            block: 'center',
            inline: 'nearest'
          });
          
          // 等待滾動完成後計算位置
          setTimeout(() => {
            // 再次獲取最新的位置
            const finalElement = document.querySelector(step.target);
            if (!finalElement) {
              console.warn(`目標元素在滾動後消失: ${step.target}`);
              this.createAndPositionTooltip(overlay, step, null);
              return;
            }
            
            targetRect = finalElement.getBoundingClientRect();
            
            // 檢查元素是否有有效的尺寸
            if (targetRect.width === 0 || targetRect.height === 0) {
              console.warn(`目標元素尺寸為 0: ${step.target}`, targetRect);
              // 嘗試使用父元素的位置
              const parent = finalElement.parentElement;
              if (parent) {
                const parentRect = parent.getBoundingClientRect();
                if (parentRect.width > 0 && parentRect.height > 0) {
                  targetRect = parentRect;
                } else {
                  // 如果父元素也不行，使用最近的 card 元素
                  const card = finalElement.closest('.card');
                  if (card) {
                    const cardRect = card.getBoundingClientRect();
                    if (cardRect.width > 0 && cardRect.height > 0) {
                      targetRect = cardRect;
                    }
                  }
                }
              }
            }
            
            // 再次確認尺寸有效
            if (targetRect.width === 0 || targetRect.height === 0) {
              console.error(`無法取得有效的目標元素尺寸: ${step.target}`);
              // 使用視窗中心作為備選方案
              targetRect = {
                top: window.scrollY + window.innerHeight / 2 - 100,
                left: window.scrollX + window.innerWidth / 2 - 200,
                width: 400,
                height: 200
              };
            }
            
            // 創建高亮區域
            // getBoundingClientRect() 返回的是相對於視窗的位置，需要加上 scroll 偏移
            const highlight = document.createElement('div');
            highlight.className = 'onboarding-highlight';
            highlight.style.top = `${targetRect.top + window.scrollY}px`;
            highlight.style.left = `${targetRect.left + window.scrollX}px`;
            highlight.style.width = `${Math.max(targetRect.width, 100)}px`;
            highlight.style.height = `${Math.max(targetRect.height, 50)}px`;
            overlay.appendChild(highlight);
            
            // 調試資訊
            if (step.id === 'guideline') {
              console.log('步驟三 - Guideline 高亮區域:', {
                top: highlight.style.top,
                left: highlight.style.left,
                width: highlight.style.width,
                height: highlight.style.height,
                targetRect: targetRect,
                element: finalElement
              });
            }
            
            // 創建並定位工具提示
            this.createAndPositionTooltip(overlay, step, targetRect);
          }, 500); // 增加等待時間以確保滾動完成
        });
      } else {
        // 找不到目標元素，延遲重試
        console.warn(`找不到目標元素: ${step.target}，將重試...`);
        setTimeout(() => {
          const retryElement = document.querySelector(step.target);
          if (retryElement) {
            this.showOverlay(step);
          } else {
            console.error(`重試後仍找不到目標元素: ${step.target}`);
            // 即使找不到目標，也顯示 tooltip
            this.createAndPositionTooltip(overlay, step, null);
          }
        }, 500);
      }
    } else {
      // 沒有目標元素，直接顯示 tooltip 在中間
      this.createAndPositionTooltip(overlay, step, null);
    }
  }

  // 確保元素可見（等待動態內容載入）
  ensureElementVisible(element) {
    return new Promise((resolve) => {
      if (!element) {
        resolve();
        return;
      }
      
      // 如果元素已經有內容且可見
      const hasSize = element.offsetHeight > 0 && element.offsetWidth > 0;
      const hasContent = element.children.length > 0 || element.textContent.trim().length > 0;
      
      if (hasSize && hasContent) {
        resolve();
        return;
      }
      
      // 等待元素可見（最多等待 3 秒）
      let attempts = 0;
      const maxAttempts = 30;
      const checkInterval = setInterval(() => {
        attempts++;
        const currentHasSize = element.offsetHeight > 0 && element.offsetWidth > 0;
        const currentHasContent = element.children.length > 0 || element.textContent.trim().length > 0;
        
        if ((currentHasSize && currentHasContent) || attempts >= maxAttempts) {
          clearInterval(checkInterval);
          resolve();
        }
      }, 100);
    });
  }

  // 創建並定位工具提示
  createAndPositionTooltip(overlay, step, targetRect) {
    const tooltip = document.createElement('div');
    tooltip.className = 'onboarding-tooltip';
    tooltip.innerHTML = `
      <div class="tooltip-header">
        <h4>${step.title}</h4>
        <button class="tooltip-close" onclick="onboarding.skip()">×</button>
      </div>
      <div class="tooltip-body">
        <p>${step.description}</p>
      </div>
      <div class="tooltip-footer">
        <button class="btn btn-secondary btn-sm" onclick="onboarding.prev()">上一步</button>
        <button class="btn btn-primary btn-sm" onclick="onboarding.next()">下一步</button>
      </div>
    `;
    
    // 先加入 DOM 以便計算尺寸
    overlay.appendChild(tooltip);
    
    // 計算最佳位置
    const position = this.calculateTooltipPosition(tooltip, step, targetRect);
    
    // 應用位置
    tooltip.style.top = `${position.top}px`;
    tooltip.style.left = `${position.left}px`;
    tooltip.classList.add(`tooltip-${position.side}`);
  }

  // 計算工具提示的最佳位置
  calculateTooltipPosition(tooltip, step, targetRect) {
    const tooltipRect = tooltip.getBoundingClientRect();
    const viewportWidth = window.innerWidth;
    const viewportHeight = window.innerHeight;
    const padding = 20; // 與邊界的距離
    const gap = 20; // 與目標元素的距離
    const stepIndicatorHeight = 70; // 步驟指示器高度（包含底部間距）
    
    // 如果沒有目標元素，顯示在視窗中間
    if (!targetRect) {
      return {
        top: window.scrollY + (viewportHeight - tooltipRect.height) / 2,
        left: window.scrollX + (viewportWidth - tooltipRect.width) / 2,
        side: 'center'
      };
    }
    
    // 計算各方向的位置
    const positions = {
      top: {
        top: targetRect.top + window.scrollY - tooltipRect.height - gap,
        left: targetRect.left + window.scrollX + (targetRect.width - tooltipRect.width) / 2,
        side: 'bottom'
      },
      bottom: {
        top: targetRect.bottom + window.scrollY + gap,
        left: targetRect.left + window.scrollX + (targetRect.width - tooltipRect.width) / 2,
        side: 'top'
      },
      left: {
        top: targetRect.top + window.scrollY + (targetRect.height - tooltipRect.height) / 2,
        left: targetRect.left + window.scrollX - tooltipRect.width - gap,
        side: 'right'
      },
      right: {
        top: targetRect.top + window.scrollY + (targetRect.height - tooltipRect.height) / 2,
        left: targetRect.right + window.scrollX + gap,
        side: 'left'
      },
      center: {
        top: window.scrollY + (viewportHeight - tooltipRect.height) / 2,
        left: window.scrollX + (viewportWidth - tooltipRect.width) / 2,
        side: 'center'
      }
    };
    
    // 根據 step.position 選擇初始位置
    let preferredPosition = step.position || 'bottom';
    if (preferredPosition === 'center') {
      return positions.center;
    }
    
    let bestPosition = positions[preferredPosition];
    
    // 檢查是否超出視窗邊界，如果超出則調整
    let attempts = 0;
    const maxAttempts = 4;
    const sides = ['bottom', 'top', 'right', 'left'];
    let currentSideIndex = sides.indexOf(preferredPosition);
    
    while (attempts < maxAttempts) {
      const side = sides[currentSideIndex];
      const pos = positions[side];
      
      // 檢查水平邊界
      if (pos.left < padding) {
        pos.left = padding;
      } else if (pos.left + tooltipRect.width > viewportWidth - padding) {
        pos.left = viewportWidth - tooltipRect.width - padding;
      }
      
      // 檢查垂直邊界（考慮步驟指示器）
      if (pos.top < window.scrollY + padding) {
        pos.top = window.scrollY + padding;
      } else if (pos.top + tooltipRect.height > window.scrollY + viewportHeight - stepIndicatorHeight - padding) {
        pos.top = window.scrollY + viewportHeight - tooltipRect.height - stepIndicatorHeight - padding;
      }
      
      // 檢查是否在視窗內（考慮步驟指示器）
      const isInViewport = 
        pos.left >= padding &&
        pos.left + tooltipRect.width <= viewportWidth - padding &&
        pos.top >= window.scrollY + padding &&
        pos.top + tooltipRect.height <= window.scrollY + viewportHeight - stepIndicatorHeight - padding;
      
      if (isInViewport) {
        bestPosition = pos;
        break;
      }
      
      // 嘗試下一個位置
      currentSideIndex = (currentSideIndex + 1) % sides.length;
      attempts++;
    }
    
    // 確保最終位置在視窗內（強制限制，考慮步驟指示器）
    bestPosition.left = Math.max(padding, Math.min(bestPosition.left, viewportWidth - tooltipRect.width - padding));
    bestPosition.top = Math.max(
      window.scrollY + padding, 
      Math.min(bestPosition.top, window.scrollY + viewportHeight - tooltipRect.height - stepIndicatorHeight - padding)
    );
    
    return bestPosition;
  }

  // 顯示步驟指示器
  showStepIndicator() {
    // 添加 class 標記引導進行中
    document.body.classList.add('onboarding-active');
    
    let indicator = document.getElementById('onboarding-step-indicator');
    if (!indicator) {
      indicator = document.createElement('div');
      indicator.id = 'onboarding-step-indicator';
      indicator.className = 'onboarding-step-indicator';
      document.body.appendChild(indicator);
    }

    const steps = onboardingSteps.filter(s => !s.showModal);
    indicator.innerHTML = steps.map((step, index) => {
      const stepNum = index + 1;
      const isActive = stepNum === this.currentStep + (onboardingSteps[0].showModal ? 0 : 1);
      const isCompleted = stepNum < this.currentStep + (onboardingSteps[0].showModal ? 0 : 1);
      
      return `
        <span class="step-dot ${isActive ? 'active' : ''} ${isCompleted ? 'completed' : ''}">
          ${isCompleted ? '✓' : stepNum}
        </span>
      `;
    }).join('') + `<span class="step-text">步驟 ${this.currentStep + 1} / ${onboardingSteps.length}</span>`;
  }

  // 設置動作
  setupAction(step) {
    if (step.action === 'click' && step.actionTarget) {
      const target = document.querySelector(step.actionTarget);
      if (target) {
        // 添加脈衝動畫
        target.classList.add('onboarding-pulse');
        
        // 等待使用者點擊
        const handler = () => {
          this.giveReward(step.reward);
          target.classList.remove('onboarding-pulse');
          target.removeEventListener('click', handler);
          setTimeout(() => this.next(), 500);
        };
        
        target.addEventListener('click', handler);
      }
    }
  }

  // 顯示 Modal 步驟
  showModalStep(step) {
    const modal = document.createElement('div');
    modal.className = 'onboarding-modal';
    modal.innerHTML = `
      <div class="onboarding-modal-overlay"></div>
      <div class="onboarding-modal-content">
        <div class="modal-header">
          <h2>${step.title}</h2>
        </div>
        <div class="modal-body">
          <p>${step.description}</p>
          ${step.id === 'complete' ? this.generateCompletionAnimation() : ''}
        </div>
        <div class="modal-footer">
          ${step.id === 'welcome' ? `
            <button class="btn btn-secondary" onclick="onboarding.skip()">跳過引導</button>
            <button class="btn btn-primary" onclick="onboarding.next()">開始引導</button>
          ` : `
            <button class="btn btn-primary" onclick="onboarding.complete()">開始使用</button>
          `}
        </div>
      </div>
    `;
    document.body.appendChild(modal);
  }

  // 生成完成動畫
  generateCompletionAnimation() {
    return `
      <div class="completion-animation">
        <div class="confetti">🎉</div>
        <div class="confetti">🎊</div>
        <div class="confetti">⭐</div>
        <div class="points-earned">+100 積分</div>
        <div class="achievement-earned">🏆 初學者</div>
      </div>
    `;
  }

  // 下一步
  next() {
    this.removeOverlay();
    this.removeModal();
    
    if (this.currentStep < onboardingSteps.length - 1) {
      this.showStep(this.currentStep + 1);
    } else {
      this.complete();
    }
  }

  // 上一步
  prev() {
    this.removeOverlay();
    this.removeModal();
    
    if (this.currentStep > 0) {
      this.showStep(this.currentStep - 1);
    }
  }

  // 跳過
  skip() {
    if (confirm('確定要跳過引導嗎？你可以稍後在設定中重新開始。')) {
      this.removeOverlay();
      this.removeModal();
      this.removeStepIndicator();
      this.isActive = false;
      this.saveOnboardingStatus(true);
      this.updateGamificationDisplay();
    }
  }

  // 完成
  complete() {
    this.removeOverlay();
    this.removeModal();
    this.removeStepIndicator();
    this.isActive = false;
    this.isCompleted = true;
    this.saveOnboardingStatus(true);
    
    // 給予獎勵
    const finalStep = onboardingSteps[onboardingSteps.length - 1];
    if (finalStep.reward) {
      this.giveReward(finalStep.reward);
    }
    
    // 解鎖所有功能
    this.unlockFeatures();
    
    // 更新顯示
    this.updateGamificationDisplay();
    
    // 顯示完成通知
    if (window.utils) {
      window.utils.showNotification('引導完成！已解鎖所有功能', 'success');
    }
  }

  // 給予獎勵
  giveReward(reward) {
    if (!reward) return;
    
    // 增加積分
    if (reward.points) {
      gamificationState.points += reward.points;
      this.saveGamificationState();
    }
    
    // 獲得成就
    if (reward.achievement) {
      if (!gamificationState.achievements.includes(reward.achievement)) {
        gamificationState.achievements.push(reward.achievement);
        this.saveGamificationState();
        this.showAchievementNotification(reward.achievement);
      }
    }
    
    // 顯示通知
    if (reward.message && window.utils) {
      window.utils.showNotification(reward.message, 'success');
    }
    
    // 更新顯示
    this.updateGamificationDisplay();
  }

  // 顯示成就通知
  showAchievementNotification(achievementId) {
    const achievements = {
      beginner: { name: '初學者', icon: '🎓' },
      action_practitioner: { name: '行動實踐者', icon: '✅' }
    };
    
    const achievement = achievements[achievementId];
    if (achievement && window.utils) {
      window.utils.showNotification(`${achievement.icon} 恭喜獲得「${achievement.name}」成就！`, 'success');
    }
  }

  // 解鎖功能
  unlockFeatures() {
    // 移除任何鎖定狀態
    document.querySelectorAll('.feature-locked').forEach(el => {
      el.classList.remove('feature-locked');
    });
  }

  // 移除遮罩層
  removeOverlay() {
    const overlay = document.getElementById('onboarding-overlay');
    if (overlay) {
      overlay.remove();
    }
  }

  // 移除 Modal
  removeModal() {
    const modal = document.querySelector('.onboarding-modal');
    if (modal) {
      modal.remove();
    }
  }

  // 移除步驟指示器
  removeStepIndicator() {
    const indicator = document.getElementById('onboarding-step-indicator');
    if (indicator) {
      indicator.remove();
    }
    // 移除引導進行中的 class
    document.body.classList.remove('onboarding-active');
  }

  // 儲存遊戲化狀態
  saveGamificationState() {
    localStorage.setItem('gamification_state', JSON.stringify(gamificationState));
  }

  // 載入遊戲化狀態
  loadGamificationState() {
    const saved = localStorage.getItem('gamification_state');
    if (saved) {
      Object.assign(gamificationState, JSON.parse(saved));
    }
  }

  // 更新遊戲化顯示
  updateGamificationDisplay() {
    this.loadGamificationState();
    
    // 更新 Header 中的積分顯示
    const pointsDisplay = document.getElementById('user-points');
    if (pointsDisplay) {
      pointsDisplay.textContent = `${gamificationState.points} 積分`;
    }
    
    // 更新等級顯示
    const level = this.calculateLevel(gamificationState.points);
    const levelDisplay = document.getElementById('user-level');
    if (levelDisplay) {
      levelDisplay.textContent = `等級 ${level}`;
    }
    
    // 更新進度條
    this.updateProgressBar();
  }

  // 計算等級
  calculateLevel(points) {
    if (points >= 1001) return 5;
    if (points >= 601) return 4;
    if (points >= 301) return 3;
    if (points >= 101) return 2;
    return 1;
  }

  // 更新進度條
  updateProgressBar() {
    const level = this.calculateLevel(gamificationState.points);
    const levelRanges = {
      1: { min: 0, max: 100 },
      2: { min: 101, max: 300 },
      3: { min: 301, max: 600 },
      4: { min: 601, max: 1000 },
      5: { min: 1001, max: Infinity }
    };
    
    const range = levelRanges[level];
    const progress = level === 5 ? 100 : 
      ((gamificationState.points - range.min) / (range.max - range.min)) * 100;
    
    const progressBar = document.getElementById('level-progress-bar');
    if (progressBar) {
      progressBar.style.width = `${progress}%`;
    }
  }
}

// 初始化引導系統
const onboarding = new OnboardingSystem();

// 載入遊戲化狀態
onboarding.loadGamificationState();

// 暴露到全域
window.onboarding = onboarding;
window.gamificationState = gamificationState;

