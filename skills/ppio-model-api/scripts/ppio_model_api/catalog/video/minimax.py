from __future__ import annotations

from ...specs import operation

OPERATIONS = (
    operation(group="video", family="minimax", name="minimax-hailuo-02", title="Minimax Hailuo-02", method="POST", base="v3", path="/async/minimax-hailuo-02", doc_slug="reference-minimax-hailuo-02"),
    operation(group="video", family="minimax", name="minimax-hailuo-2.3-fast-i2v", title="Minimax Hailuo 2.3 Fast 图生视频", method="POST", base="v3", path="/async/minimax-hailuo-2.3-fast-i2v", doc_slug="reference-minimax-hailuo-2.3-fast-i2v"),
    operation(group="video", family="minimax", name="minimax-hailuo-2.3-i2v", title="Minimax Hailuo 2.3 图生视频", method="POST", base="v3", path="/async/minimax-hailuo-2.3-i2v", doc_slug="reference-minimax-hailuo-2.3-i2v"),
    operation(group="video", family="minimax", name="minimax-hailuo-2.3-t2v", title="Minimax Hailuo 2.3 文生视频", method="POST", base="v3", path="/async/minimax-hailuo-2.3-t2v", doc_slug="reference-minimax-hailuo-2.3-t2v"),
    operation(group="video", family="minimax", name="minimax-video-01", title="Minimax Video-01", method="POST", base="v3", path="/async/minimax-video-01", doc_slug="reference-minimax-video-01"),
)
