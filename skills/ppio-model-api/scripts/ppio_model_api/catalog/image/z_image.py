from __future__ import annotations

from ...specs import operation

OPERATIONS = (
    operation(
        group="image",
        family="z-image",
        name="z-image-turbo",
        title="Z Image 文生图 Turbo",
        method="POST",
        base="v3",
        path="/async/z-image-turbo",
        doc_slug="reference-z-image-turbo",
    ),
    operation(
        group="image",
        family="z-image",
        name="z-image-turbo-lora",
        title="Z Image 文生图 Turbo LoRA",
        method="POST",
        base="v3",
        path="/async/z-image-turbo-lora",
        doc_slug="reference-z-image-turbo-lora",
    ),
)
