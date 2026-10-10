from dataclasses import dataclass, field
from uuid import uuid4


@dataclass(frozen=True)
class RegistrationUser:
    first_name: str
    last_name: str
    email: str
    password: str = field(repr=False)

    @property
    def full_name(self) -> str:
        # 組合註冊成功後前台 Header 顯示的會員名稱。
        return f"{self.first_name} {self.last_name}"


def create_registration_user(password: str) -> RegistrationUser:
    # 建立每次測試都唯一的 Frontend 註冊資料，避免 Email 重複。
    unique_id = uuid4().hex
    return RegistrationUser(
        first_name="QA",
        last_name="Automation",
        email=f"qa.auto.{unique_id}@example.com",
        password=password,
    )
