from __future__ import annotations

from ...specs import operation

OPERATIONS = (
    operation(group="video", family="partners", name="grok-imagine-video-edit", title="Grok Imagine Video 视频编辑", method="POST", base="v3", path="/async/grok-imagine-video-edit", doc_slug="reference-grok-imagine-video-edit"),
    operation(group="video", family="partners", name="grok-imagine-video-i2v", title="Grok Imagine Video 图生视频", method="POST", base="v3", path="/async/grok-imagine-video-i2v", doc_slug="reference-grok-imagine-video-i2v"),
    operation(group="video", family="partners", name="grok-imagine-video-t2v", title="Grok Imagine Video 文生视频", method="POST", base="v3", path="/async/grok-imagine-video-t2v", doc_slug="reference-grok-imagine-video-t2v"),
    operation(group="video", family="partners", name="heygen-video-translate", title="Heygen Video-translate", method="POST", base="v3", path="/async/heygen-video-translate", doc_slug="reference-heygen-video-translate"),
    operation(group="video", family="partners", name="pixverse-v4.5-i2v", title="PixVerse V4.5 图生视频", method="POST", base="v3", path="/async/pixverse-v4.5-i2v", doc_slug="reference-pixverse-v4.5-i2v"),
    operation(group="video", family="partners", name="pixverse-v4.5-t2v", title="PixVerse V4.5 文生视频", method="POST", base="v3", path="/async/pixverse-v4.5-t2v", doc_slug="reference-pixverse-v4.5-t2v"),
    operation(group="video", family="partners", name="wondershare-tm-img2video-b", title="天幕图生视频", method="POST", base="v3", path="/async/wondershare-tm-img2video-b", doc_slug="reference-wondershare-tm-img2video-b"),
    operation(group="video", family="partners", name="wondershare-tob-text2video-b", title="天幕文生视频", method="POST", base="v3", path="/async/wondershare-tob-text2video-b", doc_slug="reference-wondershare-tob-text2video-b"),
)
