## LINE Notify / Messaging API 研究筆記

### 1. 研究目的
- 定義週報推播的 LINE 正式通路，取代目前僅支援的 Google Chat。
- 釐清授權、訊息格式、頻率限制與部署需求，作為 Spec Kit T029/T028 的前置資料。

### 2. 相關產品定位
- 透過 LINE 官方帳號（Messaging API Channel）推送營運週報摘要。
- 主要面向：品牌營運團隊（多數使用 LINE 通知）。
- Google Chat 僅留作 SIT/UAT 測試渠道；正式版本需以 LINE 為主。

### 3. API 與授權流程
1. **Channel 建立**
   - 於 LINE Developers Console 建立 Messaging API Channel，取得 `channel_id`、`channel_secret`。
   - 設定 Webhook URL（若僅推播，可先不啟用 webhook）。
2. **Channel Access Token**
   - 透過 `POST /oauth2/v2.1/token` 取得長期或短期 access token。
   - 需妥善保存，並可透過 `/v2/oauth/verify` 或 `/oauth2/v2.1/verify` 驗證有效性。
   - 建議使用 Secret Manager 管理。
3. **推播端點**
   - `POST /v2/bot/message/push`：對單一 userId 推播。
   - `POST /v2/bot/message/multicast`：對多個 userId 同時推播（需先建立 audience）。
   - `POST /v2/bot/message/broadcast`：廣播所有好友（僅在官方帳號允許的情況）。
   - 需於 Header 帶入 `Authorization: Bearer {channel access token}`。
4. **訊息格式**
   - `text`、`template`、`flex` 等 JSON 結構。週報推播建議使用 **Flex Message** 呈現摘要＋CTA。
   - 可先用 `POST /v2/bot/message/validate/push` 驗證 payload。
5. **Webhook（可選）**
   - 若未來需要回收使用者互動或確認送達，可於 Webhook 接收事件。當前 POC 非必須。

> 參考來源：[LINE Messaging API Reference][line-api]

### 4. 頻率與資源限制
- **Rate limits**：依官方帳號方案而定。需檢查每月訊息額度與每分鐘速率限制，避免超量導致 API 失敗。
- **重試機制**：若回傳 429 或 5xx，需實作退避重試（最多 3 次）。
- **訊息大小**：Flex message JSON 大小有限制（< 50 KB）。需確保週報摘要內容符合範圍。
- **附件**：若要附圖，可先將圖片上傳至公開 URL（如 GCS 公共連結），再於 Flex message 中引用。

### 5. 研究任務建議（對映 Spec Kit T029/T028/T030）
1. **T029 - LINE Notify API/權限/速率研究**
   - 整理 Channel 建立流程與權限需求（帳號角色、後台設定）。
   - 確認需推播的 userId 來源：若為內部使用，可採 `multicast` (固定 userId list)；若要對品牌客戶推播，需有對應會員資料或 LINE UserId 綁定。
   - 編寫簡易測試腳本（Python / curl）驗證 push message。
2. **T028 - LINE Notify Plugin 原型**
   - 建立 `line_notify.py` 模組，封裝 token 管理、訊息格式（Flex + text fallback）。
   - 支援訊息模板（營運摘要、CTA 連結）。
3. **T030 - Plugin Loader 機制**
   - 為通知中心加入插件架構，根據配置啟用 Google Chat / Email / LINE。
   - 設計 JSON/YAML 設定，定義 channel 列表與優先順序。

### 6. 待確認問題
- 使用者名單來源：目前只推播給內部（聖保羅/勤億）還是未來要對外部客戶？需明確 userId / 群組 ID 的取得方式。
- 需不需要彈性設定不同品牌的 LINE token？若是，多品牌需各自建立 channel/token。
- Flex message 模板由誰設計與驗證？是否需設計模式（A/B 版）？
- 是否需提供報表下載連結？若是，需要設定公開可存取的 URL（有限期）或登入驗證。

### 7. 建議執行順序
1. 建立 Sandbox 官方帳號並取得 access token。
2. 使用 `line_notify_poc.py` 驗證推播成功：
   ```bash
   # 環境變數設定
   export LINE_CHANNEL_ACCESS_TOKEN="..."         # 存於 config/secrets.env 或 Secret Manager
   export LINE_TARGET_ID="Uxxxxxxxx"              # userId 或 groupId；多個可用 LINE_TARGET_IDS

   # 發送純文字
   python line_notify_poc.py --text "週報推播測試"

   # 或發送 Flex Message
   python line_notify_poc.py --flex flex_payload.json
   ```
   ✅ 2025-11-11 測試成功（Target: `Udb236aa0d298eff2e04c73b5fcbea957`，訊息："週報推播測試訊息"）
3. 將研究結果更新至 `plan.md` / `tasks.md`（T029 → Done），並拉動後續 T028/T030。
4. 完成 Plugin 整合後，安排 SIT 測試（與 Google Chat、Email 並行）。

### 8. 相關連結
- LINE Messaging API Reference  
  <https://developers.line.biz/en/reference/messaging-api/>
- LINE Platform 基礎：Channel access token  
  <https://developers.line.biz/en/docs/messaging-api/channel-access-tokens/>
- Flex Message 設計指南  
  <https://developers.line.biz/en/docs/messaging-api/using-flex-messages/>

[line-api]: https://developers.line.biz/en/reference/messaging-api/

