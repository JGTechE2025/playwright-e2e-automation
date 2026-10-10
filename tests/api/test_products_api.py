import pytest

from utils.api_client import PrestaShopApiClient


@pytest.mark.api
@pytest.mark.smoke
def test_get_products_successfully(env_vars: dict[str, str]) -> None:
    # 驗證 PrestaShop Webservice products read-only endpoint 可回傳最小商品資料。
    api_client = PrestaShopApiClient(
        base_url=env_vars["API_BASE_URL"],
        api_key=env_vars["API_KEY"],
    )

    response = api_client.get(
        "products",
        params={
            "output_format": "JSON",
            "display": "[id,name]",
            "limit": 1,
            "shop": 1,
        },
    )

    assert response.status_code == 200
    assert response.body
    assert "data" in response.body
    assert len(response.body["data"]) >= 1

    product = response.body["data"][0]

    assert product["id"]
    assert product["name"]
