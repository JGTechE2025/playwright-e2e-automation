from dataclasses import dataclass
from typing import Any

import requests
from requests.auth import HTTPBasicAuth


@dataclass(frozen=True)
class ApiResponse:
    status_code: int
    body: Any


class PrestaShopApiClient:
    def __init__(self, base_url: str, api_key: str, timeout: int = 10) -> None:
        # PrestaShop Webservice 使用 API key 作為 Basic Auth username，password 留空。
        self.base_url = base_url.rstrip("/")
        self.auth = HTTPBasicAuth(api_key, "")
        self.timeout = timeout

    def get(self, resource: str, params: dict[str, Any] | None = None) -> ApiResponse:
        # 第一階段 API automation 僅支援 read-only GET。
        url = f"{self.base_url}/{resource.lstrip('/')}"
        try:
            response = requests.get(
                url,
                auth=self.auth,
                params=params,
                timeout=self.timeout,
            )
        except requests.RequestException as error:
            raise AssertionError(
                f"GET request failed ({type(error).__name__}); details omitted for security"
            ) from None
        self._ensure_success(response)
        return ApiResponse(status_code=response.status_code, body=self._parse_json(response))

    def _ensure_success(self, response: requests.Response) -> None:
        if not response.ok:
            raise AssertionError(
                f"GET request failed with status {response.status_code}; response body omitted for security"
            )

    def _parse_json(self, response: requests.Response) -> Any:
        try:
            return response.json()
        except ValueError:
            raise AssertionError(
                f"Expected JSON response (HTTP {response.status_code}); response body omitted for security"
            ) from None
