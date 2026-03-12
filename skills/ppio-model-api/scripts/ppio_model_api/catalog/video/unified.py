from __future__ import annotations

from ...specs import operation

OPERATIONS = (
    operation(
        group="video",
        family="unified",
        name="unified-video-generation",
        title="视频生成通用接口",
        method="POST",
        base="v3",
        path="/video/create",
        doc_slug="reference-unified-video-generation",
    ),
)
