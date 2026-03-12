from __future__ import annotations

from ...specs import operation

OPERATIONS = (
    operation(group="video", family="seedance", name="seedance-v1-lite-i2v", title="Seedance V1 Lite 图生视频", method="POST", base="v3", path="/async/seedance-v1-lite-i2v", doc_slug="reference-seedance-v1-lite-i2v"),
    operation(group="video", family="seedance", name="seedance-v1-lite-t2v", title="Seedance V1 Lite 文生视频", method="POST", base="v3", path="/async/seedance-v1-lite-t2v", doc_slug="reference-seedance-v1-lite-t2v"),
    operation(group="video", family="seedance", name="seedance-v1-pro-i2v", title="Seedance V1 Pro 图生视频", method="POST", base="v3", path="/async/seedance-v1-pro-i2v", doc_slug="reference-seedance-v1-pro-i2v"),
    operation(group="video", family="seedance", name="seedance-v1-pro-t2v", title="Seedance V1 Pro 文生视频", method="POST", base="v3", path="/async/seedance-v1-pro-t2v", doc_slug="reference-seedance-v1-pro-t2v"),
    operation(group="video", family="seedance", name="seedance-v1.5-pro-i2v", title="Seedance 1.5 Pro 图生视频", method="POST", base="v3", path="/async/seedance-v1.5-pro-i2v", doc_slug="reference-seedance-v1.5-pro-i2v"),
    operation(group="video", family="seedance", name="seedance-v1.5-pro-t2v", title="Seedance 1.5 Pro 文生视频", method="POST", base="v3", path="/async/seedance-v1.5-pro-t2v", doc_slug="reference-seedance-v1.5-pro-t2v"),
)
