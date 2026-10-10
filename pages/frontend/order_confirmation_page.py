from playwright.sync_api import Locator, Page


class OrderConfirmationPage:
    def __init__(self, page: Page) -> None:
        # 保存 Playwright Page。
        self.page = page

    @property
    def confirmation_message(self) -> Locator:
        # 取得 Order Confirmation 成功訊息。
        return self.page.locator(".alert.alert-success").get_by_role(
            "heading",
            name="Your order is confirmed",
        )

    @property
    def payment_method(self) -> Locator:
        # 取得 Bank Wire payment information 區塊中的實際付款方式文字。
        return self.page.locator(".card.border-1").filter(
            has=self.page.get_by_role("heading", name="Payment information")
        ).get_by_text("Pay by Bank Wire", exact=True)

    @property
    def order_details(self) -> Locator:
        # 取得 Order Confirmation 中的 Order details 區塊。
        return self.page.locator(".order-confirmation__details")

    @property
    def order_reference_locator(self) -> Locator:
        # 取得包含本次 Order Reference 的明細列。
        return self.order_details.locator("li").filter(has_text="Order reference:")

    @property
    def order_reference(self) -> str:
        # 從實際確認頁文字擷取本次建立的 Order Reference。
        reference_text = self.order_reference_locator.inner_text()
        return reference_text.split(":", maxsplit=1)[1].strip()
