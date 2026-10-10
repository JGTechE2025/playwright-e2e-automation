import pytest
from playwright.sync_api import Page, expect

from pages.frontend.register_page import RegisterPage
from testdata.registration_data import RegistrationUser


@pytest.mark.smoke
def test_register_new_customer_successfully(
    page: Page, env_vars: dict[str, str], registration_user: RegistrationUser,
) -> None:
    # 驗證使用有效資料可以成功註冊新的 Frontend 會員。
    register_page = RegisterPage(page, env_vars["FRONTEND_URL"])

    register_page.open()
    register_page.go_to_sign_in()
    register_page.go_to_registration()
    register_page.register(registration_user)

    expect(register_page.sign_out_link).to_be_visible()
    expect(register_page.your_account_link).to_be_visible()
    expect(register_page.customer_name(registration_user.full_name)).to_be_visible()
