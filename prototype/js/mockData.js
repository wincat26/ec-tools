/**
 * AI 營運顧問系統 — 假資料（Mock Data）
 * 
 * 用途：供 Prototype 展示使用
 * 資料來源：根據 PRD 中的範例資料整理
 */

const mockData = {
  // 營運摘要資料
  summary: {
    revenue: 825000,
    revenueChange: -8.4,
    traffic: 18200,
    conversionRate: 1.2,
    avgOrderValue: 1520,
    dateRange: "2025/10/21 - 2025/10/27",
    previousWeek: "2025/10/14 - 2025/10/20"
  },

  // KPI 金字塔資料
  kpiPyramid: {
    revenue: 825000,
    traffic: {
      value: 18200,
      change: -5.2,
      label: "流量 (Sessions)"
    },
    conversion: {
      value: 1.2,
      change: -0.3,
      label: "轉換率 (%)"
    },
    aov: {
      value: 1520,
      change: 2.1,
      label: "平均客單價 (NT$)"
    }
  },

  // 流量會員分析數據
  trafficMemberAnalysis: {
    newUsers: {
      registered: 3200,
      purchased: 48,
      purchaseRate: 1.5
    },
    returningUsers: {
      visited: 15000,
      purchased: 170,
      purchaseRate: 1.13
    },
    totalTraffic: 18200
  },

  // 專家支援資料
  expertSupport: {
    search: {
      name: "SEO 優化專家",
      expertName: "張大明",
      title: "10年 SEO 經驗",
      avatar: "👨‍💼",
      description: "專精 Google 搜尋排名優化，幫助提升自然流量與關鍵字轉換",
      price: 2999,
      period: "月",
      features: [
        "每週一次策略檢視會議",
        "關鍵字排名追蹤與優化建議",
        "技術 SEO 檢測與修復",
        "內容策略規劃"
      ],
      rating: 4.8,
      subscribers: 156,
      isSubscribed: false
    },
    ads: {
      name: "廣告投放專家",
      expertName: "李雅文",
      title: "Meta/Google Ads 認證",
      avatar: "👩‍💼",
      description: "Meta 與 Google Ads 雙平台專家，優化 ROAS 與轉換成本",
      price: 3999,
      period: "月",
      features: [
        "廣告素材 A/B 測試建議",
        "受眾設定優化",
        "預算分配策略",
        "每週成效檢視"
      ],
      rating: 4.9,
      subscribers: 203,
      isSubscribed: false
    },
    email: {
      name: "Email 行銷專家",
      expertName: "王小明",
      title: "CRM 策略規劃",
      avatar: "👨‍💻",
      description: "Email 開信率與轉換率優化，自動化流程設計",
      price: 2499,
      period: "月",
      features: [
        "EDM 模板設計建議",
        "分眾策略規劃",
        "自動化流程優化",
        "A/B 測試執行"
      ],
      rating: 4.7,
      subscribers: 89,
      isSubscribed: false
    },
    ai: {
      name: "AI 工具應用專家",
      expertName: "陳美玲",
      title: "AI 行銷顧問",
      avatar: "👩‍🔬",
      description: "整合 AI 工具提升營運效率，ChatGPT/Midjourney 應用",
      price: 3499,
      period: "月",
      features: [
        "AI 工具導入規劃",
        "內容生成流程優化",
        "自動化腳本撰寫",
        "工具組合建議"
      ],
      rating: 4.6,
      subscribers: 124,
      isSubscribed: false
    },
    social: {
      name: "社群行銷專家",
      expertName: "林佳蓉",
      title: "IG/FB 社群經營",
      avatar: "👩‍🎨",
      description: "社群內容策略、KOL 合作、粉絲互動優化",
      price: 2799,
      period: "月",
      features: [
        "內容規劃與排程",
        "KOL 合作媒合",
        "社群互動策略",
        "趨勢分析報告"
      ],
      rating: 4.8,
      subscribers: 178,
      isSubscribed: false
    }
  },

  // 七大流量策略表
  trafficSources: [
    {
      source: "搜尋",
      sessions: 3200,
      cvr: 1.5,
      aov: 1480,
      revenue: 71000,
      trend: "up",
      change: 3.2,
      memberBreakdown: {
        newUsers: {
          registered: 960,
          purchased: 15,
          purchaseRate: 1.56
        },
        returningUsers: {
          visited: 2240,
          purchased: 33,
          purchaseRate: 1.47
        }
      }
    },
    {
      source: "廣告",
      sessions: 8500,
      cvr: 1.1,
      aov: 1600,
      revenue: 150000,
      trend: "down",
      change: -12.0,
      memberBreakdown: {
        newUsers: {
          registered: 2550,
          purchased: 25,
          purchaseRate: 0.98
        },
        returningUsers: {
          visited: 5950,
          purchased: 68,
          purchaseRate: 1.14
        }
      }
    },
    {
      source: "社群",
      sessions: 2100,
      cvr: 0.9,
      aov: 1200,
      revenue: 22000,
      trend: "down",
      change: -5.5,
      memberBreakdown: {
        newUsers: {
          registered: 420,
          purchased: 5,
          purchaseRate: 1.19
        },
        returningUsers: {
          visited: 1680,
          purchased: 14,
          purchaseRate: 0.83
        }
      }
    },
    {
      source: "直接",
      sessions: 2800,
      cvr: 1.8,
      aov: 1800,
      revenue: 91000,
      trend: "up",
      change: 4.1,
      memberBreakdown: {
        newUsers: {
          registered: 280,
          purchased: 2,
          purchaseRate: 0.71
        },
        returningUsers: {
          visited: 2520,
          purchased: 48,
          purchaseRate: 1.90
        }
      }
    },
    {
      source: "Email",
      sessions: 450,
      cvr: 2.5,
      aov: 2000,
      revenue: 22500,
      trend: "stable",
      change: 0.8,
      memberBreakdown: {
        newUsers: {
          registered: 0,
          purchased: 0,
          purchaseRate: 0
        },
        returningUsers: {
          visited: 450,
          purchased: 11,
          purchaseRate: 2.44
        }
      }
    },
    {
      source: "推薦",
      sessions: 750,
      cvr: 1.2,
      aov: 1350,
      revenue: 12150,
      trend: "up",
      change: 6.3,
      memberBreakdown: {
        newUsers: {
          registered: 600,
          purchased: 8,
          purchaseRate: 1.33
        },
        returningUsers: {
          visited: 150,
          purchased: 1,
          purchaseRate: 0.67
        }
      }
    },
    {
      source: "其他",
      sessions: 400,
      cvr: 0.8,
      aov: 1100,
      revenue: 3520,
      trend: "down",
      change: -2.1,
      memberBreakdown: {
        newUsers: {
          registered: 80,
          purchased: 0,
          purchaseRate: 0
        },
        returningUsers: {
          visited: 320,
          purchased: 3,
          purchaseRate: 0.94
        }
      }
    }
  ],

  // 轉換漏斗資料
  conversionFunnel: {
    ranges: [
      { id: "7d", label: "最近 7 天", subtitle: "最近 7 天 · GA4 標準事件" },
      { id: "30d", label: "最近 30 天", subtitle: "最近 30 天 · GA4 標準事件" },
      { id: "90d", label: "最近 90 天", subtitle: "最近 90 天 · GA4 標準事件" }
    ],
    overall: {
      "7d": {
        steps: [
          { key: "all_visitors", label: "訪客 (all visitors)", count: 48500 },
          { key: "view_item", label: "商品瀏覽 (view_item)", count: 18200 },
          { key: "add_to_cart", label: "加入購物車 (add_to_cart)", count: 7300 },
          { key: "begin_checkout", label: "開始結帳 (begin_checkout)", count: 4100 },
          { key: "purchase", label: "完成購買 (purchase)", count: 2280 }
        ]
      },
      "30d": {
        steps: [
          { key: "all_visitors", label: "訪客 (all visitors)", count: 132000 },
          { key: "view_item", label: "商品瀏覽 (view_item)", count: 51200 },
          { key: "add_to_cart", label: "加入購物車 (add_to_cart)", count: 20600 },
          { key: "begin_checkout", label: "開始結帳 (begin_checkout)", count: 11800 },
          { key: "purchase", label: "完成購買 (purchase)", count: 6650 }
        ]
      },
      "90d": {
        steps: [
          { key: "all_visitors", label: "訪客 (all visitors)", count: 368000 },
          { key: "view_item", label: "商品瀏覽 (view_item)", count: 142000 },
          { key: "add_to_cart", label: "加入購物車 (add_to_cart)", count: 59200 },
          { key: "begin_checkout", label: "開始結帳 (begin_checkout)", count: 32400 },
          { key: "purchase", label: "完成購買 (purchase)", count: 18600 }
        ]
      }
    },
    productSegments: [
      {
        id: "topProducts",
        label: "Top 商品",
        items: [
          {
            name: "橄欖油麵包組",
            steps: [
              { key: "view_item", label: "查看", count: 4200 },
              { key: "add_to_cart", label: "加購物車", count: 1620 },
              { key: "begin_checkout", label: "結帳", count: 980 },
              { key: "purchase", label: "成交", count: 520 }
            ]
          },
          {
            name: "經典果醬組合",
            steps: [
              { key: "view_item", label: "查看", count: 3800 },
              { key: "add_to_cart", label: "加購物車", count: 1480 },
              { key: "begin_checkout", label: "結帳", count: 900 },
              { key: "purchase", label: "成交", count: 470 }
            ]
          },
          {
            name: "手工餅乾禮盒",
            steps: [
              { key: "view_item", label: "查看", count: 3100 },
              { key: "add_to_cart", label: "加購物車", count: 1210 },
              { key: "begin_checkout", label: "結帳", count: 720 },
              { key: "purchase", label: "成交", count: 360 }
            ]
          }
        ]
      },
      {
        id: "categories",
        label: "商品類別",
        items: [
          {
            name: "調味油系列",
            steps: [
              { key: "view_item", label: "查看", count: 5200 },
              { key: "add_to_cart", label: "加購物車", count: 2100 },
              { key: "begin_checkout", label: "結帳", count: 1280 },
              { key: "purchase", label: "成交", count: 720 }
            ]
          },
          {
            name: "甜點零食",
            steps: [
              { key: "view_item", label: "查看", count: 4600 },
              { key: "add_to_cart", label: "加購物車", count: 1640 },
              { key: "begin_checkout", label: "結帳", count: 980 },
              { key: "purchase", label: "成交", count: 440 }
            ]
          },
          {
            name: "飲品沖泡",
            steps: [
              { key: "view_item", label: "查看", count: 3200 },
              { key: "add_to_cart", label: "加購物車", count: 980 },
              { key: "begin_checkout", label: "結帳", count: 610 },
              { key: "purchase", label: "成交", count: 290 }
            ]
          }
        ]
      }
    ],
    campaignSegments: [
      {
        id: "campaigns",
        label: "熱門活動",
        items: [
          {
            name: "夏日冷泡折扣",
            steps: [
              { key: "campaign_view", label: "活動頁", count: 6200 },
              { key: "view_item", label: "商品頁", count: 2800 },
              { key: "purchase", label: "訂單", count: 740 }
            ]
          },
          {
            name: "會員雙倍點數週",
            steps: [
              { key: "campaign_view", label: "活動頁", count: 5400 },
              { key: "view_item", label: "商品頁", count: 3100 },
              { key: "purchase", label: "訂單", count: 920 }
            ]
          },
          {
            name: "健康早餐組合",
            steps: [
              { key: "campaign_view", label: "活動頁", count: 4600 },
              { key: "view_item", label: "商品頁", count: 2500 },
              { key: "purchase", label: "訂單", count: 620 }
            ]
          }
        ]
      },
      {
        id: "channels",
        label: "推廣渠道",
        items: [
          {
            name: "Email EDM",
            steps: [
              { key: "campaign_view", label: "活動頁", count: 3800 },
              { key: "view_item", label: "商品頁", count: 2100 },
              { key: "purchase", label: "訂單", count: 540 }
            ]
          },
          {
            name: "社群貼文",
            steps: [
              { key: "campaign_view", label: "活動頁", count: 4200 },
              { key: "view_item", label: "商品頁", count: 1900 },
              { key: "purchase", label: "訂單", count: 430 }
            ]
          },
          {
            name: "付費廣告",
            steps: [
              { key: "campaign_view", label: "活動頁", count: 5600 },
              { key: "view_item", label: "商品頁", count: 3200 },
              { key: "purchase", label: "訂單", count: 880 }
            ]
          }
        ]
      }
    ]
  },

  // 商品結構資料
  products: {
    topProducts: [
      {
        name: "橄欖油麵包組",
        revenue: 125000,
        orders: 85,
        share: 15.2
      },
      {
        name: "經典果醬組合",
        revenue: 98000,
        orders: 120,
        share: 11.9
      },
      {
        name: "手工餅乾禮盒",
        revenue: 87000,
        orders: 95,
        share: 10.5
      },
      {
        name: "蜂蜜檸檬飲",
        revenue: 72000,
        orders: 150,
        share: 8.7
      },
      {
        name: "健康堅果包",
        revenue: 65000,
        orders: 80,
        share: 7.9
      }
    ],
    priceDistribution: {
      high: { count: 45, share: 20.6 },
      medium: { count: 120, share: 55.0 },
      low: { count: 53, share: 24.3 }
    }
  },

  // 平均訂單金額分析（整體／新客／回購客）
  aovAnalysis: {
    segments: {
      overall: {
        label: "整體",
        cartDistribution: [
          { label: "單品（1 件）", share: 38, avgValue: 920 },
          { label: "兩件組（2 件）", share: 28, avgValue: 1580 },
          { label: "三件組（3 件）", share: 22, avgValue: 2140 },
          { label: "四件以上", share: 12, avgValue: 2860 }
        ],
        priceBands: [
          { label: "高單價（NT$2,000+）", share: 24, avgOrderValue: 2680 },
          { label: "中單價（NT$1,000-2,000）", share: 52, avgOrderValue: 1480 },
          { label: "低單價（NT$1,000 以下）", share: 24, avgOrderValue: 780 }
        ]
      },
      new: {
        label: "新客",
        cartDistribution: [
          { label: "單品（1 件）", share: 56, avgValue: 860 },
          { label: "兩件組（2 件）", share: 26, avgValue: 1320 },
          { label: "三件組（3 件）", share: 12, avgValue: 1780 },
          { label: "四件以上", share: 6, avgValue: 2150 }
        ],
        priceBands: [
          { label: "高單價（NT$2,000+）", share: 12, avgOrderValue: 2280 },
          { label: "中單價（NT$1,000-2,000）", share: 48, avgOrderValue: 1420 },
          { label: "低單價（NT$1,000 以下）", share: 40, avgOrderValue: 720 }
        ]
      },
      returning: {
        label: "回購客",
        cartDistribution: [
          { label: "單品（1 件）", share: 18, avgValue: 1120 },
          { label: "兩件組（2 件）", share: 32, avgValue: 1680 },
          { label: "三件組（3 件）", share: 35, avgValue: 2360 },
          { label: "四件以上", share: 15, avgValue: 3180 }
        ],
        priceBands: [
          { label: "高單價（NT$2,000+）", share: 38, avgOrderValue: 3020 },
          { label: "中單價（NT$1,000-2,000）", share: 44, avgOrderValue: 1650 },
          { label: "低單價（NT$1,000 以下）", share: 18, avgOrderValue: 920 }
        ]
      }
    },
    insights: [
      {
        segment: "overall",
        text: "整體 AOV 由兩件組與三件組帶動，占比合計 50%，建議維持組合折扣主題。"
      },
      {
        segment: "new",
        text: "新客多以單件入手（56%），可推出 NT$990 入門包與第一次加價購誘因。"
      },
      {
        segment: "returning",
        text: "回購客有 35% 購買三件組、15% 購買四件以上，適合推訂閱制或專屬套組。"
      }
    ]
  },

  // Guideline 智能建議
  guidelines: [
    {
      id: "G001",
      category: "轉換率",
      source: "Meta Ads",
      metric: "CVR",
      currentValue: 1.1,
      delta: -0.3,
      insight: "Meta Ads 流量穩定，但轉換率下降 0.3%，主要出現在橄欖油麵包商品。",
      suggestion: "重新設定 Meta Ads 受眾，聚焦最近14天瀏覽過商品頁但未完成結帳的訪客。同時，測試商品頁 CTA 顏色以提升互動率。",
      confidenceScore: 0.88,
      createdAt: "2025-10-27T09:30:00"
    },
    {
      id: "G002",
      category: "客單價",
      source: "整體",
      metric: "AOV",
      currentValue: 1520,
      delta: -5.2,
      insight: "高價商品比例偏高，影響新客轉換。",
      suggestion: "推出 NT$990 入門包活動，吸引新客嘗試。並在購物車頁面增加加價購推薦。",
      confidenceScore: 0.82,
      createdAt: "2025-10-27T09:35:00"
    },
    {
      id: "G003",
      category: "流量",
      source: "廣告",
      metric: "Sessions",
      currentValue: 8500,
      delta: -12.0,
      insight: "廣告流量下降 12%，主要為 Meta Ads 曝光減少。",
      suggestion: "檢視 Meta Ads 預算分配，增加高 ROAS 活動預算。同時，重新審視廣告素材疲勞度。",
      confidenceScore: 0.85,
      createdAt: "2025-10-27T09:40:00"
    },
    {
      id: "G004",
      category: "轉換率",
      source: "社群",
      metric: "CVR",
      currentValue: 0.9,
      delta: -0.2,
      insight: "社群流量轉換率持續偏低，可能是內容與商品連結度不足。",
      suggestion: "加強社群內容與商品頁的連結，在貼文中加入明確的 CTA 按鈕。考慮與 KOL 合作推廣入門商品。",
      confidenceScore: 0.75,
      createdAt: "2025-10-27T09:45:00"
    }
  ],

  // 行動任務清單
  tasks: [
    {
      id: "T001",
      sourceGuidelineId: "G001",
      title: "重新設定 Meta Ads 受眾",
      description: "聚焦最近14天瀏覽過商品頁但未完成結帳的訪客",
      category: "轉換率",
      assignee: "行銷組",
      priority: "high",
      status: "進行中",
      dueDate: "2025-11-05",
      createdBy: "營運經理",
      createdAt: "2025-10-27T10:00:00",
      performanceBefore: 1.1,
      performanceAfter: null,
      impactScore: null
    },
    {
      id: "T002",
      sourceGuidelineId: "G002",
      title: "推出 NT$990 入門包活動",
      description: "吸引新客嘗試，提升轉換率",
      category: "客單價",
      assignee: "電商組",
      priority: "medium",
      status: "已完成",
      dueDate: "2025-11-07",
      createdBy: "營運經理",
      createdAt: "2025-10-20T09:00:00",
      completedAt: "2025-10-25T17:00:00",
      performanceBefore: 1480,
      performanceAfter: 1520,
      impactScore: 2.7
    },
    {
      id: "T003",
      sourceGuidelineId: "G003",
      title: "檢視 Meta Ads 預算分配",
      description: "增加高 ROAS 活動預算，重新審視廣告素材",
      category: "流量",
      assignee: "行銷組",
      priority: "high",
      status: "未開始",
      dueDate: "2025-11-10",
      createdBy: "營運經理",
      createdAt: "2025-10-27T10:15:00",
      performanceBefore: 8500,
      performanceAfter: null,
      impactScore: null
    },
    {
      id: "T004",
      sourceGuidelineId: "G004",
      title: "加強社群內容與商品頁連結",
      description: "在貼文中加入明確的 CTA 按鈕，考慮與 KOL 合作",
      category: "轉換率",
      assignee: "社群組",
      priority: "medium",
      status: "未開始",
      dueDate: "2025-11-12",
      createdBy: "營運經理",
      createdAt: "2025-10-27T10:20:00",
      performanceBefore: 0.9,
      performanceAfter: null,
      impactScore: null
    }
  ]
};

// 匯出資料（如果使用模組系統）
if (typeof module !== 'undefined' && module.exports) {
  module.exports = mockData;
}

