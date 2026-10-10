from playwright.sync_api import Locator, Page


class ProductPage:
    def __init__(self, page: Page, frontend_url: str) -> None:
        # 保存 Playwright Page 與 Frontend 首頁 URL。
        self.page = page
        self.frontend_url = frontend_url

    @property
    def proceed_to_checkout_link(self) -> Locator:
        # 取得加入購物車成功 modal 中前往 Cart 頁的連結。
        return self.page.get_by_role("link", name="Proceed to checkout")

    def product_link(self, product_name: str) -> Locator:
        # 取得首頁中指定商品的商品頁連結。
        return self.page.get_by_role("link", name=f"View product {product_name}")

    def add_to_cart_button(self, product_name: str) -> Locator:
        # 取得商品頁主商品的 Add to cart 按鈕。
        return self.page.get_by_role("button", name=f"Add to cart {product_name}")

    def open(self) -> None:
        # 開啟 Frontend 首頁。
        self.page.goto(self.frontend_url)

    def open_product(self, product_name: str) -> None:
        # 從首頁進入指定商品頁。
        self.product_link(product_name).first.click()

    def add_product_to_cart(self, product_name: str) -> None:
        # 在商品頁將目前商品加入購物車。
        self.add_to_cart_button(product_name).click()

    def go_to_cart_from_added_modal(self) -> None:
        # 從加入購物車成功 modal 進入 Cart 頁。
        self.proceed_to_checkout_link.click()
