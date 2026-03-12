from __future__ import annotations

from ..specs import operation

OPERATIONS = (
    operation(
        group="base",
        family="account",
        name="bill-list",
        title="查询账单",
        method="GET",
        base="openapi",
        path="/billing/bill/list",
        doc_slug="reference-get-bill-pay-as-you-model",
        explicit_intent=False,
    ),
    operation(
        group="base",
        family="account",
        name="user-info",
        title="获取账户信息",
        method="GET",
        base="v3",
        path="/user",
        doc_slug="reference-get-user-info",
        explicit_intent=False,
    ),
)
