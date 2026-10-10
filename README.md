# Web Automation Portfolio

## 1. Project Overview

個人 QA Automation Engineer 作品集，使用 Python、Pytest 與 Playwright 建立自動化測試框架，測試本機 Docker PrestaShop Demo，涵蓋 Frontend、Admin、REST API 與 MySQL。

專案展示 UI 操作、POM、Fixture、登入狀態隔離與跨層資料驗證能力；測試範圍為個人 Demo 環境，不屬於公司正式產品測試系統。

## 2. Tech Stack & Key Features

| 技術 | 既有實作 |
| --- | --- |
| Python 3.12 / Pytest | 測試執行、markers 與 assertions |
| Playwright sync API | UI 自動化與 `expect()` 驗證 |
| Page Object Model (POM) | 集中管理頁面操作與 Locator |
| Pytest Fixtures | 共用 session Browser，為各測試建立獨立 BrowserContext |
| BrowserContext isolation | Frontend / Admin 分開登入，E2E 使用不同 contexts |
| REST API / requests | read-only GET，驗證回應與同筆訂單資料 |
| MySQL / mysql-connector-python | read-only SELECT，驗證訂單及明細 |
| Decimal | API / DB 金額精確比較，保留 DB Decimal 精度 |
| python-dotenv | 從本機 `.env` 讀取環境設定 |
| Allure | 產生 raw results，停用原始 capture 附件並遮蔽已知敏感診斷 |

## 3. E2E Workflow

```text
Frontend → Admin → Orders API → MySQL DB
          同一個當次動態 Order Reference
```

1. Frontend 登入，選擇商品、Shipping 與 Bank Wire，送出一筆 Demo Order。
2. 從 Order Confirmation 取得當次動態 Order Reference。
3. Admin 在獨立 BrowserContext 搜尋同一個 Reference，驗證訂單、會員、Payment 與狀態文字。
4. Orders API 以 GET 及相同 Reference 篩選，確認 HTTP 200 且唯一一筆訂單。
5. MySQL 以 SELECT 查詢相同訂單及明細；API / DB 比對 Order ID、Customer ID、Payment、Status ID 與 Total Paid。Admin 的狀態文字另行驗證，不直接與 ID 比較。
6. Total Paid 使用 Decimal 精確比較；訂單明細另驗證商品、數量及正值價格。

每次 E2E 只由 Frontend 建立一筆訂單；Admin、Orders API 與 MySQL 驗證不額外建立訂單。重複執行會新增 Demo 訂單。

## 4. Test Coverage

目前共有 8 支正式測試：

| 測試 | 類型 | 驗證重點 | 資料副作用 |
| --- | --- | --- | --- |
| [Admin Login](tests/admin/test_admin_login.py) | Smoke | 登入後 Dashboard 可見 | 建立登入狀態 |
| [Frontend Registration](tests/frontend/test_registration.py) | Smoke | 唯一 Email 註冊成功並登入 | 新增一筆 Demo 會員 |
| [Frontend Login](tests/frontend/test_login.py) | Smoke | 既有帳號登入成功 | 建立登入狀態 |
| [Add to Cart](tests/frontend/test_add_to_cart.py) | Smoke | 商品名稱與數量 | 改變 Cart 狀態 |
| [Checkout Shipping](tests/frontend/test_checkout_shipping.py) | Smoke | 既有 France Address 與可用 Shipping method | 改變 Cart / Checkout 狀態，不送出訂單 |
| [Checkout Payment](tests/frontend/test_checkout_payment.py) | Smoke | Bank Wire 可見且可選取 | 改變 Cart / Checkout 狀態，不送出訂單 |
| [Products API GET](tests/api/test_products_api.py) | Smoke / API | HTTP 200、JSON 商品資料與必要欄位 | 僅 GET，不寫入資料 |
| [Bank Wire Order E2E](tests/e2e/test_bank_wire_order.py) | E2E | Frontend → Admin → Orders API → DB | 每次新增一筆 Demo 訂單 |

Smoke 聚焦單一功能或流程節點；E2E 驗證同筆訂單跨 UI、API 與 DB 的一致性。BrowserContext 隔離登入狀態，並不會回復共享 Demo 資料庫中的會員、Cart 或訂單變更。

## 5. Latest Test Results

**Day 22 Full Regression — 歷史驗證結果**

| Passed | Failed | Skipped | 執行時間 |
| --- | --- | --- | --- |
| 8 | 0 | 0 | 71.06 seconds |

執行指令：`python -m pytest --alluredir=allure-results -v`。

Day 22 結果為 `8 passed in 71.06s (0:01:11)`，當時使用本機 `PLAYWRIGHT_SLOW_MO=700`。Day 24 僅進行環境診斷與文件整理，未重新執行測試。

## 6. Project Structure

```text
pages/
├── admin/
└── frontend/
tests/
├── admin/
├── api/
├── e2e/
└── frontend/
testdata/
utils/
conftest.py
pytest.ini
requirements.txt
.env.example
README.md
PROGRESS.md
```

## 7. Setup & Execution

### 測試環境前置條件

- 自行準備本機 Docker PrestaShop + MySQL，確認 Frontend、Admin 與 DB 可連線。Repository 未提供可直接重建 Demo 環境的 Docker Compose 設定。
- 準備可登入的 Frontend / Admin 測試帳號；Checkout 需既有 France Delivery Address、測試所需商品、`My carrier` 與 Bank Wire payment method。
- 啟用 PrestaShop Webservice；Products Smoke 使用既有 Klaviyo products GET endpoint，Orders 使用一般 `/api/orders` 與獨立、僅授予 `orders GET` 的 Key。
- 自行設定 `.env.example` 所列 URL、帳號、DB 與 API 欄位。`REGISTRATION_TEST_PASSWORD` 必須獨立設定，不共用 Frontend / Admin 密碼。

### Windows PowerShell 安裝

從專案根目錄執行；只在尚無 `.venv` 時建立虛擬環境：

```powershell
if (-not (Test-Path .venv)) {
    py -3.12 -m venv .venv
}
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m playwright install chromium
```

只在第一次建立本機設定時複製範本，保留已有 `.env`：

```powershell
if (-not (Test-Path .env)) {
    Copy-Item .env.example .env
}
```

敏感值由使用者自行填入本機 `.env`。Day 24 診斷已確認本機 Python 3.12.10、現有 `.venv` 及主要套件可正常執行／匯入，無須重建。

### 執行測試

完成環境設定並啟用虛擬環境後：

```powershell
python -m pytest -v
python -m pytest --alluredir=allure-results -v
```

以上是兩次獨立執行，請擇一；包含 Registration 與 E2E 時，每次都可能新增會員與訂單。也可指定範圍：

```powershell
python -m pytest -m smoke -v
python -m pytest tests/e2e/test_bank_wire_order.py -v
```

預設為 headed；可加入 `--headless`。`PLAYWRIGHT_SLOW_MO` 控制操作速度，`BROWSER_MAXIMIZED` 控制 headed 視窗顯示。

## 8. Security & Limitations

- 憑證僅放在本機 `.env`，不得提交 Git；`.env.example` 的敏感欄位為空白，不包含真實憑證。
- REST API 僅執行 GET、MySQL 僅執行 SELECT；Frontend Registration 與 E2E 仍會建立 Demo 資料。
- Trace、Screenshot、Video 依目前安全政策停用；不得開啟 Playwright DEBUG / PWDEBUG 或附加未處理的敏感產物。
- Allure 僅產生 raw results，目前未提供 Allure HTML Report 或 CI/CD。
- 本機 Docker Demo 環境與資料未包含在 Repository 中，需自行準備。
- `.gitignore` 與已知憑證遮蔽不代表全面安全；歷史產物、未知／舊憑證、外部 logger 與手動附件未宣稱已全面清查。

## 9. Development History

詳細 Day 1～24 開發與驗證紀錄：[Development Progress](PROGRESS.md)。
