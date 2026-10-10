# 進度紀錄

## Day 1

- 建立自動化測試作品集方向。
- 確認目標技術棧：Python 3.12、Pytest、Playwright、Page Object Model、python-dotenv。

## Day 2

- 建立基礎目錄結構，包含 page objects、tests、test data 與 utils。
- 保留 `pages/common/` 作為未來共用元件放置位置，目前尚未建立共用抽象。

## Day 3

- 建立並整理根目錄設定檔：Pytest 設定、環境變數範本、Git ignore 規則、README 與進度紀錄。
- 移除空白的 `pages/siteadmin` 與 `tests/siteadmin`。

## Day 4

- 設定 `pytest.ini`：
  - 測試目錄為 `tests`
  - 註冊 `smoke`、`regression`、`e2e` markers
- 建立根目錄 `conftest.py`：
  - 使用 python-dotenv 讀取 `.env`
  - 建立 Playwright sync API fixtures
  - 每個 test 使用獨立的 `BrowserContext`
  - 必要環境變數缺少時明確 raise 錯誤

## Day 5

- 建立 Admin Login Page Object：`pages/admin/admin_login_page.py`。
- 已確認本機 PrestaShop Admin Login 頁面 locator。
- 尚未新增測試案例。

## Day 6

### 本次完成事項

- 更新 `README.md`，補充目前專案已具備的架構、目前狀態與 pytest 執行方式。
- 依照文件規則使用繁體中文記錄，並保留 Python、Pytest、Playwright、POM、Fixture、BrowserContext 等技術名詞英文。
- 實際執行 pytest 驗證目前專案狀態。

### 新增或修改的檔案

- `README.md`
- `PROGRESS.md`

### 使用的架構與設計理由

- README 以作品集展示為目的，只記錄目前已存在的 Pytest 設定、Playwright Fixture、環境變數讀取與 Admin Login Page Object。
- PROGRESS 以每日學習與開發紀錄為目的，詳細記錄本次文件更新、驗證結果、問題與下一步。
- 未在文件中寫入 `.env` 密碼、私人 Email、Token 或其他敏感資訊。

### 實際 pytest 執行結果

- 執行指令：`.\.venv\Scripts\python.exe -m pytest`
- 結果：`collected 0 items`
- 狀態：pytest exit code 為 `1`
- 說明：目前尚未建立任何測試案例，因此沒有 tests 被收集或執行。這不代表測試通過。

### 遇到的問題與解法

- 問題：專案目前只有測試框架與 Page Object，尚未建立實際 test files。
- 解法：在文件中明確標示目前 pytest 未收集到測試案例，不將結果記錄為測試成功。

### 尚未完成的項目與下一步

- 尚未建立 Admin login 測試案例。
- 尚未建立 Frontend Page Object。
- 尚未加入 Allure report、screenshot hook 或 trace。
- 下一步可建立第一個 Admin login smoke test，並再次執行 pytest 驗證。

## Day 7

### 本次完成事項

- 新增第一支 Admin Login 自動化測試。
- 測試案例：使用正確 Admin 帳號密碼登入成功。
- 測試已標記為 `@pytest.mark.smoke`。
- 測試使用既有 `page` Fixture、`env_vars` Fixture 與 `AdminLoginPage`。
- 測試使用 Playwright `expect()` 驗證登入後 Dashboard 標題可見。
- 更新 `README.md`，將目前狀態改為已具備 Admin Login smoke test。

### 新增或修改的檔案

- 新增：`tests/admin/test_admin_login.py`
- 修改：`README.md`
- 修改：`PROGRESS.md`

### locator / POM / Fixture 如何配合

- `conftest.py` 提供 `page` Fixture，讓測試取得每次獨立的 Playwright `Page`。
- `conftest.py` 提供 `env_vars` Fixture，集中讀取 `ADMIN_URL`、`ADMIN_USERNAME`、`ADMIN_PASSWORD`，避免在測試中硬編碼敏感資訊。
- `AdminLoginPage` 負責 Admin login 頁面的 UI 操作與 Locator：
  - 開啟登入頁
  - 填入 Email
  - 填入 Password
  - 點擊登入按鈕
  - 提供 Dashboard heading 作為登入成功驗證目標
- test file 只描述測試流程與商業意圖，不直接操作 Locator。

### 使用的架構與設計理由

- 使用 Page Object Model（POM）將 UI 操作集中在 `AdminLoginPage`，讓測試案例保持簡潔。
- 使用 Fixture 管理瀏覽器頁面與環境變數，降低測試重複設定。
- 使用 Playwright `expect()` 驗證畫面狀態，避免只檢查函式回傳值而沒有驗證實際 UI。
- 不使用 `sleep()`、`skip`、`xfail` 或 `try/except` 隱藏失敗。

### 實際 pytest 執行結果

- 指定測試指令：`.\.venv\Scripts\python.exe -m pytest tests/admin/test_admin_login.py -v`
- 指定測試結果：`1 passed in 2.17s`
- 全專案測試指令：`.\.venv\Scripts\python.exe -m pytest`
- 全專案測試結果：`1 passed in 2.18s`

### 遇到的問題與解法

- 問題：本次新增測試後第一次執行即通過，未遇到 locator 或登入流程失敗。
- 解法：保留既有已確認的 `AdminLoginPage` Locator，沒有降低驗證標準。

### 尚未完成的項目與下一步

- 尚未建立 Admin logout 或其他後台功能測試。
- 尚未建立 Frontend Page Object 與 Frontend 測試案例。
- 尚未加入 Allure report、screenshot hook 或 trace。
- 下一步可新增 Admin logout 或 Dashboard smoke test，擴充登入後的基本驗證範圍。

## Day 8

### 本次完成事項

- 新增 Frontend Registration Page Object。
- 新增第一支 Frontend Registration smoke test。
- 測試案例：使用有效資料成功註冊新會員。
- 測試已標記為 `@pytest.mark.smoke`。
- 測試使用既有 `page` Fixture 與 `env_vars` Fixture。
- 測試使用 Playwright `expect()` 驗證註冊成功後的登入狀態。
- 更新 `README.md`，加入 Frontend Registration smoke test 狀態與執行方式。

### 新增或修改的檔案

- 新增：`pages/frontend/register_page.py`
- 新增：`testdata/registration_data.py`
- 新增：`tests/frontend/test_registration.py`
- 修改：`README.md`
- 修改：`PROGRESS.md`

### 測試資料產生策略

- 使用 `uuid4()` 產生唯一 Email，格式為測試專用的 `qa.auto.<unique>@example.com`。
- 不使用私人 Email。
- First name / Last name 使用固定測試資料：`QA` / `Automation`。
- Password 使用符合目前 PrestaShop 密碼規則與強度檢查的測試密碼。

### locator / POM / Fixture 如何配合

- `conftest.py` 提供 `page` Fixture，讓每次測試都有獨立的 Playwright `Page` 與 `BrowserContext`。
- `conftest.py` 提供 `env_vars` Fixture，從 `.env` 讀取 `FRONTEND_URL`，避免在 test file 硬編碼 localhost URL。
- `RegisterPage` 負責 Frontend Registration 的 UI 操作與 Locator：
  - 開啟 Frontend 首頁
  - 進入 Sign in
  - 進入 Create account / Registration
  - 選擇 Social title
  - 填寫 First name、Last name、Email、Password
  - 勾選必要的 Privacy / Terms checkbox
  - 送出 Registration
  - 提供 `Sign out`、`Your account` 與會員名稱作為登入狀態驗證介面
- `tests/frontend/test_registration.py` 只負責準備測試資料、呼叫 POM 流程與描述商業意圖。

### 使用的架構與設計理由

- 使用 Page Object Model（POM）集中管理 Frontend Registration 頁面的 Locator 與 UI 操作。
- 使用 test data helper 產生唯一 Email，避免資料庫已有會員造成測試不穩定。
- 使用 Playwright `expect()` 驗證明確登入狀態，不只檢查 URL。
- 不使用 `sleep()`、XPath、`skip`、`xfail`、DB validation、Admin validation、Allure、screenshot hook 或 trace。

### 實際 pytest 執行結果

- 指定測試指令：`.\.venv\Scripts\python.exe -m pytest tests/frontend/test_registration.py -v`
- 指定測試結果：`1 passed in 2.92s`
- 全專案測試指令：`.\.venv\Scripts\python.exe -m pytest`
- 全專案測試結果：`2 passed in 4.14s`

### 遇到的問題與解法

- 問題：Registration 頁面的 `Email` 與 `Password` accessible locator 不是唯一，會與頁尾 newsletter 或顯示密碼按鈕衝突。
- 解法：依實際 DOM 使用已確認的欄位 id：`#field-email` 與 `#field-password`。
- 問題：原先使用的測試密碼未符合強度要求，被 PrestaShop 密碼強度檢查拒絕。
- 解法：改用較強的固定測試密碼，並實際確認可以完成註冊。
- 問題：Header 的 `Sign in` role locator 有多個匹配。
- 解法：依實際 DOM 使用 Header 中唯一的 `a[aria-label="Sign in"]`。

### 尚未完成的項目與下一步

- 尚未建立 Frontend login、logout 或會員中心相關測試。
- 尚未建立 Frontend 商品、購物車或結帳流程測試。
- 尚未加入 Allure report、screenshot hook 或 trace。
- 下一步可新增 Frontend Login smoke test，驗證已存在會員登入流程。

## Day 9

### 本次完成事項

- 更新 `env_vars` Fixture，支援 `FRONTEND_USERNAME` 與 `FRONTEND_PASSWORD`。
- 更新 `.env.example`，加入 Frontend Login 測試帳號欄位名稱。
- 新增 Frontend Login Page Object。
- 新增 Frontend Login smoke test。
- 測試案例：使用有效 Frontend 測試帳號登入成功。
- 測試已標記為 `@pytest.mark.smoke`。
- 測試使用 Playwright `expect()` 驗證登入成功後的明確登入狀態。
- 更新 `README.md`，加入 Frontend Login smoke test 狀態與執行方式。

### 新增或修改的檔案

- 新增：`pages/frontend/login_page.py`
- 新增：`tests/frontend/test_login.py`
- 修改：`conftest.py`
- 修改：`.env.example`
- 修改：`README.md`
- 修改：`PROGRESS.md`

### locator / POM / Fixture 如何配合

- `conftest.py` 的 `env_vars` Fixture 統一提供 `FRONTEND_URL`、`FRONTEND_USERNAME`、`FRONTEND_PASSWORD`。
- `LoginPage` 負責 Frontend Login 的 UI 操作與 Locator：
  - 開啟 Frontend 首頁
  - 點擊 Header 的 Sign in
  - 填寫 Email
  - 填寫 Password
  - 點擊 Sign in
  - 提供 `Sign out` 與 `Your account` 作為登入成功驗證介面
- `tests/frontend/test_login.py` 只負責取得測試資料、呼叫 POM 流程與驗證結果，不直接操作 Locator。

### 使用的架構與設計理由

- 使用 Page Object Model（POM）集中管理 Login 頁面的 Locator 與 UI 操作。
- 使用 Fixture 讀取固定 Frontend 測試帳號，避免在 Python 內硬編碼帳密。
- 使用 Playwright `expect()` 驗證登入後 UI 狀態，不只檢查 URL。
- 不使用 `sleep()`、`skip`、`xfail`、`try/except`、DB validation、Admin validation、Allure、trace 或 screenshot hook。

### 實際 pytest 執行結果

- 指定測試指令：`.\.venv\Scripts\python.exe -m pytest tests/frontend/test_login.py -v`
- 指定測試結果：`1 passed in 2.30s`
- 全專案測試指令：`.\.venv\Scripts\python.exe -m pytest`
- 全專案測試結果：`3 passed in 5.71s`

### 遇到的問題與解法

- 問題：`Email` 與 `Password` accessible locator 不是唯一，會與頁尾 newsletter 或顯示密碼按鈕衝突。
- 解法：依實際 Login DOM 使用已確認且唯一的 `#field-email` 與 `#field-password`。
- 問題：Header 的 `Sign in` role locator 有多個匹配。
- 解法：依實際 DOM 使用 Header 中唯一的 `a[aria-label="Sign in"]`。
- 問題：一開始尚未有可重複使用的 Frontend 測試帳號資訊。
- 解法：在固定測試帳號建立後，透過 `.env` 與 `env_vars` Fixture 讀取，不在程式碼或文件寫入帳密。

### 尚未完成的項目與下一步

- 尚未建立 Frontend logout 或會員中心相關測試。
- 尚未建立 Frontend 商品、購物車或結帳流程測試。
- 尚未加入 Allure report、screenshot hook 或 trace。
- 下一步可新增 Frontend Logout smoke test 或會員中心基本驗證。

## Day 10

### 本次完成事項

- 新增 Frontend Product Page Object。
- 新增 Frontend Cart Page Object。
- 新增 Frontend Add to Cart smoke test。
- 測試案例：使用者可以從 Frontend 選擇商品並成功加入購物車。
- 測試已標記為 `@pytest.mark.smoke`。
- 測試使用 Playwright `expect()` 驗證 Cart 中商品名稱可見與商品數量正確。
- 更新 `README.md`，加入 Frontend Add to Cart smoke test 狀態與執行方式。

### 新增或修改的檔案

- 新增：`pages/frontend/product_page.py`
- 新增：`pages/frontend/cart_page.py`
- 新增：`tests/frontend/test_add_to_cart.py`
- 修改：`README.md`
- 修改：`PROGRESS.md`

### 測試流程

- 開啟 Frontend 首頁。
- 從首頁進入 demo shop 中已存在的商品：`The best is yet to come' Framed poster`。
- 在商品頁點擊 Add to cart。
- 從加入購物車成功 modal 進入 Cart 頁。
- 驗證 Cart 中商品名稱可見。
- 驗證 Cart 中商品數量為 `1`。

### locator / variant 問題與解法

- 問題：商品頁有 related products，導致 Add to cart button 與 quantity input 在頁面中有多個匹配。
- 解法：使用實際 DOM 中主商品 Add to cart button 的 accessible name：`Add to cart The best is yet to come' Framed poster`。
- 問題：商品有 Dimension variant，預設選項為 `40x60cm`，且本案例不需要改變 variant。
- 解法：保留預設 variant，不猜測或硬選 Size / Color。
- 問題：Cart 頁有 featured products，商品名稱與 quantity aria label 會在推薦商品區重複。
- 解法：`CartPage` 將驗證範圍限制在 `.cart__overview`，只檢查實際 Cart 商品清單。
- 問題：加入購物車成功 modal 的 `Proceed to checkout` 文字實際連到 Cart summary 頁 `/cart?action=show`。
- 解法：僅使用它進入 Cart 頁，不進行 Checkout、Payment 或 Order 流程。

### 使用的架構與設計理由

- 使用 Page Object Model（POM）拆分 Product 與 Cart 職責。
- `ProductPage` 負責開啟 Frontend、進入商品頁、加入購物車與從成功 modal 進入 Cart。
- `CartPage` 負責提供 Cart 商品名稱與數量驗證介面。
- test file 只描述 add-to-cart 商業流程，不直接操作 Locator。
- 不使用 `sleep()`、XPath、`skip`、`xfail`、DB validation、Admin validation、Allure、trace 或 screenshot hook。

### 實際 pytest 執行結果

- 指定測試指令：`.\.venv\Scripts\python.exe -m pytest tests/frontend/test_add_to_cart.py -v`
- 指定測試結果：`1 passed in 2.69s`
- 全專案測試指令：`.\.venv\Scripts\python.exe -m pytest`
- 全專案測試結果：`4 passed in 7.47s`

### 遇到的問題與解法

- 問題：全頁搜尋商品名稱會同時命中 Cart 商品與 featured products。
- 解法：Cart 驗證固定從 `.cart__overview` 內查找商品名稱與 quantity。
- 問題：商品頁存在多個 Add to cart button。
- 解法：使用帶商品名稱的 role locator，確認只匹配主商品 Add to cart button。

### 尚未完成的項目與下一步

- 尚未建立 Checkout、Payment 或 Order 測試。
- 尚未建立 Cart 更新數量或移除商品測試。
- 尚未加入 Allure report、screenshot hook 或 trace。
- 下一步可新增 Cart update quantity smoke test，或建立 Checkout 前置頁面的驗證案例。

## Day 11

### 本次完成事項

- 新增 Frontend Checkout Page Object。
- 新增 Frontend Checkout Shipping smoke test。
- 測試案例：`test_checkout_reaches_shipping_successfully`。
- 測試已標記為 `@pytest.mark.smoke`。
- 測試使用既有 `LoginPage`、`ProductPage`、`CartPage`、`page` Fixture 與 `env_vars` Fixture。
- 測試使用固定 Frontend 測試帳號登入，加入既有穩定商品，從 Cart 進入 Checkout。
- 測試使用該帳號已存在的 France Delivery Address，不在測試中新增 Address。
- 測試進入 Shipping Method step 後，使用 Playwright `expect()` 驗證至少一個未 disabled 的 Shipping method 顯示。
- 更新 `README.md`，加入 Checkout Shipping smoke test 狀態、執行方式、前置條件與 pytest 結果。

### 新增或修改的檔案

- 新增：`pages/frontend/checkout_page.py`
- 新增：`tests/frontend/test_checkout_shipping.py`
- 修改：`pages/frontend/cart_page.py`
- 修改：`README.md`
- 修改：`PROGRESS.md`

### CheckoutPage 設計

- `CheckoutPage` 負責 Checkout 專屬 Locator 與操作：
  - 已選取 Delivery Address：`#checkout-addresses-step article.address-card.selected address`
  - Addresses step Continue button：`#checkout-addresses-step button[name="confirm-addresses"]`
  - Shipping Method heading：`#checkout-delivery-step h1`
  - 可用 Shipping method：`#checkout-delivery-step .delivery-option__item:has(input[name^="delivery_option"]:not([disabled]))`
- `CartPage` 新增 `proceed_to_checkout()`，讓 test file 不直接操作 Cart checkout locator。
- test file 只描述登入、加入商品、進 Cart、進 Checkout、確認 Address 與 Shipping method 的測試流程。

### Address / Shipping 前置條件

- 固定 Frontend 測試帳號已手動建立可用的 France Delivery Address。
- 測試會驗證目前選取的 Delivery Address 內容包含 `France`。
- 測試不會新增 Address。
- 測試只到 Shipping Method step，不做 Payment、Order、Admin validation 或 DB validation。

### 實際 DOM 確認結果

- Cart 頁 `Proceed to checkout` 是 role `link`，文字為 `Proceed to checkout`，href 指向 `/order`。
- Checkout Addresses step 使用 `#checkout-addresses-step`，目前已選取的 address card class 包含 `selected`。
- Addresses step Continue button 實際文字為 `Continue to Shipping Method`，button name 為 `confirm-addresses`。
- Shipping step 使用 `#checkout-delivery-step`，標題為 `Shipping Method`。
- Shipping methods 實際 DOM 為 `.delivery-option__item js-delivery-option`，不是 `.delivery-option`。
- 目前 France address 下實際可用 Shipping method 包含 `Click and collect` 與 `My carrier`，radio input 未 disabled。

### 使用的架構與設計理由

- 優先重用既有 Page Object 與 Fixture，避免在測試中重複 locator。
- Checkout locator 集中在 `CheckoutPage`，維持 Page Object Model。
- 使用 Playwright `expect()` 驗證 UI 狀態。
- 不使用 `sleep()`、XPath、`skip`、`xfail` 或 `try/except` 隱藏失敗。

### 實際 pytest 執行結果

- 第一次直接執行指令：`python -m pytest tests/frontend/test_checkout_shipping.py -v`
- 結果：失敗，原因是系統 `python` 未安裝 `playwright`，在匯入 `conftest.py` 時出現 `ModuleNotFoundError: No module named 'playwright'`。
- 解法：啟用專案 `.venv` 後再用同一個 `python -m pytest` 指令執行。
- Checkout Shipping 指定測試指令：`python -m pytest tests/frontend/test_checkout_shipping.py -v`
- Checkout Shipping 指定測試結果：`1 passed in 4.54s`
- 全專案測試指令：`python -m pytest`
- 全專案測試結果：`5 passed in 11.37s`

### 遇到的問題與解法

- 問題：未啟用 `.venv` 時，系統 `python` 缺少 `playwright`。
- 解法：啟用專案 `.venv` 後執行測試。
- 問題：新增測試時尚未有 `CheckoutPage`，指定測試在 collection 階段因缺少 module 失敗。
- 解法：新增 `pages/frontend/checkout_page.py`，只放 Checkout 專屬 locator 與動作。
- 問題：Shipping method 的實際 DOM class 不是 `.delivery-option`。
- 解法：依實際 DOM 改用 `.delivery-option__item`，並限制為包含未 disabled `delivery_option` radio input 的項目。
- 問題：Shipping method 實際可用數量可能依後台設定改變。
- 解法：測試不硬寫固定數量，只驗證至少第一個未 disabled Shipping method 可見。

### 尚未完成的項目與下一步

- 尚未建立 Payment 或 Order 測試。
- 尚未建立 Checkout address 新增、修改或刪除測試。
- 尚未加入 Allure report、screenshot hook 或 trace。

## Day 12

### 本次完成事項

- 擴充既有 `CheckoutPage`，加入 Shipping method 選擇、Shipping Continue、Payment step 與 Bank Wire payment method 驗證介面。
- 新增 Frontend Checkout Payment smoke test。
- 測試案例：`test_checkout_reaches_payment_successfully`。
- 測試已標記為 `@pytest.mark.smoke`。
- 測試使用既有 `LoginPage`、`ProductPage`、`CartPage`、`CheckoutPage`、`page` Fixture 與 `env_vars` Fixture。
- 測試使用固定 Frontend 測試帳號登入，加入既有穩定商品，從 Cart 進入 Checkout。
- 測試確認既有 France Delivery Address，進入 Shipping Method，選擇 `My carrier`，再進入 Payment step。
- 測試驗證實際 UI 顯示的 `Pay by bank wire` payment method 可見且可選取。
- 本次未勾選 Terms、未 Place order、未建立 Order、未做 Admin validation 或 DB validation。
- 更新 `README.md`，加入 Checkout Payment smoke test 狀態、執行方式、前置條件與 pytest 結果。

### 新增或修改的檔案

- 新增：`tests/frontend/test_checkout_payment.py`
- 修改：`pages/frontend/checkout_page.py`
- 修改：`README.md`
- 修改：`PROGRESS.md`

### CheckoutPage 擴充內容

- `select_shipping_method(shipping_method_name)`：選擇指定 Shipping method。
- `continue_from_shipping()`：從 Shipping Method step 進入 Payment step。
- `payment_step_heading`：提供 Payment step 標題驗證。
- `bank_wire_payment_method`：提供 `Pay by bank wire` 顯示文字驗證。
- `bank_wire_payment_method_input`：提供 Bank Wire radio input 驗證。
- `select_bank_wire_payment_method()`：選取 Bank Wire radio，但不送出訂單。

### 實際 DOM 確認結果

- Shipping step 的 `My carrier` 位於 `#checkout-delivery-step .delivery-option__item`。
- `My carrier` radio input name 為 `delivery_option[9]`，id 為 `delivery_option_2`，未 disabled。
- Shipping Continue button 的 name 為 `confirmDeliveryOption`，實際文字為 `Continue to Payment`。
- Payment step 使用 `#checkout-payment-step`，標題為 `Payment`。
- Bank Wire 實際 UI 顯示文字為 `Pay by bank wire`。
- Bank Wire radio input 使用 `data-module-name="ps_wirepayment"`，id 為 `payment-option-1`，未 disabled。

### Bank Wire 驗證方式

- 先驗證 `Pay by bank wire` 文字可見。
- 再選取 Bank Wire radio input。
- 最後使用 Playwright `expect()` 驗證該 radio input 已 checked。
- 測試不勾選 Terms，也不觸發 Place order。

### 實際 pytest 執行結果

- Checkout Payment 指定測試指令：`python -m pytest tests/frontend/test_checkout_payment.py -v`
- Checkout Payment 指定測試結果：`1 passed in 4.92s`
- 全專案測試指令：`python -m pytest`
- 全專案測試結果：`6 passed in 14.68s`
- 執行環境：已啟用專案 `.venv` 後執行。

### 遇到的問題與解法

- 問題：新增測試時 `CheckoutPage` 尚未提供 `select_shipping_method()`，指定測試在執行到 Shipping step 時失敗。
- 解法：依實際 DOM 擴充 `CheckoutPage`，新增 Shipping method selector、Shipping Continue button 與 Payment step locator。
- 問題：需求提到 Bank Wire，但實際 Payment UI 文字不是 `Bank Wire`，而是 `Pay by bank wire`。
- 解法：依目前 DOM 顯示文字使用 `Pay by bank wire` 驗證，並用 `data-module-name="ps_wirepayment"` 鎖定 Bank Wire radio input。
- 問題：只驗證 payment method 可見不足以確認可選。
- 解法：在不送出訂單的前提下選取 Bank Wire radio input，並驗證 input 已 checked。

### 尚未完成的項目與下一步

- 尚未建立 Place order 或 Order success 測試。
- 尚未建立 Payment terms validation 測試。
- 尚未做 Admin validation 或 DB validation。
- 尚未加入 Allure report、screenshot hook 或 trace。

## Day 13

### 本次完成事項

- 新增第一支真正建立資料的 E2E Test。
- 新增 Bank Wire Order E2E test：`test_customer_can_place_bank_wire_order_successfully`。
- 測試已標記為 `@pytest.mark.e2e`，未標記 smoke。
- 測試使用既有 `LoginPage`、`ProductPage`、`CartPage`、`CheckoutPage`、`page` Fixture 與 `env_vars` Fixture。
- 新增 `OrderConfirmationPage`，負責 Order Confirmation 頁面的成功訊息、Order Reference 與 Payment method 驗證。
- 擴充 `CheckoutPage`，加入 Terms checkbox 與 Place Order button。
- 更新 `README.md`，加入 Bank Wire Order E2E 狀態、執行方式與資料副作用說明。

### 新增或修改的檔案

- 新增：`tests/e2e/test_bank_wire_order.py`
- 新增：`pages/frontend/order_confirmation_page.py`
- 修改：`pages/frontend/checkout_page.py`
- 修改：`README.md`
- 修改：`PROGRESS.md`

### Order Flow

- 使用固定 Frontend 測試帳號登入。
- 加入既有穩定商品：`The best is yet to come' Framed poster`。
- 從 Cart 進入 Checkout。
- 驗證既有 Delivery Address 包含 `France`。
- 進入 Shipping Method。
- 選擇 `My carrier`。
- 進入 Payment。
- 選擇 Bank Wire 對應的 `Pay by bank wire` radio input。
- 勾選必要 Terms and Conditions。
- 點擊 Place Order，建立真實測試訂單。
- 進入 Order Confirmation。

### Order Reference 如何取得

- Order Reference 從本次實際建立的 Order Confirmation 頁面取得。
- 實際 DOM 中 Order details 區塊為 `.order-confirmation__details`。
- Reference 位於其中包含 `Order reference:` 的 `li`。
- `OrderConfirmationPage.order_reference` 會讀取該列文字，切出冒號後的 reference。
- 測試驗證 reference 不是空字串，且符合目前 UI 顯示的 uppercase alphanumeric 形式。
- 文件不記錄任何實際 Order Reference。

### Confirmation 如何驗證

- 成功訊息使用 `.alert.alert-success` 中的 heading `Your order is confirmed` 驗證。
- Bank Wire 付款資訊使用 Payment information 卡片中的實際 UI 文字 `Pay by Bank Wire` 驗證。
- Order details 中的 Order Reference locator 必須可見。
- 本階段不驗證固定 Total，避免把價格與運費變動綁死在 E2E 測試中。

### 實際 DOM 確認結果

- Terms checkbox：`#checkout-payment-step input[name="conditions_to_approve[terms-and-conditions]"]`
- Place Order button：`#payment-confirmation button[type="submit"]`
- Order Confirmation success message：`.alert.alert-success` 內的 `Your order is confirmed`
- Payment information 實際文字：`Pay by Bank Wire`
- Order details 區塊：`.order-confirmation__details`
- Order details 付款方式實際文字：`Payment method: Bank transfer`

### 實際 pytest 執行結果

- Bank Wire Order E2E 指定測試指令：`python -m pytest tests/e2e/test_bank_wire_order.py -v`
- Bank Wire Order E2E 指定測試結果：`1 passed in 5.50s`
- 全專案測試指令：`python -m pytest`
- 全專案測試結果：`7 passed in 19.34s`
- 執行環境：已啟用專案 `.venv` 後執行。

### 遇到的問題與解法

- 問題：新增測試時尚未有 `OrderConfirmationPage`，指定測試在 collection 階段因缺少 module 失敗。
- 解法：新增 `pages/frontend/order_confirmation_page.py`，將確認頁 locator 與 reference 擷取集中在 Page Object。
- 問題：一開始猜測的 `#content-hook_order_confirmation` 不存在於目前 Order Confirmation DOM。
- 解法：依實際 DOM 改用 `.alert.alert-success` 驗證成功訊息，並使用 `.order-confirmation__details` 取得 Order details。
- 問題：Payment step 勾選 `My carrier` 後若太快繼續，可能停留在 Shipping step。
- 解法：測試流程保留明確 Payment heading 驗證；既有 Page Object 流程在實際 pytest 中可穩定進入 Payment。
- 問題：Bank Wire 在 Payment step、Payment information 與 Order details 使用不同實際文字。
- 解法：Payment step 使用 `Pay by bank wire`，Confirmation 的 Payment information 使用 `Pay by Bank Wire`，Order details 則記錄為 `Bank transfer`，測試選擇最能代表 Bank Wire 的 Payment information 文字驗證。

### 資料副作用

- 這是第一支會真正建立測試資料的 E2E Test。
- 每次執行都可能新增一筆測試訂單，這是目前 Demo Environment 可接受的行為。
- 未使用 mock、route intercept 或 DB 操作避開 Place order。

### 尚未完成的項目與下一步

- 下一步為 Admin Order validation。
- DB validation 尚未開始。
- 尚未加入 MySQL library。
- 尚未加入 Allure report、screenshot hook 或 trace。

## Day 14

### 本次完成事項

- 擴充既有 Bank Wire Order E2E，加入 Admin Back Office validation。
- E2E 流程成為 Frontend 建立 Order、取得 Order Reference，再使用 Admin 驗證同一筆 Order。
- 新增 Admin 專用 `BrowserContext` 與 `admin_page` Fixture，確保 Frontend / Admin Portal session 隔離。
- 新增 `AdminOrdersPage`，負責 Orders 頁進入、Reference 搜尋、結果列定位、開啟訂單詳細頁與 Admin 欄位驗證 locator。
- 更新 `README.md`，說明 Bank Wire Order E2E 已包含 Admin validation 與不同 Portal 使用獨立 `BrowserContext`。

### 新增或修改的檔案

- 新增：`pages/admin/admin_orders_page.py`
- 修改：`conftest.py`
- 修改：`tests/e2e/test_bank_wire_order.py`
- 修改：`README.md`
- 修改：`PROGRESS.md`

### Frontend → Admin cross-portal E2E

- Frontend 使用既有 `page` Fixture 建立訂單。
- Frontend 完成 Order Confirmation 後，從確認頁取得本次動態 Order Reference。
- Admin 使用新的 `admin_page` Fixture，背後是獨立 `admin_browser_context`。
- Admin 登入使用既有 `AdminLoginPage`，帳號密碼仍由 `env_vars` 讀取。
- Admin Orders validation 使用 Frontend 產生的同一個 Order Reference，不另外建立訂單，也不依賴最新第一筆訂單。

### BrowserContext 隔離

- `page` Fixture 繼續使用既有 `browser_context`，供 Frontend 流程使用。
- 新增 `admin_browser_context` Fixture，每次測試建立獨立 Admin `BrowserContext`，測試結束後 close。
- 新增 `admin_page` Fixture，從 Admin 專用 context 建立 Page。
- 這避免 Frontend 已登入狀態被 Admin Portal 共用。

### Order Reference 如何跨 Portal 傳遞

- `OrderConfirmationPage.order_reference` 從 Frontend Order Confirmation 頁 `.order-confirmation__details` 中包含 `Order reference:` 的列取得 reference。
- 測試將該 reference 存入本地變數 `order_reference`。
- 同一個 `order_reference` 被傳入 `AdminOrdersPage.search_order_reference(order_reference)`。
- Admin validation 全部依此 reference 定位，不硬編碼實際訂單編號。

### Admin Orders 如何定位同一筆 Order

- 進入 Orders 頁：Back Office 中 role link `Orders`。
- 清除保留 filter：`button[name="order[actions][reset]"]`。
- Reference 搜尋欄位：`#order_reference`。
- Search button：`button[name="order[actions][search]"]`。
- 搜尋結果列：`#order_grid_table tbody tr` 中包含 `.column-reference` 且文字符合本次 reference 的 row。
- 開啟詳細頁：搜尋結果列中的 `a.grid-view-row-link`。

### 實際驗證欄位

- Admin 找得到同一筆 Order Reference：搜尋結果列 `.column-reference` 完全等於 Frontend 產生的 reference。
- 詳細頁 Reference：`#orderBasicInfo` 中的 reference 文字完全相同。
- Customer：`#customerCard h2` 包含固定測試會員名稱 `QA Automation`。
- Payment：`#orderBasicInfo` 中顯示 `Bank transfer`。
- Order status：第一個 `.card-details` 中顯示 `Awaiting bank wire payment`。

### 實際 DOM 確認結果

- Orders 頁主標題：role heading `Orders` exact。
- Orders grid：`#order_grid_table`。
- Orders grid Reference column：`.column-reference`。
- Orders grid Customer column 實際顯示格式為縮寫加姓氏，例如 `Q. Automation`；詳細頁 Customer 卡片顯示完整 `QA Automation`，因此 Customer 驗證放在詳細頁。
- 訂單詳細頁標題格式包含 order id、reference 與 customer，例如 `Order #... <reference> from QA Automation`。
- Basic information 卡片 id 為 `#orderBasicInfo`。
- Customer 卡片 id 為 `#customerCard`。

### 實際 pytest 執行結果

- Bank Wire Order E2E 指定測試指令：`python -m pytest tests/e2e/test_bank_wire_order.py -v`
- Bank Wire Order E2E 指定測試結果：`1 passed in 10.83s`
- 全專案測試指令：`python -m pytest`
- 全專案測試結果：`7 passed in 25.18s`
- 執行環境：已啟用專案 `.venv` 後執行。

### 遇到的問題與解法

- 問題：新增測試先引用 `AdminOrdersPage`，指定測試在 collection 階段因缺少 module 失敗。
- 解法：新增 `pages/admin/admin_orders_page.py`，集中管理 Back Office Orders locator 與操作。
- 問題：Orders grid 會保留先前搜尋 filter，Reference 欄位可能已有舊值。
- 解法：搜尋本次 reference 前若 grid reset button 存在就先清除 filter；若沒有保留 filter，直接填入本次 Order Reference 搜尋。
- 問題：完整 pytest 中 Admin Orders grid 沒有保留 filter 時不渲染 reset button，強制點擊會 timeout。
- 解法：`AdminOrdersPage.search_order_reference()` 改為先確認 reset button 存在才點擊，搜尋與驗證仍依本次 Order Reference 精準定位。
- 問題：Orders grid Customer 欄位顯示縮寫格式，不適合作為固定會員完整名稱驗證。
- 解法：進入訂單詳細頁後，使用 `#customerCard h2` 驗證完整 `QA Automation`。
- 問題：不能使用 Frontend context 登入 Admin。
- 解法：新增 Admin 專用 context/page fixture，測試同時接收 `page` 與 `admin_page`。

### 尚未完成的項目與下一步

- 下一步為 DB validation。
- DB validation 尚未開始。
- 尚未加入 MySQL library。
- 尚未加入 Allure report、screenshot hook 或 trace。

## Day 15

### 本次完成事項

- 擴充既有 Bank Wire Order E2E，加入 MySQL DB Validation。
- 完成第一條 Frontend → Admin → DB 完整 E2E。
- 安裝 MySQL Python driver：`mysql-connector-python==26.7.0`。
- 更新 `requirements.txt`，保留既有 dependency 並新增 MySQL driver。
- 更新 `.env.example`，加入 `DB_HOST`、`DB_PORT`、`DB_NAME`、`DB_USER`、`DB_PASSWORD`，不包含真實密碼。
- 更新本機 `.env`，加入 DB connection 設定；不提交、不記錄密碼。
- 擴充 `env_vars` Fixture，將 DB 設定列為必要環境變數，缺少時會明確指出變數名稱。
- 新增 `utils/db_helper.py`，提供 read-only SELECT DB helper。

### 新增或修改的檔案

- 新增：`utils/db_helper.py`
- 修改：`tests/e2e/test_bank_wire_order.py`
- 修改：`conftest.py`
- 修改：`requirements.txt`
- 修改：`.env.example`
- 修改：本機 `.env`
- 修改：`README.md`
- 修改：`PROGRESS.md`

### MySQL driver

- 使用套件：`mysql-connector-python==26.7.0`。
- 安裝在專案 `.venv`。
- 因本機 Docker MySQL 使用 localhost 連線，DB helper 明確設定 `ssl_disabled=True`，避免 MySQL connector 對本機 TLS cipher 輸出 deprecation warning。

### DB helper 架構

- `DatabaseHelper` 位於 `utils/db_helper.py`。
- 使用 `mysql.connector` 建立 connection。
- 使用 dictionary cursor，讓測試用欄位名稱讀取結果。
- 提供：
  - `connect()`
  - `close()`
  - `fetch_one()`
  - `fetch_all()`
  - `fetch_order_by_reference(order_reference)`
  - `fetch_order_details(order_id)`
- Helper 會檢查 query 必須以 `SELECT` 開頭。
- Helper 禁止包含 `INSERT`、`UPDATE`、`DELETE`、`DROP`、`ALTER`、`CREATE`、`TRUNCATE`、`REPLACE`、`MERGE`。
- 本 Portfolio 的 DB validation 維持 read-only。

### DB connection 如何管理

- `conftest.py` 新增 `db_helper` Fixture。
- Fixture 從 `env_vars` 取得 DB connection 設定。
- Fixture 建立 `DatabaseHelper`、呼叫 `connect()`，並在 `finally` 呼叫 `close()`。
- 即使測試中途失敗，也會關閉 DB connection。

### 使用哪些 table

- `ps_orders`
- `ps_customer`
- `ps_order_state_lang`
- `ps_lang`
- `ps_order_detail`

### 使用哪些 SELECT

- 查詢 `INFORMATION_SCHEMA.COLUMNS` 確認實際 table / column。
- 查詢 `ps_lang` 確認目前 active language。
- 查詢 `ps_order_state_lang` 確認實際 status 文字。
- E2E validation 使用 `ps_orders` 依 `reference = order_reference` 查詢本次訂單。
- E2E validation JOIN `ps_customer` 驗證 customer。
- E2E validation JOIN `ps_order_state_lang` 與 active `ps_lang` 驗證 order status。
- E2E validation 使用本次查到的 `id_order` 查詢 `ps_order_detail` 驗證商品明細。

### Order Reference 如何從 Frontend 傳到 Admin 再傳到 DB

- Frontend Order Confirmation 從 `.order-confirmation__details` 中擷取本次 `order_reference`。
- Admin Orders 使用同一個 `order_reference` 填入 `#order_reference` 搜尋。
- DB validation 使用同一個 `order_reference` 查詢 `ps_orders.reference`。
- 測試不硬編碼 Order Reference、不依賴 DB 最新一筆資料、不建立第二筆 Order 供 Admin 或 DB 驗證。

### DB 實際驗證欄位

- `ps_orders.reference`：完全等於 Frontend 取得的 Order Reference。
- `ps_customer.firstname`：`QA`。
- `ps_customer.lastname`：`Automation`。
- `ps_orders.payment`：`Bank transfer`。
- `ps_order_state_lang.name`：`Awaiting bank wire payment`。
- `ps_orders.total_paid`：大於 `0`。
- `ps_orders.id_customer`：大於 `0`。
- `ps_orders.current_state`：大於 `0`。
- `ps_order_detail.product_name`：包含穩定商品 `The best is yet to come' Framed poster`。
- `ps_order_detail.product_quantity`：等於 `1`。
- `ps_order_detail.product_price`：大於 `0`。

### 實際 schema 確認結果

- `ps_orders` 包含 `id_order`、`reference`、`payment`、`total_paid`、`id_customer`、`current_state`。
- `ps_customer` 包含 `id_customer`、`firstname`、`lastname`。
- `ps_order_state_lang` 包含 `id_order_state`、`id_lang`、`name`。
- `ps_lang` 目前 active language 為 English，`id_lang = 1`。
- `ps_order_detail` 包含 `id_order`、`product_name`、`product_quantity`、`product_price`。

### 實際 pytest 執行結果

- Bank Wire Order E2E 指定測試指令：`python -m pytest tests/e2e/test_bank_wire_order.py -v`
- Bank Wire Order E2E 指定測試結果：`1 passed in 12.58s`
- 全專案測試指令：`python -m pytest`
- 全專案測試結果：`7 passed in 24.82s`
- 執行環境：已啟用專案 `.venv` 後執行。

### 遇到的問題與解法

- 問題：專案原本沒有 MySQL driver。
- 解法：在 `.venv` 安裝 `mysql-connector-python`，並更新 `requirements.txt`。
- 問題：`.env` 原本沒有 DB connection 設定。
- 解法：依本機 Docker MySQL container 設定補上 DB env keys；文件只記錄變數名稱，不記錄密碼。
- 問題：需要驗證 status，但不應猜 `id_lang`。
- 解法：先查 `ps_lang` 確認 active language，再在 SELECT 中以 active language 對應 `ps_order_state_lang`。
- 問題：第一次 DB E2E 通過時 MySQL connector 對本機 TLS cipher 輸出 deprecation warning。
- 解法：本機 DB helper 連線設定 `ssl_disabled=True`，重跑後輸出乾淨。
- 問題：完整 pytest 中 `test_checkout_reaches_payment_successfully` 偶發停在 Shipping Method，原因是選擇 `My carrier` 後 `selectDeliveryOption` AJAX 尚未完成就點擊 Continue。
- 解法：`CheckoutPage.select_shipping_method()` 在未選取目標 shipping method 時等待 `action=selectDeliveryOption` response，並驗證 radio checked 與 Continue button enabled；若帳號已記住 `My carrier`，則直接驗證已選取狀態。

### 尚未完成的項目與下一步

- Frontend → Admin → DB 完整 E2E 已完成。
- 下一步可補充 DB validation 的更多欄位，例如 carrier、address 或 total consistency。
- 尚未加入 Allure report、screenshot hook 或 trace。

## Day 16

### 本次完成事項

- 整合 Allure raw results。
- 新增 Test Failure 自動截圖並附加到 Allure。
- 修正 `README.md` 中「DB 已完成但仍寫尚未加入 DB」的矛盾。
- 保留既有正式 Business Test Case，未新增新的正式測試案例。
- 未加入 Playwright trace、video recording、API automation 或 BasePage。

### 新增或修改的檔案

- 修改：`conftest.py`
- 修改：`README.md`
- 修改：`PROGRESS.md`

### Allure 整合方式

- 專案已安裝 `allure-pytest`。
- 使用 pytest 原生命令產生 Allure raw results：
  - `python -m pytest --alluredir=allure-results`
- `allure-results/` 已存在於 `.gitignore`，不會提交 raw results。
- 本階段不安裝 Allure CLI，也不宣稱可以直接開啟 HTML report。

### screenshot failure hook 架構

- 在 `conftest.py` 新增 `pytest_runtest_makereport` hook。
- Hook 使用 `hookwrapper=True`，先讓 pytest 產生原始 report，再檢查 outcome。
- 只在 `report.when == "call"` 且 `report.failed` 時處理 screenshot。
- 不改變 pytest 原本 failure behavior。
- 不使用 skip / xfail。
- 不吞掉原本 assertion 或 traceback。
- Screenshot 直接以 bytes 透過 `allure.attach()` 附加，格式為 PNG。
- Screenshot 不會永久散落專案根目錄。

### Frontend / Admin page 如何處理

- Hook 會從 `item.funcargs` 檢查目前測試是否使用：
  - `page`
  - `admin_page`
- Frontend 測試失敗時，如果 `page` 存在且未關閉，附加 `frontend-page-failure` screenshot。
- Cross-portal E2E 失敗時，如果 `page` 與 `admin_page` 都存在且未關閉，會分別附加 frontend 與 admin screenshot。
- 若某個 fixture 不存在或 Page 已關閉，會略過該 screenshot，不影響原始測試失敗。

### 驗證 failure screenshot 的方式

- 暫時新增一支明確失敗的驗證測試：`tests/test_allure_failure_probe_tmp.py`。
- 該測試同時使用 `page` 與 `admin_page`，分別開啟 Frontend 與 Admin URL，然後故意 `assert False`。
- 執行指令：
  - `python -m pytest tests/test_allure_failure_probe_tmp.py --alluredir=allure-results -v`
- 結果如預期失敗，pytest 保留原始 AssertionError traceback。
- `allure-results` 產生 2 個 PNG attachment，分別對應 Frontend page 與 Admin page。
- 驗證完成後已刪除暫時失敗測試，正式專案未留下故意失敗 test。

### 實際 pytest 執行結果

- 第一次正式 Allure results 指令：
  - `python -m pytest --alluredir=allure-results`
  - 結果：`7 passed in 30.61s`
  - `allure-results` 成功產生 raw result 檔案。
- Failure screenshot probe 指令：
  - `python -m pytest tests/test_allure_failure_probe_tmp.py --alluredir=allure-results -v`
  - 結果：`1 failed in 2.43s`
  - 符合預期，並產生 2 個 PNG attachment。
- 暫時失敗測試刪除後，會再次執行正式全專案 `--alluredir` 作為最終驗證。
- 最終正式 Allure results 指令：
  - `python -m pytest --alluredir=allure-results`
  - 結果：`7 passed in 25.07s`
  - `allure-results` 成功產生 30 個 raw result 檔案。

### 遇到的問題與解法

- 問題：需要驗證 screenshot hook，但不能破壞正式測試案例。
- 解法：建立暫時失敗 probe test 驗證 artifact，確認後立即刪除。
- 問題：Cross-portal E2E 可能同時有 `page` 與 `admin_page`。
- 解法：hook 會分別檢查兩個 fixture，存在且未關閉才各自附加 screenshot。
- 問題：README 原本仍寫「尚未加入 Allure attachment、screenshot hook、trace、DB、API 或 BasePage」，與 DB 已完成狀態矛盾。
- 解法：更新 README，目前標示 Allure raw results、失敗截圖與 MySQL DB Validation 已完成；尚未完成項目只保留 Playwright trace、video recording、API automation 與 BasePage。
- 問題：正式 Allure run 中 Admin Orders 頁 URL 已進入 `/sell/orders/`，但 heading 偶發尚未渲染完成，導致 E2E 在 `orders_heading` 驗證失敗。
- 解法：在 `AdminOrdersPage.open()` 中等待 Orders heading 可見，讓導航完成條件留在 Page Object。

### 尚未完成的項目與下一步

- 下一步為 Playwright Trace。
- 尚未加入 video recording。
- 尚未加入 API automation。

## Day 17

### 本次完成事項

- 新增 Playwright Trace on Failure。
- Frontend `browser_context` 與 Admin `admin_browser_context` 都支援 trace。
- 只有測試失敗時保存 trace zip。
- 測試成功時停止 tracing，不留下 trace file。
- 失敗 trace zip 會附加到 Allure raw results。
- 未加入 video recording、API automation、BasePage 或新的正式 Business Test Case。

### 新增或修改的檔案

- 修改：`conftest.py`
- 修改：`.gitignore`
- 修改：`README.md`
- 修改：`PROGRESS.md`

### Trace lifecycle 如何設計

- `browser_context` / `admin_browser_context` fixture 建立 `BrowserContext` 後立即呼叫：
  - `context.tracing.start(screenshots=True, snapshots=True, sources=True)`
- 測試 teardown 時檢查目前 test 是否 failed。
- 若 failed：
  - `context.tracing.stop(path=trace_path)`
  - 將 trace zip 附加到 Allure。
- 若 passed：
  - `context.tracing.stop()`
  - 不指定 path，因此不保存 trace file。
- 不改變 pytest 原始 test result。

### Frontend / Admin context 如何各自 trace

- Frontend context 使用既有 `browser_context` Fixture。
- Admin context 使用既有 `admin_browser_context` Fixture。
- 兩個 context 各自 start / stop tracing。
- Cross-portal E2E 若失敗，Frontend 與 Admin 可各自保留獨立 trace zip。
- 不共用同一個 trace file。

### pytest report 如何傳給 fixture teardown

- 沿用既有 `pytest_runtest_makereport` hook。
- Hook 使用 `setattr(item, f"rep_{report.when}", report)` 將 setup / call / teardown report 存在 test item。
- Fixture teardown 使用 `request.node.rep_call` 判斷 call phase 是否 failed。
- Screenshot hook 仍在 call failed 時執行，不與 trace 邏輯建立第二套 report hook。

### Trace file 命名與儲存位置

- Trace 目錄：`artifacts/traces/`。
- `.gitignore` 已加入 `artifacts/traces/`。
- 檔名包含 pytest nodeid 與 context 名稱：
  - `<safe-test-name>-frontend.zip`
  - `<safe-test-name>-admin.zip`
- 檔名會將 Windows 不適合的字元替換為 `-`。

### 暫時 failure probe 如何驗證

- 暫時新增 `tests/test_trace_failure_probe_tmp.py`。
- Probe 同時使用 `page` 與 `admin_page`。
- Probe 分別開啟 Frontend URL 與 Admin URL 後故意 `assert False`。
- 執行指令：
  - `python -m pytest tests/test_trace_failure_probe_tmp.py --alluredir=allure-results -v`
- 結果如預期失敗，pytest 保留原始 AssertionError traceback。
- `artifacts/traces/` 產生 2 個 trace zip：
  - frontend trace
  - admin trace
- 兩個 trace zip 皆為非空檔案。
- 使用 Python `zipfile.testzip()` 確認 zip 結構正常，`bad=None`。
- Allure results 同時產生 2 個 trace zip attachment 與既有 failure screenshot attachment。
- Probe 驗證完成後已刪除，正式專案未留下故意失敗 test。

### 實際 pytest 結果

- Failure trace probe：
  - `python -m pytest tests/test_trace_failure_probe_tmp.py --alluredir=allure-results -v`
  - 結果：`1 failed in 4.57s`
  - 符合預期，用於驗證 failure artifact。
- 正式 regression：
  - `python -m pytest --alluredir=allure-results`
  - 結果：`7 passed in 29.55s`
  - `allure-results` 產生 30 個 raw result 檔案。
  - 正式通過測試未留下 failure trace，`artifacts/traces/` 無 trace file。

### 遇到的問題與解法

- 問題：需要讓 fixture teardown 知道測試結果，但不能建立第二套互相衝突的 report hook。
- 解法：擴充既有 `pytest_runtest_makereport`，將 report 存入 `request.node`，trace fixture teardown 讀取 `rep_call`。
- 問題：pytest nodeid 可能含有 Windows filename 不適合的字元。
- 解法：新增 `safe_artifact_name()`，將不適合字元替換成 `-` 並限制長度。
- 問題：需要驗證 trace 但不能留下失敗測試。
- 解法：建立暫時 probe test，驗證後刪除並重新跑正式 regression。

### 尚未完成的項目與下一步

- 下一步為 API Automation。
- 尚未加入 video recording。
- 尚未加入 BasePage。

## Day 18

### 本次完成事項

- 開始 API Automation 第一階段。
- 確認目前本機 Docker PrestaShop Webservice / API 可用。
- 新增 API environment variables 架構。
- 新增簡單 read-only API client。
- 新增第一支 read-only GET API smoke test。
- 未新增 API 建立 / 修改 / 刪除資料。
- 未新增 UI + API E2E 串接。
- 未新增 DB + API 串接。
- 未新增 video recording、BasePage 或其他 UI Business Test。

### 新增或修改的檔案

- 新增：`utils/api_client.py`
- 新增：`tests/api/test_products_api.py`
- 修改：`conftest.py`
- 修改：`.env.example`
- 修改：本機 `.env`
- 修改：`pytest.ini`
- 修改：`README.md`
- 修改：`PROGRESS.md`

### API 前置條件

- 透過 DB read-only 查詢確認 `PS_WEBSERVICE = 1`，Webservice 已啟用。
- 目前存在 1 組 active webservice account。
- 該 key 是 Klaviyo module webservice key。
- 一般 `/api/products` 會被目前 key 拒絕，實際錯誤為 products resource 不允許使用此 key。
- 實際可用 API base endpoint 為 Klaviyo Webservice endpoint。
- `API_BASE_URL` 與 `API_KEY` 已加入本機 `.env`。
- `.env.example` 只加入變數名稱，不包含真實 API Key。

### 實際 endpoint / authentication 方式

- 實際 base endpoint：`/api/klaviyo`。
- 第一支測試使用 resource：`products`。
- 實際 request path：`/api/klaviyo/products`。
- Authentication：HTTP Basic Auth。
- API key 作為 username。
- Password 留空。
- Credential 由 `.env` 提供，不在 Python、README 或 PROGRESS 中硬編碼。

### API client 架構

- `PrestaShopApiClient` 位於 `utils/api_client.py`。
- 使用既有 dependency：`requests`。
- 第一階段只提供 `GET`。
- Client 負責：
  - `base_url`
  - Basic Authentication
  - timeout
  - GET request
  - HTTP success status handling
  - JSON response parsing
- 若 HTTP response 非 2xx，helper 會 raise `AssertionError` 並保留 pytest 原始 failure behavior。
- 若 response 不是 JSON，helper 會 raise `AssertionError`。
- 未加入 POST、PUT、PATCH、DELETE。

### response format

- 實際 API 支援 JSON，但必須帶 `output_format=JSON`。
- Products endpoint 需要 `shop` 參數。
- 測試使用最小必要 query：
  - `output_format=JSON`
  - `display=[id,name]`
  - `limit=1`
  - `shop=1`
- Response body 實際包含 `data` list。
- Product item 至少包含 `id` 與 `name`。

### 第一支 API Case

- 檔案：`tests/api/test_products_api.py`
- 測試名稱：`test_get_products_successfully`
- Markers：
  - `@pytest.mark.api`
  - `@pytest.mark.smoke`
- `pytest.ini` 新增 `api: API tests` marker。

### assertions

- 使用 Python / pytest assert。
- 不使用 Playwright `expect()` 驗 API response。
- 驗證：
  - HTTP status code 為 `200`
  - response body 存在
  - response body 包含 `data`
  - 至少有一筆 product resource
  - 第一筆 product 有 `id`
  - 第一筆 product 有 `name`
- 未硬編碼特定 product id。

### pytest 結果

- API 指定測試指令：
  - `python -m pytest tests/api/test_products_api.py -v`
- API 指定測試結果：
  - `1 passed in 0.18s`
- 全專案測試指令：
  - `python -m pytest --alluredir=allure-results`
- 全專案測試結果：
  - `8 passed in 30.32s`
- `allure-results` 成功產生 31 個 raw result 檔案。

### 遇到問題與解法

- 問題：`.env` 原本沒有 API env vars。
- 解法：確認現有 active webservice key 後，將 `API_BASE_URL` 與 `API_KEY` 加入本機 `.env`；文件不記錄 key。
- 問題：一般 `/api/products` endpoint 被目前 key 拒絕。
- 解法：依實際 PrestaShop Webservice response，改用目前 key 可用的 `/api/klaviyo/products` endpoint。
- 問題：`/api/klaviyo/products` 若沒有 `shop` 參數會回傳 `Invalid request parameters`。
- 解法：依實際 response 加入 `shop=1`。
- 問題：若未指定 `output_format=JSON`，Webservice 會回傳 XML 或錯誤。
- 解法：API test 明確使用 `output_format=JSON`，client 負責 JSON parsing。

### 尚未完成的項目與下一步

- 下一步為使用本次 UI 建立的 Order Reference 做 API Order validation。
- 尚未做 UI + API E2E 串接。
- 尚未做 DB + API 串接。
- 尚未透過 API 建立、修改或刪除資料。

## Day 19

### 本次完成事項

- 完成 Playwright Browser 顯示設定，改善本機觀察測試操作的體驗。
- 新增 `PLAYWRIGHT_SLOW_MO` 環境變數，驗證為非負整數，並在 Chromium launch 傳入 `slow_mo`。
- `.env.example` 設定 `PLAYWRIGHT_SLOW_MO=0`、`BROWSER_MAXIMIZED=false`；本機觀察設定為 `PLAYWRIGHT_SLOW_MO=700`、`BROWSER_MAXIMIZED=true`。
- 正式回歸測試建議使用 `slow_mo=0`。
- Headed 且 `BROWSER_MAXIMIZED=true` 時，Chromium 使用 `--start-maximized`，BrowserContext 使用 `no_viewport=True`，讓 viewport 適應視窗。
- Frontend `browser_context`、Admin `admin_browser_context` 與跨站 E2E 的不同 Context 共用顯示設定。
- 保留 session 共用單一 Chromium 與每個測試的 BrowserContext 隔離，不重複啟動多餘 Browser。
- 保留原本 headed 預設，新增 `--headless` 選項；不可與 `--headed` 同時使用。
- `BROWSER_MAXIMIZED=false` 維持原有 viewport 設定；Headless 不啟用最大化，未指定其他 viewport 時使用固定 1280×720。
- 未加入 `time.sleep()` 或固定等待，未修改 Business Test Case 或 pages 業務流程。
- 保留 screenshot-on-failure、trace-on-failure、Allure attachments 與 Frontend / Admin Context 隔離。

### 新增或修改的檔案

- Browser 顯示設定實作階段修改：`conftest.py`、`.env.example`、本機 `.env`。
- 本次文件更新修改：`README.md`、`PROGRESS.md`。
- 本次文件更新未修改 Python 程式碼、tests、pages、fixtures 或 `.env`。

### pytest 結果

- 以下為 Browser 顯示設定實作階段已取得的驗證結果；本次文件更新未重新執行 pytest。
- Frontend / Admin Login Smoke 指令：
  - `python -m pytest tests/frontend/test_login.py tests/admin/test_admin_login.py -m smoke -v --headed --alluredir=allure-results -p no:cacheprovider`
- 結果：`2 passed in 12.47s`。
- 此結果僅涵蓋 Frontend 與 Admin Login Smoke，不代表全專案回歸或跨站 E2E 已重新驗證。

### Browser 設定驗證

- 實作階段以本機頁面探測 Frontend、Admin 的獨立 Context，兩個 Chromium 視窗狀態皆回報 `maximized`，viewport 皆為 `None`。
- `slow_mo=700` 下，3 次本機按鈕點擊耗時 2.32 秒。
- Headless 模式確認固定 viewport 為 1280×720。
- 額外探測確認四種 headed / headless 與最大化開關組合，以及無效 slow_mo 值的拒絕行為。
- 實際螢幕上的顯示效果與操作節奏可另行人工檢視。

### 尚未完成的項目與下一步

- 本階段未重新執行全專案回歸或跨站 E2E。
- 後續仍可依 Day 18 規劃，以 UI 建立的 Order Reference 做 API Order validation。

## Day 20

### 本次完成事項

- 完成一般 PrestaShop Orders API 前置權限檢查與獨立 Key 驗證。
- 唯讀 SELECT 確認 Webservice 已啟用（`PS_WEBSERVICE=1`）。
- 原有 Klaviyo Key 沒有一般 `orders GET` 權限；GET `/api/orders` 回傳 401、錯誤碼 26。
- 使用者在 Admin 建立獨立 Orders GET 專用 Webservice Key，並自行安全填入本機 `.env`；未修改或刪除 Klaviyo Key，未以 SQL 修改權限。
- 加入 `ORDERS_API_BASE_URL`、`ORDERS_API_KEY` 獨立設定；一般 API base 為 `http://localhost:8080/api`。
- 新 Key 使用 Basic Auth（username 為 Key、password 留空），GET `/api/orders` 成功取得 HTTP 200。
- 使用 `output_format=JSON`、`display=[id,reference]`、`limit=1` 確認最外層 object 包含 `orders` array，項目具有 `id`、`reference`。
- 使用既有訂單的動態 Reference 執行 `filter[reference]`，回傳 HTTP 200、一筆符合資料，Reference 與原 Order ID 一致。
- 保留原有 Klaviyo Products 設定與測試；既有 Klaviyo products GET 亦確認回傳 HTTP 200。
- 此階段僅執行唯讀 GET 與權限 SELECT，未新增正式 Test Case 或 UI + API + DB E2E。

### 新增或修改的檔案

- 設定階段修改：`.env.example`、本機 `.env`。
- 開發紀錄於 Day 21 完整 Regression 通過後補入 `PROGRESS.md`。
- 未記錄 Key、帳密或會員個資。

### 驗證結果

- Orders 最小欄位 GET：HTTP 200，`orders` array 回傳一筆資料。
- Orders Reference Filter：HTTP 200，唯一符合訂單且 Order ID 一致。
- 以上為唯讀探測結果，不是新增 pytest Test Case 的通過結果。

### 遇到問題與解法

- 問題：Klaviyo Key 不允許一般 orders 資源；一般 `/api` 根目錄在該 Key 下曾回傳 500，原因未確認。
- 解法：保留 Klaviyo 設定，使用者另建 Orders GET Key，以一般 `/api/orders` 成功驗證；未擅自修改原有權限，也未宣稱根目錄 500 已修復。

### 尚未完成的項目與下一步

- 下一步為使用 UI 本次建立的 Order Reference 串接 Orders API 與 DB 比對，於 Day 21 完成。

## Day 21

### 本次完成事項

- 擴充既有 Bank Wire E2E 為 Frontend → Admin → API → DB。
- 新增獨立 `orders_api_client` fixture，重用 `PrestaShopApiClient`，缺少 Orders 必要設定時明確報錯，不使用 Klaviyo Key 替代。
- 先以實際唯讀 Response 確認 `id`、`reference`、`id_customer`、`current_state`、`payment`、`total_paid` 六個欄位及唯一 Reference Filter 支援。
- DB helper 保留 MySQL Decimal，不再轉 float；API 金額以 Decimal 轉換後精確比較。
- 每次 E2E 僅由 Frontend 建立一筆訂單；Admin、API、DB 使用該次相同動態 Reference，不另外建立訂單或硬編碼 ID。
- API 僅使用 GET、DB 僅使用 SELECT；保留既有 Frontend / Admin / DB assertions 與 BrowserContext 隔離。
- 保留 screenshot-on-failure、trace-on-failure 與 Allure attachments，未加入 skip、xfail 或固定 sleep。

### 新增或修改的檔案

- 實作階段修改：`conftest.py`、`utils/db_helper.py`、`tests/e2e/test_bank_wire_order.py`。
- Regression 通過後修改：`README.md`、`PROGRESS.md`。
- 重用 `utils/api_client.py`，保留 `tests/api/test_products_api.py` 與 Page Objects；本次完整 Regression 未更動程式或 Assertions。
- 本機 `.env` 保持原值，`PLAYWRIGHT_SLOW_MO=700`。

### API Assertions 與既有 DB Assertions

- GET `/api/orders` 使用 JSON output、動態 `filter[reference]` 及六個必要 display 欄位。
- HTTP 200；Response 為 object，含 `orders` array，且恰好一筆訂單。
- API Reference 與 Frontend、Admin、DB 一致。
- API Order ID / Customer ID 分別與 DB Order ID / Customer ID 一致。
- API Payment、Current State ID 與 DB 相同欄位一致；Total Paid 使用 Decimal 比較。
- 保留 DB Reference、既有測試會員、Bank transfer、狀態名稱、正值金額與 ID 的 assertions。
- 保留訂單明細商品名稱、數量為 1、價格大於 0 的 assertions。
- API 狀態 ID 比較 DB ID，Admin UI 狀態文字使用既有文字 assertions，不混用 ID 與文字。

### 實際 pytest 結果

- Products API Smoke：`python -m pytest tests/api/test_products_api.py -v`
  - 結果：`1 passed in 0.10s`。
- 指定 Bank Wire E2E：`python -m pytest tests/e2e/test_bank_wire_order.py -v`
  - 結果：`1 passed in 27.36s`。
- 完整 Regression：`python -m pytest --alluredir=allure-results`
  - 結果：`8 passed in 74.64s (0:01:14)`；共 8 支、8 pass、0 fail，未跳過測試。
- 所有指令使用專案 Python 虛擬環境；完整 Regression 保留本機 slow_mo=700。
- 本次完整 Regression 僅 Bank Wire E2E 會送出訂單；Frontend Registration 另會建立測試會員，其他 Checkout 測試不送出訂單。

### 遇到問題與解法

- 問題：DB helper 原本將 Decimal 轉成 float，金額精度可能遺失。
- 解法：保留 DB Decimal，API 金額以 `Decimal(str(...))` 比對。
- 問題：原先完整 Regression 因「不要建立第二筆訂單」的範圍不明遭自動審核拒絕，當時未執行。
- 解法：使用者明確授權不同 pytest 執行可建立新訂單，每次 E2E 只建立一筆且各層共用 Reference；本次完整 Regression 已執行並通過。
- 本次完整 Regression 無測試失敗，未降低 Assertions 或修改權限。

### 尚未完成的項目與下一步

- 本階段 E2E 整合與完整 Regression 驗證已完成，無阻擋問題。
- Day 20 記錄的 `/api` 根目錄 500 原因未調查；目前獨立 Orders Key 的 `/api/orders` 已成功，不影響本次流程。

## Day 22

### 本次完成事項

- 確認硬編碼密碼僅位於 Registration 資料工廠，供 Registration 測試使用。
- 移除 Python 密碼常值，改由獨立 `REGISTRATION_TEST_PASSWORD` 環境變數提供。
- 使用者自行安全設定本機 `.env`；本次未修改 `.env` 或其他帳號、API Key。
- `registration_user` fixture 明確檢查缺少、空白及與 Frontend / Admin 密碼共用的情況，不提供替代密碼。
- `create_registration_user(password)` 接收密碼；RegistrationUser 密碼欄位設 `repr=False`。
- 保留 UUID 唯一 Email、POM、註冊流程與既有 assertions。
- Registration context 不錄製 trace，避免 fill() 參數保存密碼；其他測試 trace、Context 隔離及 screenshot-on-failure 保留。
- 未執行任何 Git init、add、commit、push。

### 新增或修改的檔案

- `testdata/registration_data.py`
- `tests/frontend/test_registration.py`
- `conftest.py`
- `.env.example`
- `README.md`
- `PROGRESS.md`

### 實際 pytest 結果

- 使用專案 Python 虛擬環境執行：`python -m pytest tests/frontend/test_registration.py -v`。
- 結果：`1 passed in 10.47s`，建立一筆 Demo 測試會員。
- 未執行完整 Regression，不將此結果視為全專案驗證。

### 遇到問題與解法

- 問題：註冊資料原本硬編碼測試密碼，且 dataclass repr 可能顯示密碼。
- 解法：使用獨立環境變數，密碼欄位不參與 repr。
- 問題：Playwright trace 記錄 fill() 的參數，可能保存 Registration 密碼。
- 解法：只對使用 registration_user fixture 的 Frontend context 停用 trace 錄製。

### 尚未完成的項目與下一步

- 本次 Registration 指定測試通過；硬編碼 Registration 密碼已移除。
- 本次未重新檢查歷史本機 Trace 或執行完整 Regression。

### Day 22 補強：測試產物敏感資訊

- 盤點 Registration、Frontend / Admin Login、Checkout Shipping / Payment、Bank Wire E2E 的密碼輸入與 artifacts；先前只有 Registration 停用 Trace，其他 contexts 有 trace，失敗 screenshot 未遮罩。
- 最小保守政策：所有自訂 Frontend / Admin contexts 不錄製 Trace、不產生失敗 screenshot；CLI tracing / screenshot / video 非 off 即拒絕，禁止 Playwright DEBUG / PWDEBUG。
- 保留 Registration 獨立環境變數及 repr=False、Business assertions、POM 操作、測試資料、Context 隔離。
- pytest 不顯示 locals，對 longrepr / captured sections 遮蔽已知環境憑證及 URL / Basic Auth 編碼形式。
- Allure 原始 capture 附件停用；寫入結果前遮蔽 statusDetails message / trace。
- API 錯誤只保留 HTTP 狀態等診斷描述，不輸出原始 response body 或 URL。
- 修改檔案：`conftest.py`、`utils/api_client.py`、`README.md`、`PROGRESS.md`。未修改 `.env`、tests、pages、測試資料或 Git 狀態。
- targeted smoke 指令：`python -m pytest tests/frontend/test_registration.py tests/frontend/test_login.py tests/admin/test_admin_login.py tests/api/test_products_api.py -v --alluredir=allure-results`。
- 第一輪結果：`4 passed in 19.40s`；Allure 防護修正後最終結果：`4 passed in 19.18s`。兩輪各建立一筆 Registration 測試會員，未建立訂單。
- 暫存本機失敗探測初次發現 Allure 使用原始 exception / capture，僅遮蔽 pytest report 不足；停用原始 capture 並在 Allure report_result 寫檔前再次遮蔽後通過安全檢查。
- 虛構哨兵失敗探測確認 Console / Allure 不含敏感值，無 screenshot / video / trace；暫存檔已刪除，預期失敗不是正式 smoke 的失敗。
- 未執行完整 Regression 或 Bank Wire E2E；沿用相同 fixture 政策，不宣稱已重新驗證其業務流程。
- 仍存在風險：未知／舊憑證、live logging、外部 logger 或手動 attachments 不保證遮蔽；歷史 Allure / Trace 未清查或刪除。不得將此防護宣稱為完全安全。

### Day 22 最後整理：安全架構精簡與驗證

- Code Review 確認停用後的 Trace 路徑、檔名函式、failure 判斷、Trace attachment 函式、截圖空函式及相關 imports 已無用途，完成最小清理。
- 移除 context fixtures 未使用的 request 參數與不再需要的 report 暫存；保留 Browser lifecycle、Context 隔離與 pytest / Allure 遮蔽。
- 短於 4 字元的已知敏感值若出現在診斷，省略整段診斷；其餘值繼續精確遮蔽，避免逐字替換大量破壞訊息，不降低短憑證保護。
- API 網路例外只回報例外類型；JSON 解析錯誤不附原始 exception chain。HTTP 狀態仍可診斷，URL、Header、完整 body 不輸出。
- README 明確區分歷史 screenshot / Trace 與目前全面停用政策，移除易誤解的現行 Trace 操作說明。
- 未來 Trace 僅能在獨立匿名、無憑證與敏感網路資料的測試／context 經產物安全驗證後另行設計；本階段未新增功能或恢復 Trace。
- 修改檔案：`conftest.py`、`utils/api_client.py`、`README.md`、`PROGRESS.md`。
- targeted smoke：`python -m pytest tests/frontend/test_registration.py tests/frontend/test_login.py tests/admin/test_admin_login.py tests/api/test_products_api.py -v --alluredir=allure-results`。
- 實際結果：`4 passed in 20.73s`；本輪 Registration 建立一筆 Demo 會員，未建立訂單。
- 本機虛構資料安全探測通過：原值 / URL 編碼值 / 短值遮蔽、API 網路例外、省略敏感 Console / Allure 失敗資訊，且未產生 screenshot / video / Trace；暫存探測已刪除。
- 保留 Registration 獨立環境變數與 repr=False；未修改 `.env`、Business assertions、POM 或測試資料，未執行 Git 操作。
- 未執行完整 Regression 或 Bank Wire E2E。建議使用者確認後執行完整 Regression，驗證兩個 contexts 與 Orders API / DB 的整體整合。
- 仍存在風險：歷史產物、未知／舊憑證、外部 logger、live logging 與手動 attachments 未保證安全；短值出現時會損失診斷內容。

### Day 22 最終完整 Regression 驗證

- 使用者授權本次 Demo Bank Wire E2E 建立一筆訂單、Registration 建立一筆唯一 Email 的會員；各層驗證不額外建立訂單。
- 執行前確認 PrestaShop、MySQL、phpMyAdmin Docker 容器運作，Frontend GET 回傳 HTTP 200；未停止、重建或清除 Demo 資料庫。
- 使用本機既有 `.venv` 與 `.env` 執行：`python -m pytest --alluredir=allure-results -v`。
- 實際結果：`8 passed in 71.06s (0:01:11)`。
- 總測試數 8：Passed 8、Failed 0、Skipped 0、Xfailed 0、Xpassed 0、Errors 0；未使用 skip / xfail / 固定 sleep 掩蓋結果。
- Admin Login、Products API、Bank Wire E2E、Frontend Add to Cart、Checkout Payment、Checkout Shipping、Login、Registration 全部通過。
- Bank Wire E2E 的 Frontend → Admin → Orders API → DB 同一動態 Reference 驗證均通過，含 Order ID、Customer ID、Payment、Current State ID 與 Decimal Total Paid 比對。
- Registration 以獨立環境密碼及唯一 Email 正常完成，保留 repr=False 與全部既有 assertions。
- 以執行前後檔案清單 / 雜湊比對：本輪新增 8 份 Allure raw test results，全部 passed；無新增 screenshot、Trace zip 或 Video。
- 本輪新產物安全比對目前 `.env` 敏感值及 URL / Basic Auth 編碼形式，未發現已知憑證；未輸出或記錄憑證、會員個資或訂單識別資訊。
- `.env` 雜湊保持不變，未修改帳密、API Key 或 slow_mo。產物稽核暫存基準已移除。
- 本次僅更新 `README.md`、`PROGRESS.md` 及 pytest / Allure 正常產物；未修改 Python、assertions、POM 或測試資料。
- 未執行 Git init / add / commit / push，未執行 docker compose down -v。
- 本次無測試失敗或待處理的 Regression 問題；歷史產物、未知／舊憑證及外部 live logging 仍不在本輪新產物安全確認範圍。

## Day 23 — Git Pre-Commit Audit

### 實際檢查與修改

- 日期：2026-10-10。`git rev-parse --show-toplevel` 回報非 Git repository，專案沒有 `.git`；尚未初始化 Git，沒有 staged 檔案。
- 本次僅執行唯讀 Git 檢查，未執行 init、add、commit、push、reset、clean 或 Docker 資料操作。
- 原 `.gitignore` 已排除 `.env`、`.venv`、Python / pytest cache、Allure、Trace 路徑及 `.idea`；補齊 `.env.*`（保留 `.env.example`）、完整 artifacts、Trace / Screenshot / Video / Log、IDE 本機設定、憑證檔與資料庫匯出排除。
- 影像與 zip 等規則刻意保守；未來如需提交公開圖片或壓縮檔，須逐檔安全審查後調整規則。
- 對候選文字內容掃描憑證常值、環境設定、Authorization / Basic / Bearer、URL 內嵌帳密、常見 Key / JWT / 私鑰格式、Email、電話與長字串；輸出僅為檔案位置、行號、風險類型或分類，不顯示疑似秘密原值。
- 命中經上下文確認為環境變數引用、執行時參數、Basic Auth 說明、商品文字、程式識別字與 Registration 工廠產生的測試資料；未發現疑似真實憑證或私人資料。`.env.example` 敏感欄位均空白。
- 不讀取 `.env` 內容，未比對本機憑證原值或編碼值；本次靜態掃描不能保證辨識未知憑證或所有個資。
- README 補入實際存在的 `tests/api/`，保留 `tests/e2e/`；新增 Python 3.12 venv、requirements 與 Chromium 安裝、Docker PrestaShop / MySQL 前置條件及安全建立 `.env` 說明。保留現有指令、Day 22 結果與安全政策，沒有新增 CI/CD 或 GitHub 已完成的宣稱。
- 僅修改 `.gitignore`、`README.md`、`PROGRESS.md`；不修改 Python、POM、Fixture、Assertions、測試資料或 Docker 資料。Day 1～22 紀錄保留原文。
- 純文件／排除規則變更，未執行完整 Regression；`8 passed in 71.06s` 為 Day 22 歷史結果，不是 Day 23 新測試。

### 首次 Commit 候選清單

目前共 27 個檔案：Python 21 個（含 8 支測試）、Markdown 2 個、環境範本 1 個、Git 排除規則 1 個、Pytest INI 1 個、requirements TXT 1 個。以下為工作目錄候選，並非已 staged 清單；空資料夾不會納入 Git。

- `.env.example`
- `.gitignore`
- `conftest.py`
- `main.py`
- `PROGRESS.md`
- `pytest.ini`
- `README.md`
- `requirements.txt`
- `pages/admin/admin_login_page.py`
- `pages/admin/admin_orders_page.py`
- `pages/frontend/cart_page.py`
- `pages/frontend/checkout_page.py`
- `pages/frontend/login_page.py`
- `pages/frontend/order_confirmation_page.py`
- `pages/frontend/product_page.py`
- `pages/frontend/register_page.py`
- `testdata/registration_data.py`
- `tests/admin/test_admin_login.py`
- `tests/api/test_products_api.py`
- `tests/e2e/test_bank_wire_order.py`
- `tests/frontend/test_add_to_cart.py`
- `tests/frontend/test_checkout_payment.py`
- `tests/frontend/test_checkout_shipping.py`
- `tests/frontend/test_login.py`
- `tests/frontend/test_registration.py`
- `utils/api_client.py`
- `utils/db_helper.py`

### 尚未完成事項與風險

- 複核確認候選仍為 27 個；變更雜湊僅有 `.gitignore`、README、PROGRESS，Day 1～22 原始位元組雜湊一致，`.env` 大小與修改時間不變（未讀取內容）。排除規則以本機路徑比對抽查通過；尚無 Git repository，未以 Git 原生 ignore / staged 檢查驗證，下一階段仍需複核。
- Git 初始化、staging、首次 commit 與 push 均尚未執行。本次審查後可進入 Git Init 的下一階段；真正 commit 前仍須審查 staged 路徑與實際 diff，確認未使用強制加入忽略檔案。
- `.gitignore` 只控制一般未追蹤檔案，不是敏感資訊保證，也不能保護已追蹤或強制加入的內容。
- 歷史 Allure、Trace、影像與其他本機產物未清查、未刪除；本次只確認排除政策，不能宣稱歷史產物安全。`.pytest_cache` 內容存取遭拒；該目錄已排除，不影響候選文字掃描。
- 既有 `.venv` 指向不存在的 Python 3.12 基礎執行檔；下次測試前需修復／重建環境，本次不處理。
- 本次未驗證 Docker 執行狀態、套件重新安裝或測試執行；本機 Docker Compose 設定不在候選檔案中，需另行準備。
- 新增或變動檔案、未知格式、編碼憑證及其他個資仍可能超出靜態規則辨識範圍；首次 commit 前若發現任何不確定敏感資料，應停止並詢問使用者。


## Day 24 — GitHub README Portfolio Optimization

### 本次完成事項

- 將 README 改為適合公開 GitHub 的個人 QA Automation Engineer Portfolio 首頁，以繁體中文搭配既有英文技術術語。
- 依序整理 Project Overview、Tech Stack & Key Features、E2E Workflow、Test Coverage、Latest Test Results、Project Structure、Setup & Execution、Security & Limitations、Development History。
- 核對現有 8 支正式測試：7 支 Smoke、1 支 Bank Wire E2E；Coverage 表格連至實際測試檔，明確列出會員、Cart / Checkout 與訂單副作用。
- E2E 使用同一當次動態 Order Reference；Frontend 每次只建立一筆訂單，Admin / Orders API / MySQL 驗證同筆資料。API / DB 的 Status ID 比對與 Admin 狀態文字驗證分開說明，金額保留 Decimal 精確比較。
- 保留 Day 22 Full Regression 歷史結果：8 Passed、0 Failed、0 Skipped、71.06 seconds；Day 24 未重新執行測試。
- 保留 Windows PowerShell 安裝與 pytest / Allure raw results 指令；以存在檢查避免重建既有 `.venv` 或覆寫 `.env`，說明自行準備 Docker PrestaShop + MySQL 與既有測試資料的條件。
- 移除 README 中 Day 23「Python 3.12 路徑失效、需重建 .venv」的過時描述。Day 24 先前診斷已確認 Python 3.12.10、pyvenv.cfg 路徑與現有 .venv 正常，pytest、playwright、requests、allure-pytest、mysql-connector-python 均可匯入。
- 更正說明：Day 23 的環境損壞判定過於確定；Day 24 診斷發現一般 Codex 沙箱有 setup refresh 錯誤，核准的沙箱外執行正常，支持執行環境／權限差異，但未確定 Day 23 失敗的完整原因。Day 1～23 原始紀錄保留，不覆寫歷史。
- README 明確保留 .env 不提交、API GET / DB SELECT、Trace / Screenshot / Video 停用、Allure 僅 raw results，以及歷史產物／未知憑證未全面清查的限制；未新增虛構 CI/CD、HTML Report、截圖或 Badge。
- 詳細歷程透過 README 的相對連結導向 PROGRESS，避免首頁重複開發紀錄。

### 修改範圍與驗證

- 僅修改 `README.md`、`PROGRESS.md`，保留 Day 1～23 原始內容；未修改 Python、POM、Fixtures、Tests、Assertions、requirements、.gitignore 或 .env。
- 本次只做文件整理與靜態核對，不執行 pytest、Docker、git add、git commit 或 git push。
- 完成後檢查章節順序、Markdown 表格與 code fences、目錄及相對連結；以檔案雜湊與 Git diff 確認修改範圍及歷史保留。

### 尚未完成事項與下一步

- 文件尚未提交或推送；下一步為 Code Review，確認後另行授權下一次 Commit。
- Day 22 結果仍是最近已記錄的完整 Regression；本次文件變更不代表重新驗證業務流程或 Demo 環境可重建。
