from decimal import Decimal

import pytest
from playwright.sync_api import Page, expect

from pages.admin.admin_login_page import AdminLoginPage
from pages.admin.admin_orders_page import AdminOrdersPage
from pages.frontend.cart_page import CartPage
from pages.frontend.checkout_page import CheckoutPage
from pages.frontend.login_page import LoginPage
from pages.frontend.order_confirmation_page import OrderConfirmationPage
from pages.frontend.product_page import ProductPage
from utils.db_helper import DatabaseHelper
from utils.api_client import PrestaShopApiClient


@pytest.mark.e2e
def test_customer_can_place_bank_wire_order_successfully(
    page: Page,
    admin_page: Page,
    db_helper: DatabaseHelper,
    orders_api_client: PrestaShopApiClient,
    env_vars: dict[str, str],
) -> None:
    # 同一筆 Bank Wire Order 依序完成 Frontend、Admin、API 與 DB 驗證。
    product_name = "The best is yet to come' Framed poster"

    login_page = LoginPage(page, env_vars["FRONTEND_URL"])
    product_page = ProductPage(page, env_vars["FRONTEND_URL"])
    cart_page = CartPage(page)
    checkout_page = CheckoutPage(page)
    order_confirmation_page = OrderConfirmationPage(page)

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
    checkout_page.select_shipping_method("My carrier")
    checkout_page.continue_from_shipping()

    expect(checkout_page.payment_step_heading).to_be_visible()
    checkout_page.select_bank_wire_payment_method()
    checkout_page.accept_terms_and_conditions()
    checkout_page.place_order()

    expect(order_confirmation_page.confirmation_message).to_be_visible()
    expect(order_confirmation_page.order_reference_locator).to_be_visible()
    expect(order_confirmation_page.payment_method).to_contain_text("Pay by Bank Wire")

    order_reference = order_confirmation_page.order_reference

    assert order_reference
    assert order_reference.isupper()
    assert order_reference.isalnum()

    admin_login_page = AdminLoginPage(admin_page, env_vars["ADMIN_URL"])
    admin_orders_page = AdminOrdersPage(admin_page)

    admin_login_page.open()
    admin_login_page.login(env_vars["ADMIN_USERNAME"], env_vars["ADMIN_PASSWORD"])
    expect(admin_login_page.dashboard_heading).to_be_visible()

    admin_orders_page.open()
    expect(admin_orders_page.orders_heading).to_be_visible()
    admin_orders_page.search_order_reference(order_reference)
    expect(admin_orders_page.search_result_order_reference(order_reference)).to_have_text(
        order_reference
    )
    admin_orders_page.open_order_detail(order_reference)

    expect(admin_orders_page.order_reference).to_have_text(order_reference)
    expect(admin_orders_page.customer).to_contain_text("QA Automation")
    expect(admin_orders_page.payment_method).to_contain_text("Bank transfer")
    expect(admin_orders_page.order_status).to_contain_text("Awaiting bank wire payment")

    response = orders_api_client.get(
        "orders",
        params={
            "output_format": "JSON",
            "filter[reference]": f"[{order_reference}]",
            "display": "[id,reference,id_customer,current_state,payment,total_paid]",
        },
    )
    assert response.status_code == 200
    assert isinstance(response.body, dict)
    assert "orders" in response.body
    assert isinstance(response.body["orders"], list)
    assert len(response.body["orders"]) == 1
    api_order = response.body["orders"][0]
    assert api_order["reference"] == order_reference

    db_order = db_helper.fetch_order_by_reference(order_reference)

    assert api_order["reference"] == db_order["reference"]
    assert int(api_order["id"]) == db_order["id_order"]
    assert int(api_order["id_customer"]) == db_order["id_customer"]
    assert api_order["payment"] == db_order["payment"]
    assert int(api_order["current_state"]) == db_order["current_state"]
    assert Decimal(str(api_order["total_paid"])) == db_order["total_paid"]

    assert db_order["reference"] == order_reference
    assert db_order["firstname"] == "QA"
    assert db_order["lastname"] == "Automation"
    assert db_order["payment"] == "Bank transfer"
    assert db_order["order_state_name"] == "Awaiting bank wire payment"
    assert db_order["total_paid"] > 0
    assert db_order["id_customer"] > 0
    assert db_order["current_state"] > 0

    order_details = db_helper.fetch_order_details(db_order["id_order"])

    assert order_details
    assert any(product_name in detail["product_name"] for detail in order_details)
    matching_product = next(
        detail for detail in order_details if product_name in detail["product_name"]
    )
    assert matching_product["product_quantity"] == 1
    assert matching_product["product_price"] > 0
