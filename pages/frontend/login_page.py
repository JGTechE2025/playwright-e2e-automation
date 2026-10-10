from playwright.sync_api import Locator, Page


class LoginPage:
    def __init__(self, page: Page, frontend_url: str) -> None:
        # 保存 Playwright Page 與 Frontend 首頁 URL。
        self.page = page
        self.frontend_url = frontend_url

    @property
    def sign_in_link(self) -> Locator:
        # 取得 Header 的 Sign in 入口。
        return self.page.locator('a[aria-label="Sign in"]')

    @property
    def email_input(self) -> Locator:
        # 取得 Login 表單的 Email 欄位。
        return self.page.locator("#field-email")

    @property
    def password_input(self) -> Locator:
        # 取得 Login 表單的 Password 欄位。
        return self.page.locator("#field-password")

    @property
    def sign_in_button(self) -> Locator:
        # 取得 Login 表單的 Sign in 按鈕。
        return self.page.get_by_role("button", name="Sign in")

    @property
    def sign_out_link(self) -> Locator:
        # 取得登入成功後可見的 Sign out 連結。
        return self.page.get_by_role("link", name="Sign out")

    @property
    def your_account_link(self) -> Locator:
        # 取得登入成功後可見的 Your account 連結。
        return self.page.get_by_role("link", name="Your account")

    def open(self) -> None:
        # 開啟 Frontend 首頁。
        self.page.goto(self.frontend_url)

    def go_to_sign_in(self) -> None:
        # 從 Frontend Header 進入 Sign in 頁。
        self.sign_in_link.click()

    def fill_email(self, email: str) -> None:
        # 填入 Frontend 會員 Email。
        self.email_input.fill(email)

    def fill_password(self, password: str) -> None:
        # 填入 Frontend 會員密碼。
        self.password_input.fill(password)

    def click_sign_in(self) -> None:
        # 點擊 Sign in 按鈕送出 Login 表單。
        self.sign_in_button.click()

    def login(self, email: str, password: str) -> None:
        # 完成 Frontend Login 流程。
        self.fill_email(email)
        self.fill_password(password)
        self.click_sign_in()
