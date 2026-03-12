from __future__ import annotations

from ...specs import operation

OPERATIONS = (
    operation(
        group="image",
        family="seedream",
        name="seedream-4.0",
        title="Seedream 图片生成 4.0",
        method="POST",
        base="v3",
        path="/seedream-4.0",
        doc_slug="reference-seedream-4.0",
    ),
    operation(
        group="image",
        family="seedream",
        name="seedream-4.5",
        title="Seedream 图片生成 4.5",
        method="POST",
        base="v3",
        path="/seedream-4.5",
        doc_slug="reference-seedream-4.5",
    ),
    operation(
        group="image",
        family="seedream",
        name="seedream-5.0-lite",
        title="Seedream 图片生成 5.0 lite",
        method="POST",
        base="v3",
        path="/seedream-5.0-lite",
        doc_slug="reference-seedream-5.0-lite",
    ),
)
