from collections.abc import Generator
from pathlib import Path
import os
import re

import allure_commons
import pytest
from dotenv import load_dotenv
from playwright.sync_api import Browser, BrowserContext, Page, Playwright

from utils.db_helper import DatabaseHelper
from utils.api_client import PrestaShopApiClient
from testdata.registration_data import RegistrationUser, create_registration_user


PROJECT_ROOT = Path(__file__).resolve().parent
load_dotenv(PROJECT_ROOT / ".env")

REQUIRED_ENV_VARS = (
    "FRONTEND_URL",
    "FRONTEND_USERNAME",
    "FRONTEND_PASSWORD",
    "ADMIN_URL",
    "ADMIN_USERNAME",
    "ADMIN_PASSWORD",
    "DB_HOST",
    "DB_PORT",
    "DB_NAME",
    "DB_USER",
    "DB_PASSWORD",
    "API_BASE_URL",
    "API_KEY",
)


def get_required_env(name: str) -> str:
    # 取得必要環境變數，缺少時明確中止並指出變數名稱。
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value


def redact_sensitive_text(text: str) -> str:
    from base64 import b64encode
    from urllib.parse import quote, quote_plus

    values = set()
    for name, value in os.environ.items():
        if value and any(part in name.upper() for part in ("PASSWORD", "API_KEY", "TOKEN", "SECRET", "USERNAME")):
            values.update((value, quote(value, safe=""), quote_plus(value)))
            if "KEY" in name.upper():
                values.add(b64encode(f"{value}:".encode()).decode())
    # 短值不逐字替換，以免一般訊息被大量破壞；仍採保守省略。
    if any(len(value) < 4 and value in text for value in values):
        return "[REDACTED: diagnostic omitted because it contains a short sensitive value]"
    for value in sorted(values, key=len, reverse=True):
        text = text.replace(value, "[REDACTED]")
    return text


def pytest_configure(config: pytest.Config) -> None:
    # 阻止 plugin 另行產生未經處理的影像、video 或 trace。
    for option in ("tracing", "screenshot", "video"):
        if config.getoption(option, default="off") != "off":
            raise pytest.UsageError("Sensitive artifact protection requires tracing/screenshot/video=off")
    config.option.showlocals = False
    # Allure teardown 會重新附加 capture；停用未經遮蔽的原始 Log 附件。
    config.option.attach_capture = False
    if not allure_commons.plugin_manager.has_plugin("sensitive-report-redaction"):
        allure_commons.plugin_manager.register(SensitiveAllureReports(), "sensitive-report-redaction")
    if "pw:" in os.getenv("DEBUG", "") or os.getenv("PWDEBUG"):
        raise pytest.UsageError("Disable Playwright debug logging for credential-bearing tests")


class SensitiveAllureReports:
    @allure_commons.hookimpl(hookwrapper=True, tryfirst=True)
    def report_result(self, result):
        # Allure 使用原始 exception 產生 statusDetails，須在寫檔前再次遮蔽。
        if result.statusDetails:
            for field in ("message", "trace"):
                value = getattr(result.statusDetails, field, None)
                if value:
                    setattr(result.statusDetails, field, redact_sensitive_text(value))
        yield


@pytest.hookimpl(hookwrapper=True, trylast=True)
def pytest_runtest_makereport(item: pytest.Item, call: pytest.CallInfo[object]):
    # 只遮蔽 pytest 錯誤及 capture，不保存影像或變更測試結果。
    outcome = yield
    report = outcome.get_result()
    if report.longrepr is not None:
        report.longrepr = redact_sensitive_text(str(report.longrepr))
    report.sections = [(name, redact_sensitive_text(text)) for name, text in report.sections]


@pytest.fixture(scope="session")
def orders_api_client() -> PrestaShopApiClient:
    # Orders 設定獨立驗證，不影響 Klaviyo Products，也不使用其他 Key 替代。
    return PrestaShopApiClient(
        base_url=get_required_env("ORDERS_API_BASE_URL"),
        api_key=get_required_env("ORDERS_API_KEY"),
    )


@pytest.fixture(scope="session")
def env_vars() -> dict[str, str]:
    # 提供測試所需的環境變數集合。
    return {name: get_required_env(name) for name in REQUIRED_ENV_VARS}


@pytest.fixture
def registration_user() -> RegistrationUser:
    password = get_required_env("REGISTRATION_TEST_PASSWORD")
    if not password.strip():
        raise RuntimeError("Missing required environment variable: REGISTRATION_TEST_PASSWORD")
    if password in (os.getenv("FRONTEND_PASSWORD"), os.getenv("ADMIN_PASSWORD")):
        raise RuntimeError("REGISTRATION_TEST_PASSWORD must be independent of login credentials")
    return create_registration_user(password)


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption(
        "--headless", action="store_true", default=False,
        help="Run project Chromium headlessly (default: headed).",
    )


@pytest.fixture(scope="session")
def browser_type_launch_args(
    browser_type_launch_args: dict,
    pytestconfig: pytest.Config,
) -> dict:
    # 延伸 plugin 參數，保留原本 headed 預設，不額外啟動 Browser。
    options = dict(browser_type_launch_args)
    raw_slow_mo = os.getenv("PLAYWRIGHT_SLOW_MO", "0").strip()
    if not re.fullmatch(r"[0-9]+", raw_slow_mo):
        raise pytest.UsageError("PLAYWRIGHT_SLOW_MO must be a non-negative integer")
    if pytestconfig.getoption("--headless") and pytestconfig.getoption("--headed"):
        raise pytest.UsageError("--headless and --headed cannot be used together")
    options["headless"] = pytestconfig.getoption("--headless")
    options["slow_mo"] = int(raw_slow_mo)
    if os.getenv("BROWSER_MAXIMIZED", "false").strip().lower() == "true" and not options["headless"]:
        options["args"] = [*options.get("args", []), "--start-maximized"]
    return options


@pytest.fixture(scope="session")
def browser_context_args(
    browser_context_args: dict,
    browser_type_launch_args: dict,
) -> dict:
    # Frontend、Admin、跨站 E2E 與 plugin context 共用設定。
    options = dict(browser_context_args)
    if "--start-maximized" in browser_type_launch_args.get("args", []):
        options.pop("viewport", None)
        options.pop("device_scale_factor", None)
        options["no_viewport"] = True
    return options


@pytest.fixture(scope="session")
def browser(
    playwright: Playwright,
    browser_type_launch_args: dict,
) -> Generator[Browser, None, None]:
    # 使用 plugin Playwright lifecycle，每個 session 僅啟動一個 Chromium。
    browser = playwright.chromium.launch(**browser_type_launch_args)
    try:
        yield browser
    finally:
        browser.close()


@pytest.fixture(scope="function")
def browser_context(
    browser: Browser,
    browser_context_args: dict,
) -> Generator[BrowserContext, None, None]:
    # 每個測試建立獨立的 BrowserContext，避免共用登入狀態。
    context = browser.new_context(**browser_context_args)
    # 所有自訂 UI contexts 採 fail-closed：不錄製憑證或敏感畫面。
    try:
        yield context
    finally:
        context.close()


@pytest.fixture(scope="function")
def page(browser_context: BrowserContext) -> Page:
    # 從目前測試的 BrowserContext 建立新的 Page。
    return browser_context.new_page()


@pytest.fixture(scope="function")
def admin_browser_context(
    browser: Browser,
    browser_context_args: dict,
) -> Generator[BrowserContext, None, None]:
    # Admin 使用獨立 BrowserContext，避免共用 Frontend 登入狀態。
    context = browser.new_context(**browser_context_args)
    # Admin 登入同樣不錄製憑證或敏感畫面。
    try:
        yield context
    finally:
        context.close()


@pytest.fixture(scope="function")
def admin_page(admin_browser_context: BrowserContext) -> Page:
    # 從 Admin 專用 BrowserContext 建立 Page。
    return admin_browser_context.new_page()


@pytest.fixture(scope="function")
def db_helper(env_vars: dict[str, str]) -> Generator[DatabaseHelper, None, None]:
    # 建立 read-only DB helper，測試結束後確實關閉連線。
    helper = DatabaseHelper(
        host=env_vars["DB_HOST"],
        port=int(env_vars["DB_PORT"]),
        database=env_vars["DB_NAME"],
        user=env_vars["DB_USER"],
        password=env_vars["DB_PASSWORD"],
    )
    try:
        helper.connect()
        yield helper
    finally:
        helper.close()
