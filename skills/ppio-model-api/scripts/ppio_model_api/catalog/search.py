from __future__ import annotations

from ..specs import operation

OPERATIONS = (
    operation(
        group="search",
        family="web-search",
        name="web-search",
        title="Web Search API",
        method="POST",
        base="v3",
        path="/web-search",
        doc_slug="reference-web-search",
    ),
)
