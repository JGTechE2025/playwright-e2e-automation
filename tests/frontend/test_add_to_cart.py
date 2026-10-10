import pytest
from playwright.sync_api import Page, expect

from pages.frontend.cart_page import CartPage
from pages.frontend.product_page import ProductPage


@pytest.mark.smoke
def test_add_product_to_cart_successfully(page: Page, env_vars: dict[str, str]) -> None:
    # 驗證訪客可以將 demo shop 既有商品加入購物車。
    product_name = "The best is yet to come' Framed poster"
    quantity = "1"

    product_page = ProductPage(page, env_vars["FRONTEND_URL"])
    cart_page = CartPage(page)

    product_page.open()
    product_page.open_product(product_name)
    product_page.add_product_to_cart(product_name)
    product_page.go_to_cart_from_added_modal()

    expect(cart_page.cart_product_name(product_name)).to_be_visible()
    expect(cart_page.cart_product_quantity(product_name)).to_have_value(quantity)
