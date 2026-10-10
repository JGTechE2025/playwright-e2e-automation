from playwright.sync_api import Locator, Page


class AdminLoginPage:
    def __init__(self, page: Page, admin_url: str) -> None:
        # 保存 Playwright Page 與 Admin 登入頁 URL。
        self.page = page
        self.admin_url = admin_url

    @property
    def email_input(self) -> Locator:
        # 取得 Admin 登入表單的 Email 欄位。
        return self.page.get_by_role("textbox", name="Email address")

    @property
    def password_input(self) -> Locator:
        # 取得 Admin 登入表單的 Password 欄位。
        return self.page.get_by_label("Password")

    @property
    def login_button(self) -> Locator:
        # 取得 Admin 登入表單的登入按鈕。
        return self.page.get_by_role("button", name="LOG IN")

    @property
    def dashboard_heading(self) -> Locator:
        # 取得登入成功後 Dashboard 頁面的標題。
        return self.page.get_by_role("heading", name="Dashboard")

    def open(self) -> None:
        # 開啟 Admin 登入頁。
        self.page.goto(self.admin_url)

    def fill_email(self, email: str) -> None:
        # 填入 Admin 帳號 Email。
        self.email_input.fill(email)

    def fill_password(self, password: str) -> None:
        # 填入 Admin 帳號密碼。
        self.password_input.fill(password)

    def click_login(self) -> None:
        # 點擊登入按鈕送出表單。
        self.login_button.click()

    def login(self, email: str, password: str) -> None:
        # 完成 Admin 登入流程。
        self.fill_email(email)
        self.fill_password(password)
        self.click_login()

    def is_logged_in(self) -> bool:
        # 檢查 Dashboard 標題是否可見，用來判斷是否已登入。
        return self.dashboard_heading.is_visible()
