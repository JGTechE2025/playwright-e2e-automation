from playwright.sync_api import Locator, Page, expect


class AdminOrdersPage:
    def __init__(self, page: Page) -> None:
        # 保存 Admin Back Office 使用的 Playwright Page。
        self.page = page

    @property
    def orders_link(self) -> Locator:
        # 取得 Back Office 進入 Orders 頁的連結。
        return self.page.get_by_role("link", name="Orders").first

    @property
    def orders_heading(self) -> Locator:
        # 取得 Orders 頁主標題。
        return self.page.get_by_role("heading", name="Orders", exact=True)

    @property
    def reference_filter_input(self) -> Locator:
        # 取得 Orders grid 的 Reference 搜尋欄位。
        return self.page.locator("#order_reference")

    @property
    def search_button(self) -> Locator:
        # 取得 Orders grid 的 Search button。
        return self.page.locator('button[name="order[actions][search]"]')

    @property
    def reset_button(self) -> Locator:
        # 取得 Orders grid 的 Reset button，用來清除前一次保留的篩選條件。
        return self.page.locator('button[name="order[actions][reset]"]')

    @property
    def orders_table(self) -> Locator:
        # 取得 Orders grid。
        return self.page.locator("#order_grid_table")

    @property
    def order_reference(self) -> Locator:
        # 取得訂單詳細頁 Basic information 中的 Order Reference。
        return self.page.locator("#orderBasicInfo").get_by_text(
            self._current_order_reference,
            exact=True,
        )

    @property
    def customer(self) -> Locator:
        # 取得訂單詳細頁 Customer 卡片中的客戶標題。
        return self.page.locator("#customerCard h2")

    @property
    def payment_method(self) -> Locator:
        # 取得訂單詳細頁 Basic information 中的 Payment 文字。
        return self.page.locator("#orderBasicInfo").get_by_text(
            "Bank transfer",
            exact=True,
        )

    @property
    def order_status(self) -> Locator:
        # 取得訂單詳細頁目前 Order status 文字。
        return self.page.locator(".card-details").first.get_by_text(
            "Awaiting bank wire payment",
            exact=True,
        ).first

    def open(self) -> None:
        # 從 Admin Dashboard 進入 Orders 頁。
        self.orders_link.click()
        expect(self.orders_heading).to_be_visible(timeout=15000)

    def search_result_row(self, order_reference: str) -> Locator:
        # 取得 Orders grid 中指定 Reference 的搜尋結果列。
        return self.page.locator("#order_grid_table tbody tr").filter(
            has=self.page.locator(".column-reference", has_text=order_reference)
        )

    def search_result_order_reference(self, order_reference: str) -> Locator:
        # 取得搜尋結果列中的 Reference 欄位。
        return self.search_result_row(order_reference).locator(".column-reference")

    def search_order_reference(self, order_reference: str) -> None:
        # 清除保留的 grid filter，並用本次 Frontend 產生的 Reference 搜尋訂單。
        self._current_order_reference = order_reference
        if self.reset_button.count() > 0:
            self.reset_button.click()
        self.reference_filter_input.fill(order_reference)
        self.search_button.click()

    def open_order_detail(self, order_reference: str) -> None:
        # 從搜尋結果列開啟同一筆訂單詳細頁。
        self._current_order_reference = order_reference
        self.search_result_row(order_reference).locator("a.grid-view-row-link").click()
