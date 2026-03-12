from __future__ import annotations

from ...specs import operation

OPERATIONS = (
    operation(
        group="image",
        family="jimeng",
        name="jimeng-txt2img-v3.0",
        title="即梦文生图 3.0",
        method="POST",
        base="v3",
        path="/async/jimeng-txt2img-v3.0",
        doc_slug="reference-jimeng-txt2img-v3.0",
    ),
    operation(
        group="image",
        family="jimeng",
        name="jimeng-txt2img-v3.1",
        title="即梦文生图 3.1",
        method="POST",
        base="v3",
        path="/async/jimeng-txt2img-v3.1",
        doc_slug="reference-jimeng-txt2img-v3.1",
    ),
)
