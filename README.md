# Web Automation Portfolio

這是一個以 Python 建立的 Web 自動化測試作品集，用來展示可維護的端對端測試架構。

## 專案目的

本專案使用 Pytest、Playwright sync API 與 Page Object Model 撰寫 UI 自動化測試。目標是逐步建立清楚、可擴充、適合作為 QA Automation Portfolio 的測試專案。

目前主要支援：

- `frontend`
- `admin`

每個測試都會建立新的 `BrowserContext`，避免不同入口或登入狀態互相共用。

## 技術架構

本專案使用 Python 3.12 + Pytest + Playwright 建立 Web UI 自動化測試框架，並採用 Page Object Model（POM）管理頁面操作與 Locator。

- Python 3.12
- Pytest
- Playwright sync API
- Page Object Model
- python-dotenv
- Allure raw results
- Playwright Trace on Failure（歷史功能；目前安全政策停用）
- REST API Automation
- requests
- MySQL DB Validation
- mysql-connector-python

## 專案結構

```text
pages/
  admin/
  common/
  frontend/
tests/
  admin/
  api/
  e2e/
  frontend/
  smoke/
testdata/
utils/
conftest.py
pytest.ini
.env
.env.example
README.md
PROGRESS.md
```

## 目前狀態

目前已完成基礎 Pytest 設定、Playwright fixtures、環境變數讀取、Admin Login Page Object、Frontend Registration Page Object、Frontend Login Page Object、Frontend Product / Cart / Checkout Page Object、Allure raw results、歷史失敗截圖 / Trace 功能（Day 22 因憑證安全停用）、REST API Automation 第一階段、MySQL DB Validation，以及 smoke / e2e tests。

Admin Login smoke test 會使用正確 Admin 帳號密碼登入後台，並透過 Playwright `expect()` 驗證 Dashboard 標題可見。

Frontend Registration smoke test 會使用唯一 Email 與有效註冊資料建立新會員，並透過 Playwright `expect()` 驗證登入狀態。

Frontend Login smoke test 會使用固定 Frontend 測試帳號登入，並透過 Playwright `expect()` 驗證登入狀態。

Frontend Add to Cart smoke test 會從 demo shop 選擇穩定商品加入購物車，並透過 Playwright `expect()` 驗證 Cart 中的商品名稱與數量。

Frontend Checkout Shipping smoke test 會使用固定 Frontend 測試帳號登入、加入既有穩定商品、從 Cart 進入 Checkout，使用帳號內已存在的 France Delivery Address 進入 Shipping Method，並透過 Playwright `expect()` 驗證至少一個未 disabled 的 Shipping method 顯示。

Frontend Checkout Payment smoke test 會沿用既有 Checkout 流程，確認 France Delivery Address 後選擇 `My carrier`，進入 Payment step，並驗證實際 UI 顯示的 `Pay by bank wire` payment method 可見且 radio 可選取。此測試不會勾選 Terms、不會送出 Place order，也不會建立 Order。

Bank Wire Order E2E test 會使用固定 Frontend 測試帳號建立真實測試訂單：登入、加入穩定商品、使用既有 France Delivery Address、選擇 `My carrier`、選擇 Bank Wire、勾選 Terms、Place order，最後驗證 Order Confirmation、取得本次 Order Reference。接著測試會使用獨立 Admin `BrowserContext` 登入 Back Office，在 Orders 頁以同一個 Order Reference 搜尋並驗證訂單資料。接著使用獨立 Orders GET Key 查詢一般 `/api/orders`，以本次動態 Order Reference 找到唯一訂單，再使用同一個 Reference 查詢 MySQL，驗證 `ps_orders`、customer、status 與 order detail 資料，並比對 API 與 DB。每次 E2E 僅由 Frontend 建立一筆測試訂單，Admin、API、DB 驗證不另外建立訂單；不同 pytest 執行可產生新的測試訂單。完整流程為 Frontend → Admin → API → DB。

API smoke test 會使用 PrestaShop Webservice 的 read-only GET endpoint，透過 `.env` 的 `API_BASE_URL` 與 `API_KEY` 驗證 products resource 可以回傳 JSON 商品資料。第一階段 API Automation 只執行 GET，不透過 API 建立、修改或刪除資料。

Allure 已可透過 pytest 產生 raw results。Day 22 安全補強後，所有自訂 UI contexts 不產生失敗截圖，避免任意敏感畫面洩漏；不依賴密碼欄位顯示遮蔽。

Day 22 安全補強後，所有自訂 Frontend / Admin BrowserContext 均不錄製 Playwright Trace，包含 Registration、Login、Checkout 與跨站 E2E。舊 trace 可能含敏感資料；本次未清除或宣稱已清理歷史產物。

Klaviyo Products API Smoke 與 Orders API E2E Validation 已完成；尚未加入 video recording 或 BasePage。

### Orders API E2E Validation

- Orders 使用獨立的 read-only GET Webservice Key，透過 `ORDERS_API_BASE_URL` 與 `ORDERS_API_KEY` 提供；既有 Klaviyo `API_BASE_URL`、`API_KEY` 與 Products Smoke 保留。
- `orders_api_client` fixture 重用 `PrestaShopApiClient`，使用 Basic Auth（Key 作為 username，password 留空）；缺少 Orders 設定時明確報錯，不以其他 Key 替代。
- Frontend Order Confirmation 取得本次動態 `order_reference`；Admin 搜尋及詳細頁、Orders API filter、DB SELECT 均使用同一個 Reference，不硬編碼 Order Reference 或 Order ID。
- GET `/api/orders` 參數：`output_format=JSON`、`filter[reference]=[本次order_reference]`、`display=[id,reference,id_customer,current_state,payment,total_paid]`。
- 驗證 HTTP 200、最外層 object 含 `orders` array、恰好一筆訂單及 Reference 一致。
- 比對 API / DB 的 Order ID、Customer ID、Payment、Current State ID、Total Paid；API 金額以 Decimal 轉換，DB 保留原始 Decimal 精度。
- API 狀態 ID 與 DB 狀態 ID 比對；Admin 狀態文字與既有 DB 狀態名稱 assertions 保留，不直接比較 ID 與 UI 文字。
- API 僅使用 GET，DB 僅使用 SELECT；保留 BrowserContext 隔離；失敗影像與原始 Log 附件依 Day 22 安全政策停用，Allure 測試結果仍保留。

## 執行方式

### 本機安裝與前置條件

測試環境為本機 Docker PrestaShop + MySQL。請先準備並啟動既有測試容器，確認 Frontend 與 Admin 可連線、MySQL 可接受連線，且 PrestaShop Webservice 已啟用。本專案目前沒有納入 Docker Compose 設定，需自行準備環境；下列指令不會建立或清除 Docker 資料。

Windows PowerShell 使用 Python 3.12 建立虛擬環境並安裝相依套件與 Chromium：

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m playwright install chromium
Copy-Item .env.example .env
```

`Copy-Item` 僅適用於尚未存在本機 `.env` 的首次設定；已有 `.env` 時請保留，勿覆寫。請自行在本機填入 `.env.example` 所列的 URL、測試帳號、獨立 Registration 密碼、DB 與 API 設定，勿將敏感值寫入文件或提交 Git。Frontend / Admin 帳號須可登入；Checkout 另需既有 France Delivery Address、可購買商品、可用的 `My carrier` 與 Bank Wire。Orders Key 僅授予 `orders GET`，Products API 使用其獨立設定，DB 驗證只執行 SELECT。

Day 23 發現既有 `.venv` 的 Python 3.12 基礎執行檔路徑已失效；下次執行前需先安裝／確認 Python 3.12，重新建立可用虛擬環境並完成上述安裝。本次未重建環境或重跑測試。

安裝相依套件並準備 Playwright browser 後，可使用以下指令執行測試：

```bash
python -m pytest
```

產生 Allure raw results：

```bash
python -m pytest --alluredir=allure-results
```

目前只確認 pytest 可產生 `allure-results` raw results；本階段不要求安裝 Allure CLI，也不宣稱可直接開啟 HTML report。

歷史上曾支援失敗截圖與 Playwright Trace；目前 fixtures 不產生這些檔案，CLI 亦拒絕啟用 tracing / screenshot / video。歷史產物可能含憑證，須另行安全檢查，不能視為已清理。

也可以只執行 Admin Login smoke test：

```bash
python -m pytest tests/admin/test_admin_login.py -v
```

或只執行 Frontend Registration smoke test：

```bash
python -m pytest tests/frontend/test_registration.py -v
```

或只執行 Frontend Login smoke test：

```bash
python -m pytest tests/frontend/test_login.py -v
```

或只執行 Frontend Add to Cart smoke test：

```bash
python -m pytest tests/frontend/test_add_to_cart.py -v
```

或只執行 Frontend Checkout Shipping smoke test：

```bash
python -m pytest tests/frontend/test_checkout_shipping.py -v
```

或只執行 Frontend Checkout Payment smoke test：

```bash
python -m pytest tests/frontend/test_checkout_payment.py -v
```

或只執行 Bank Wire Order E2E test：

```bash
python -m pytest tests/e2e/test_bank_wire_order.py -v
```

或只執行 API products smoke test：

```bash
python -m pytest tests/api/test_products_api.py -v
```

## Checkout 前置條件

- 固定 Frontend 測試帳號需已存在，並透過 `.env` 的 `FRONTEND_USERNAME` 與 `FRONTEND_PASSWORD` 提供。
- 該帳號需已建立可用的 France Delivery Address。
- DB credentials 需透過 `.env` 的 `DB_HOST`、`DB_PORT`、`DB_NAME`、`DB_USER`、`DB_PASSWORD` 提供。
- Klaviyo Products API credentials 需透過 `.env` 的 `API_BASE_URL` 與 `API_KEY` 提供。
- Orders API credentials 需透過 `.env` 的 `ORDERS_API_BASE_URL` 與 `ORDERS_API_KEY` 提供，Key 只授予 `orders GET`。
- Checkout Shipping 測試不會新增 Address，也不會進入 Payment、建立 Order、做 Admin validation 或 DB validation。
- Checkout Payment 測試會選擇 `My carrier` 並進入 Payment step，只驗證 `Pay by bank wire` 可見且可選，不會建立 Order、做 Admin validation 或 DB validation。
- Bank Wire Order E2E 測試會實際建立測試訂單；每次執行都可能新增一筆測試資料。
- Bank Wire Order E2E 測試的 Frontend 與 Admin 會使用不同 `BrowserContext`，避免跨 Portal 共用登入狀態。
- DB Validation 僅使用 read-only `SELECT`，不執行 INSERT、UPDATE、DELETE、DROP、ALTER、CREATE、TRUNCATE、REPLACE 或 MERGE。
- API Automation 第一階段僅使用 read-only `GET`，不執行 POST、PUT、PATCH 或 DELETE。

## 最近一次 pytest 結果

- Bank Wire Order E2E 指定測試：`python -m pytest tests/e2e/test_bank_wire_order.py -v`
- 結果：`1 passed in 27.36s`
- API products 指定測試：`python -m pytest tests/api/test_products_api.py -v`
- 結果：`1 passed in 0.10s`
- Day 22 最終全專案測試：`python -m pytest --alluredir=allure-results -v`
- 結果：`8 passed in 71.06s (0:01:11)`
- 指定 Products Smoke 與 E2E 為 Day 21 歷史結果；Day 22 最終完整 Regression 共 8 支：8 passed、0 failed、0 skipped、0 xfailed、0 xpassed、0 errors。
- 使用專案 `.venv` Python 執行；本次完整 Regression 保留 `PLAYWRIGHT_SLOW_MO=700`，本機 `.env` 未變更。

## 環境變數

`.env.example` 定義專案需要的環境變數名稱。實際執行時請在本機 `.env` 設定對應值。

`.env` 已加入 `.gitignore`，不應提交帳號、密碼或其他敏感資訊。

### Registration 測試密碼

- 請自行在本機 `.env` 設定獨立 `REGISTRATION_TEST_PASSWORD`；`.env.example` 只提供空白欄位。
- 不共用 Frontend 固定登入或 Admin 密碼。缺少、空白或與上述登入密碼相同時，Registration fixture 明確報錯，不產生替代密碼。
- Registration 資料工廠接收 fixture 提供的密碼，保留 UUID 唯一 Email、POM 流程及既有 assertions。
- 密碼不包含在 RegistrationUser repr，也不輸出至 Log 或 Allure；所有自訂 UI contexts 停用 Playwright trace 與失敗截圖，避免 fill() 密碼參數及敏感畫面被保存。
- 指定驗證：`python -m pytest tests/frontend/test_registration.py -v`，Day 22 結果：`1 passed in 10.47s`。此測試會建立一筆 Demo 測試會員；其後 Day 22 最終完整 Regression 亦已通過。

### Playwright Browser 顯示設定

以下設定可放在本機 `.env`，只控制 Browser 顯示與操作速度：

- `PLAYWRIGHT_SLOW_MO=0`：預設快速執行；正式回歸測試建議使用 `slow_mo=0`。
- `PLAYWRIGHT_SLOW_MO=700`：本機觀察測試操作時使用，每次支援 slow_mo 的 Playwright 操作延遲 700 毫秒。
- `PLAYWRIGHT_SLOW_MO` 必須為非負整數，單位為毫秒。
- `BROWSER_MAXIMIZED=true`：headed 模式下最大化 Chromium，透過 `--start-maximized` 與 `no_viewport=True` 讓 viewport 適應視窗大小。
- `BROWSER_MAXIMIZED=false`：維持原有固定 viewport 行為。

`.env.example` 預設為 `PLAYWRIGHT_SLOW_MO=0`、`BROWSER_MAXIMIZED=false`。Frontend、Admin 與跨站 E2E 的不同 BrowserContext 都使用相同顯示設定，並保留 Context 隔離。

專案預設使用 headed 模式；可使用 `--headed` 明確指定。Headless 模式不啟用視窗最大化，仍使用固定 viewport；未指定其他 viewport 時為 1280×720：

```bash
python -m pytest --headless
```

`--headless` 與 `--headed` 不可同時使用。操作減速使用 Chromium launch 的 `slow_mo`，不加入 `time.sleep()` 或固定等待；失敗截圖與 Trace 依 Day 22 安全政策停用，Allure 測試結果仍保留。

### 測試產物敏感資訊防護（Day 22）

- 密碼輸入測試包含 Registration、Frontend Login、Admin Login、Checkout Shipping / Payment、Bank Wire E2E；其他自訂 UI context 亦採一致保守政策，不錄製 Trace 或失敗截圖。
- CLI 的 tracing、screenshot、video 必須為 off，Playwright DEBUG / PWDEBUG 不得啟用；不產生未經處理的影像或 protocol log。
- pytest 不顯示 locals，錯誤報告及 captured sections 遮蔽目前環境中的 password、API Key、Token、Secret、username 及 URL / Basic Auth 編碼形式。
- Allure 不附加原始 captured stdout / stderr / log；statusDetails 在寫檔前再次遮蔽已知敏感值。API HTTP 錯誤保留狀態；網路例外僅保留例外類型，JSON 解析錯誤不串接原始例外；不輸出 URL、Authorization Header 或原始 response body。
- targeted smoke 最終結果：Registration、Frontend Login、Admin Login、Products API 共 `4 passed in 20.73s`。
- 本機虛構哨兵失敗探測確認 Console / Allure 遮蔽且無影像產物；暫存探測已移除。其後 Day 22 最終完整 Regression 已包含 Bank Wire E2E 並通過。
- 防護不代表任意外部 logger、`-s` / live logging、未知或舊憑證及歷史產物完全安全；勿開啟 live debug logging 或手動附加未處理的敏感檔案。歷史 Allure / Trace 仍需另行安全清查。

### 安全架構維護與未來 Trace 評估

- 已移除停用後未使用的 Trace 路徑、檔名 / 附件函式、失敗截圖空函式及相關 imports；原有 Browser fixtures、Context 隔離與 Allure 測試結果保留，未增加新 hook。
- 已知敏感值長度至少 4 字元時保留原值及編碼值遮蔽；短於 4 字元且出現在診斷中時，省略整段診斷並留下安全提示，避免逐字替換破壞一般錯誤訊息。短憑證仍不會直接顯示，但相關診斷資訊會減少。
- 未來若需 Trace，應先建立獨立、匿名、完全不輸入憑證的測試及 context；確認沒有登入 cookie、Authorization Header、API Key、私人資料或敏感網路 response，再以虛構哨兵與產物檢查驗證。不能只因未呼叫 login 就判定安全。
- 現階段只做評估，不提供 Trace 開關或恢復錄製。Day 22 最終完整 Regression 已經使用者授權執行並通過，包含 Bank Wire E2E 的 Frontend → Admin → Orders API → DB，以及 Registration。

### Day 22 最終完整 Regression 驗證

- Docker PrestaShop / MySQL 容器運作，Frontend 可用性 HTTP 200；使用既有 `.venv` 執行全部 8 支正式測試。
- 指令：`python -m pytest --alluredir=allure-results -v`。
- 結果：`8 passed in 71.06s (0:01:11)`；Failed、Skipped、Xfailed、Xpassed、Errors 均為 0。
- Bank Wire E2E 只由 Frontend 建立一筆 Demo 訂單，Admin / Orders API / DB 均使用該次同一動態 Reference；Registration 正常建立一筆唯一 Email 的 Demo 會員。
- 本輪新增 8 份 Allure raw test results，未新增 screenshot / Trace / Video。新產物比對目前 `.env` 的已知敏感值及 URL / Basic Auth 編碼形式未發現洩漏；不代表歷史產物或未知憑證已清理。
- `.env` 雜湊前後一致，未修改憑證或本機 slow_mo；未執行 Git 操作或清除 Docker 資料。
