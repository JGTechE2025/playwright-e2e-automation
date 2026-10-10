import pytest
from playwright.sync_api import Page, expect

from pages.admin.admin_login_page import AdminLoginPage


@pytest.mark.smoke
def test_admin_login_with_valid_credentials(page: Page, env_vars: dict[str, str]) -> None:
    # 驗證使用正確 Admin 帳號密碼可以登入後台。
    admin_login_page = AdminLoginPage(page, env_vars["ADMIN_URL"])

    admin_login_page.open()
    admin_login_page.login(env_vars["ADMIN_USERNAME"], env_vars["ADMIN_PASSWORD"])

    expect(admin_login_page.dashboard_heading).to_be_visible()
