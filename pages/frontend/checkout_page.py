from playwright.sync_api import Locator, Page, expect


class CheckoutPage:
    def __init__(self, page: Page) -> None:
        # 保存 Playwright Page。
        self.page = page

    @property
    def selected_delivery_address(self) -> Locator:
        # 取得 Checkout Addresses step 中已選取的 Delivery Address。
        return self.page.locator(
            "#checkout-addresses-step article.address-card.selected address"
        )

    @property
    def continue_address_button(self) -> Locator:
        # 取得 Addresses step 的 Continue button。
        return self.page.locator(
            '#checkout-addresses-step button[name="confirm-addresses"]'
        )

    @property
    def shipping_step_heading(self) -> Locator:
        # 取得 Shipping Method step 標題。
        return self.page.locator("#checkout-delivery-step h1").get_by_text(
            "Shipping Method",
            exact=True,
        )

    @property
    def first_available_shipping_method(self) -> Locator:
        # 取得第一個未 disabled 的 Shipping method，代表實際可選擇的配送方式。
        return self.page.locator(
            '#checkout-delivery-step .delivery-option__item:has(input[name^="delivery_option"]:not([disabled]))'
        ).first

    def shipping_method(self, shipping_method_name: str) -> Locator:
        # 取得指定名稱且未 disabled 的 Shipping method。
        return self.page.locator(
            '#checkout-delivery-step .delivery-option__item:has(input[name^="delivery_option"]:not([disabled]))'
        ).filter(has_text=shipping_method_name)

    def shipping_method_input(self, shipping_method_name: str) -> Locator:
        # 取得指定 Shipping method 的 radio input。
        return self.shipping_method(shipping_method_name).locator(
            'input[name^="delivery_option"]'
        )

    @property
    def continue_shipping_button(self) -> Locator:
        # 取得 Shipping Method step 的 Continue button。
        return self.page.locator(
            '#checkout-delivery-step button[name="confirmDeliveryOption"]'
        )

    @property
    def payment_step_heading(self) -> Locator:
        # 取得 Payment step 標題。
        return self.page.locator("#checkout-payment-step h1").get_by_text(
            "Payment",
            exact=True,
        )

    @property
    def bank_wire_payment_method(self) -> Locator:
        # 取得實際 UI 顯示為 Pay by bank wire 的 Payment method。
        return self.page.locator(
            '#checkout-payment-step .payment-option:has(input[data-module-name="ps_wirepayment"])'
        ).get_by_text("Pay by bank wire", exact=True)

    @property
    def bank_wire_payment_method_input(self) -> Locator:
        # 取得 Bank Wire payment method 的 radio input。
        return self.page.locator(
            '#checkout-payment-step input[data-module-name="ps_wirepayment"]'
        )

    @property
    def terms_and_conditions_checkbox(self) -> Locator:
        # 取得 Payment step 必須勾選的 Terms and Conditions checkbox。
        return self.page.locator(
            '#checkout-payment-step input[name="conditions_to_approve[terms-and-conditions]"]'
        )

    @property
    def place_order_button(self) -> Locator:
        # 取得 Payment step 的 Place Order button。
        return self.page.locator('#payment-confirmation button[type="submit"]')

    def continue_from_addresses(self) -> None:
        # 使用目前已選取的 Delivery Address 進入 Shipping Method step。
        self.continue_address_button.click()

    def select_shipping_method(self, shipping_method_name: str) -> None:
        # 選擇指定 Shipping method。
        shipping_input = self.shipping_method_input(shipping_method_name)
        if not shipping_input.is_checked():
            with self.page.expect_response(
                lambda response: "action=selectDeliveryOption" in response.url
                and response.ok
            ):
                shipping_input.check()
        expect(shipping_input).to_be_checked()
        expect(self.continue_shipping_button).to_be_enabled()

    def continue_from_shipping(self) -> None:
        # 使用目前已選取的 Shipping method 進入 Payment step。
        self.continue_shipping_button.click()
        self.payment_step_heading.wait_for(state="visible")

    def select_bank_wire_payment_method(self) -> None:
        # 選擇 Pay by bank wire，但不送出訂單。
        self.bank_wire_payment_method_input.check()

    def accept_terms_and_conditions(self) -> None:
        # 勾選建立訂單前必要的 Terms and Conditions。
        self.terms_and_conditions_checkbox.check()

    def place_order(self) -> None:
        # 送出目前選取的 Payment method 並建立訂單。
        self.place_order_button.click()
