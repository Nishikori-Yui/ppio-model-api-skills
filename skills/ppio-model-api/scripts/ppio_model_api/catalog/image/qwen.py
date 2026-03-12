from __future__ import annotations

from ...specs import operation

OPERATIONS = (
    operation(
        group="image",
        family="qwen-image",
        name="qwen-image-edit",
        title="Qwen-Image 图像编辑",
        method="POST",
        base="v3",
        path="/async/qwen-image-edit",
        doc_slug="reference-qwen-image-edit",
    ),
    operation(
        group="image",
        family="qwen-image",
        name="qwen-image-txt2img",
        title="Qwen-Image 文生图",
        method="POST",
        base="v3",
        path="/async/qwen-image-txt2img",
        doc_slug="reference-qwen-image-txt2img",
    ),
)
