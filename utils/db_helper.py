import re
from typing import Any

import mysql.connector
from mysql.connector.connection import MySQLConnection


class DatabaseHelper:
    _FORBIDDEN_SQL = re.compile(
        r"\b(INSERT|UPDATE|DELETE|DROP|ALTER|CREATE|TRUNCATE|REPLACE|MERGE)\b",
        re.IGNORECASE,
    )

    def __init__(
        self,
        host: str,
        port: int,
        database: str,
        user: str,
        password: str,
    ) -> None:
        # 保存 DB connection 設定，不在程式碼硬編碼任何密碼。
        self.host = host
        self.port = port
        self.database = database
        self.user = user
        self.password = password
        self._connection: MySQLConnection | None = None

    def connect(self) -> None:
        # 建立 MySQL connection。
        self._connection = mysql.connector.connect(
            host=self.host,
            port=self.port,
            database=self.database,
            user=self.user,
            password=self.password,
            ssl_disabled=True,
        )

    def close(self) -> None:
        # 關閉 MySQL connection。
        if self._connection and self._connection.is_connected():
            self._connection.close()

    def fetch_one(self, query: str, params: tuple[Any, ...] = ()) -> dict[str, Any] | None:
        # 執行單筆 read-only SELECT 查詢。
        rows = self.fetch_all(query, params)
        if not rows:
            return None
        if len(rows) > 1:
            raise AssertionError(f"Expected one DB row, got {len(rows)}")
        return rows[0]

    def fetch_all(self, query: str, params: tuple[Any, ...] = ()) -> list[dict[str, Any]]:
        # 執行 read-only SELECT 查詢並回傳 dict rows。
        self._ensure_select_only(query)
        if not self._connection:
            raise RuntimeError("Database connection is not open")

        cursor = self._connection.cursor(dictionary=True)
        try:
            cursor.execute(query, params)
            rows = cursor.fetchall()
        finally:
            cursor.close()

        return [self._normalize_row(row) for row in rows]

    def fetch_order_by_reference(self, order_reference: str) -> dict[str, Any]:
        # 使用 Frontend 產生的 Order Reference 查詢 ps_orders 與相關驗證資料。
        order = self.fetch_one(
            """
            SELECT
                o.id_order,
                o.reference,
                o.payment,
                o.total_paid,
                o.id_customer,
                o.current_state,
                c.firstname,
                c.lastname,
                osl.name AS order_state_name
            FROM ps_orders o
            INNER JOIN ps_customer c ON c.id_customer = o.id_customer
            INNER JOIN ps_order_state_lang osl
                ON osl.id_order_state = o.current_state
                AND osl.id_lang = (
                    SELECT l.id_lang
                    FROM ps_lang l
                    WHERE l.active = 1
                    ORDER BY l.id_lang
                    LIMIT 1
                )
            WHERE o.reference = %s
            """,
            (order_reference,),
        )
        if order is None:
            raise AssertionError(f"Order reference not found in DB: {order_reference}")
        return order

    def fetch_order_details(self, order_id: int) -> list[dict[str, Any]]:
        # 使用 DB 查到的 id_order 查詢該訂單明細。
        return self.fetch_all(
            """
            SELECT
                id_order,
                product_name,
                product_quantity,
                product_price
            FROM ps_order_detail
            WHERE id_order = %s
            """,
            (order_id,),
        )

    def _ensure_select_only(self, query: str) -> None:
        stripped_query = query.strip()
        if not stripped_query.upper().startswith("SELECT"):
            raise ValueError("Only SELECT queries are allowed")
        if self._FORBIDDEN_SQL.search(stripped_query):
            raise ValueError("Only read-only SELECT queries are allowed")

    def _normalize_row(self, row: dict[str, Any]) -> dict[str, Any]:
        # 保留 MySQL Decimal 精度，供 API / DB 金額精確比較。
        return dict(row)
