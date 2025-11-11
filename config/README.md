# Config Directory Guide

- `private/`：存放敏感憑證與 `.env`（未納入版本控制）。
- `secrets.example.env`：提供必要的環境變數樣板，請複製為 `config/private/secrets.env` 後填入實際值。
- 其他公開設定檔（如 `clients.yaml.example`）會保留在對應專案底下。

## 初始化步驟
1. 取得服務帳戶／密鑰檔案，放入 `config/private/`。
2. 複製 `secrets.example.env` 至 `config/private/secrets.env` 並填寫。
3. 執行專案 README 中的依賴安裝流程。
