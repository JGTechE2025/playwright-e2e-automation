import pytest
from playwright.sync_api import Page, expect

from pages.frontend.login_page import LoginPage


@pytest.mark.smoke
def test_frontend_login_with_valid_credentials(page: Page, env_vars: dict[str, str]) -> None:
    # 驗證使用有效 Frontend 測試帳號可以登入成功。
    login_page = LoginPage(page, env_vars["FRONTEND_URL"])

    login_page.open()
    login_page.go_to_sign_in()
    login_page.login(env_vars["FRONTEND_USERNAME"], env_vars["FRONTEND_PASSWORD"])

    expect(login_page.sign_out_link).to_be_visible()
    expect(login_page.your_account_link).to_be_visible()
