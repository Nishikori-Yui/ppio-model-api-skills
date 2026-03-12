from __future__ import annotations

from ...specs import operation

OPERATIONS = (
    operation(
        group="image",
        family="image-tools",
        name="image-eraser",
        title="图像擦除",
        method="POST",
        base="v3",
        path="/async/image-eraser",
        doc_slug="reference-image-eraser",
    ),
    operation(
        group="image",
        family="image-tools",
        name="image-remove-background",
        title="图像背景移除",
        method="POST",
        base="v3",
        path="/async/image-remove-background",
        doc_slug="reference-image-remove-background",
    ),
    operation(
        group="image",
        family="image-tools",
        name="image-upscaler",
        title="图像高清化",
        method="POST",
        base="v3",
        path="/async/image-upscaler",
        doc_slug="reference-image-upscaler",
    ),
)
