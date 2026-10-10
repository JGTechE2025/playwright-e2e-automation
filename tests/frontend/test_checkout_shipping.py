import pytest
from playwright.sync_api import Page, expect

from pages.frontend.cart_page import CartPage
from pages.frontend.checkout_page import CheckoutPage
from pages.frontend.login_page import LoginPage
from pages.frontend.product_page import ProductPage


@pytest.mark.smoke
def test_checkout_reaches_shipping_successfully(
    page: Page,
    env_vars: dict[str, str],
) -> None:
    # 驗證固定 Frontend 測試帳號可使用既有 France Delivery Address 進入 Shipping。
    product_name = "The best is yet to come' Framed poster"

    login_page = LoginPage(page, env_vars["FRONTEND_URL"])
    product_page = ProductPage(page, env_vars["FRONTEND_URL"])
    cart_page = CartPage(page)
    checkout_page = CheckoutPage(page)

    login_page.open()
    login_page.go_to_sign_in()
    login_page.login(env_vars["FRONTEND_USERNAME"], env_vars["FRONTEND_PASSWORD"])

    product_page.open()
    product_page.open_product(product_name)
    product_page.add_product_to_cart(product_name)
    product_page.go_to_cart_from_added_modal()
    cart_page.proceed_to_checkout()

    expect(checkout_page.selected_delivery_address).to_contain_text("France")
    checkout_page.continue_from_addresses()

    expect(checkout_page.shipping_step_heading).to_be_visible()
    expect(checkout_page.first_available_shipping_method).to_be_visible()
