from __future__ import annotations

from ...specs import operation

OPERATIONS = (
    operation(group="video", family="kling", name="kling-2.5-turbo-i2v", title="Kling V2.5 Turbo 图生视频", method="POST", base="v3", path="/async/kling-2.5-turbo-i2v", doc_slug="reference-kling-2.5-turbo-i2v"),
    operation(group="video", family="kling", name="kling-2.5-turbo-t2v", title="Kling V2.5 Turbo 文生视频", method="POST", base="v3", path="/async/kling-2.5-turbo-t2v", doc_slug="reference-kling-2.5-turbo-t2v"),
    operation(group="video", family="kling", name="kling-o1-i2v", title="Kling-o1 图生视频", method="POST", base="v3", path="/async/kling-o1-i2v", doc_slug="reference-kling-o1-i2v"),
    operation(group="video", family="kling", name="kling-o1-ref2v", title="Kling-o1 参考生视频", method="POST", base="v3", path="/async/kling-o1-ref2v", doc_slug="reference-kling-o1-ref2v"),
    operation(group="video", family="kling", name="kling-o1-t2v", title="Kling-o1 文生视频", method="POST", base="v3", path="/async/kling-o1-t2v", doc_slug="reference-kling-o1-t2v"),
    operation(group="video", family="kling", name="kling-o1-video-edit", title="Kling-o1 视频编辑", method="POST", base="v3", path="/async/kling-o1-video-edit", doc_slug="reference-kling-o1-video-edit"),
    operation(group="video", family="kling", name="kling-v1.6-i2v", title="KLING V1.6 图生视频", method="POST", base="v3", path="/async/kling-v1.6-i2v", doc_slug="reference-kling-v1.6-i2v"),
    operation(group="video", family="kling", name="kling-v1.6-t2v", title="KLING V1.6 文生视频", method="POST", base="v3", path="/async/kling-v1.6-t2v", doc_slug="reference-kling-v1.6-t2v"),
    operation(group="video", family="kling", name="kling-v2.6-pro-i2v", title="Kling V2.6 Pro 图生视频", method="POST", base="v3", path="/async/kling-v2.6-pro-i2v", doc_slug="reference-kling-v2.6-pro-i2v"),
    operation(group="video", family="kling", name="kling-v2.6-pro-motion-control", title="Kling V2.6 Pro 动作控制", method="POST", base="v3", path="/async/kling-v2.6-pro-motion-control", doc_slug="reference-kling-v2.6-pro-motion-control"),
    operation(group="video", family="kling", name="kling-v2.6-pro-t2v", title="Kling V2.6 Pro 文生视频", method="POST", base="v3", path="/async/kling-v2.6-pro-t2v", doc_slug="reference-kling-v2.6-pro-t2v"),
    operation(group="video", family="kling", name="kling-v3.0-pro-i2v", title="Kling v3.0 Pro 图生视频", method="POST", base="v3", path="/async/kling-v3.0-pro-i2v", doc_slug="reference-kling-v3.0-pro-i2v"),
    operation(group="video", family="kling", name="kling-v3.0-pro-t2v", title="Kling v3.0 Pro 文生视频", method="POST", base="v3", path="/async/kling-v3.0-pro-t2v", doc_slug="reference-kling-v3.0-pro-t2v"),
    operation(group="video", family="kling", name="kling-v3.0-std-i2v", title="Kling v3.0 Standard 图生视频", method="POST", base="v3", path="/async/kling-v3.0-std-i2v", doc_slug="reference-kling-v3.0-std-i2v"),
    operation(group="video", family="kling", name="kling-v3.0-std-t2v", title="Kling v3.0 Standard 文字生成视频", method="POST", base="v3", path="/async/kling-v3.0-std-t2v", doc_slug="reference-kling-v3.0-std-t2v"),
)
