from playwright.sync_api import Locator, Page

from testdata.registration_data import RegistrationUser


class RegisterPage:
    def __init__(self, page: Page, frontend_url: str) -> None:
        # 保存 Playwright Page 與 Frontend 首頁 URL。
        self.page = page
        self.frontend_url = frontend_url

    @property
    def sign_in_link(self) -> Locator:
        # 取得 Header 的 Sign in 入口。
        return self.page.locator('a[aria-label="Sign in"]')

    @property
    def create_account_link(self) -> Locator:
        # 取得登入頁的 Create an account 入口。
        return self.page.get_by_role("link", name="Create an account")

    @property
    def social_title_mr_radio(self) -> Locator:
        # 取得註冊表單的 Mr. social title 選項。
        return self.page.get_by_label("Mr.")

    @property
    def first_name_input(self) -> Locator:
        # 取得註冊表單的 First name 欄位。
        return self.page.get_by_role("textbox", name="First name")

    @property
    def last_name_input(self) -> Locator:
        # 取得註冊表單的 Last name 欄位。
        return self.page.get_by_role("textbox", name="Last name")

    @property
    def email_input(self) -> Locator:
        # 取得註冊表單的 Email 欄位。
        return self.page.locator("#field-email")

    @property
    def password_input(self) -> Locator:
        # 取得註冊表單的 Password 欄位。
        return self.page.locator("#field-password")

    @property
    def customer_privacy_checkbox(self) -> Locator:
        # 取得必要的 Customer data privacy checkbox。
        return self.page.locator("#field-customer_privacy")

    @property
    def terms_checkbox(self) -> Locator:
        # 取得必要的 terms and privacy policy checkbox。
        return self.page.locator("#field-psgdpr")

    @property
    def create_account_button(self) -> Locator:
        # 取得註冊表單的送出按鈕。
        return self.page.get_by_role("button", name="Create account")

    @property
    def sign_out_link(self) -> Locator:
        # 取得註冊成功並登入後才會顯示的 Sign out 連結。
        return self.page.get_by_role("link", name="Sign out")

    @property
    def your_account_link(self) -> Locator:
        # 取得登入狀態下可見的 Your account 連結。
        return self.page.get_by_role("link", name="Your account")

    def customer_name(self, full_name: str) -> Locator:
        # 取得 Header 顯示的註冊會員名稱。
        return self.page.get_by_text(full_name, exact=True)

    def open(self) -> None:
        # 開啟 Frontend 首頁。
        self.page.goto(self.frontend_url)

    def go_to_sign_in(self) -> None:
        # 從 Frontend Header 進入 Sign in 頁。
        self.sign_in_link.click()

    def go_to_registration(self) -> None:
        # 從 Sign in 頁進入 Registration 頁。
        self.create_account_link.click()

    def select_social_title(self) -> None:
        # 選擇註冊表單的 Social title。
        self.social_title_mr_radio.check()

    def fill_first_name(self, first_name: str) -> None:
        # 填入會員 First name。
        self.first_name_input.fill(first_name)

    def fill_last_name(self, last_name: str) -> None:
        # 填入會員 Last name。
        self.last_name_input.fill(last_name)

    def fill_email(self, email: str) -> None:
        # 填入唯一 Email。
        self.email_input.fill(email)

    def fill_password(self, password: str) -> None:
        # 填入符合 PrestaShop 規則的密碼。
        self.password_input.fill(password)

    def accept_required_policies(self) -> None:
        # 勾選註冊必要的 Privacy / Terms checkbox。
        self.customer_privacy_checkbox.check()
        self.terms_checkbox.check()

    def submit_registration(self) -> None:
        # 送出 Registration 表單。
        self.create_account_button.click()

    def register(self, user: RegistrationUser) -> None:
        # 完成 Frontend Registration 流程。
        self.select_social_title()
        self.fill_first_name(user.first_name)
        self.fill_last_name(user.last_name)
        self.fill_email(user.email)
        self.fill_password(user.password)
        self.accept_required_policies()
        self.submit_registration()
