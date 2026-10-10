from playwright.sync_api import Locator, Page


class CartPage:
    def __init__(self, page: Page) -> None:
        # 保存 Playwright Page。
        self.page = page

    @property
    def cart_overview(self) -> Locator:
        # 取得 Cart 頁實際購物車商品清單區塊，排除 featured products。
        return self.page.locator(".cart__overview")

    def cart_product_name(self, product_name: str) -> Locator:
        # 取得 Cart 商品列中的商品名稱。
        return self.cart_overview.locator(".product-line__title").get_by_text(
            product_name,
            exact=True,
        )

    def cart_product_quantity(self, product_name: str) -> Locator:
        # 取得 Cart 商品列中的商品數量欄位。
        return self.cart_overview.locator(
            f'input[aria-label="Change quantity of {product_name}"]'
        )

    @property
    def proceed_to_checkout_link(self) -> Locator:
        # 取得 Cart summary 中進入 Checkout 的連結。
        return self.page.get_by_role("link", name="Proceed to checkout")

    def proceed_to_checkout(self) -> None:
        # 從 Cart 頁進入 Checkout。
        self.proceed_to_checkout_link.click()
