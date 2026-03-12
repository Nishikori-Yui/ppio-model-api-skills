from __future__ import annotations

from ...specs import operation

OPERATIONS = (
    operation(group="video", family="vidu", name="vidu-2.0-img2video", title="Vidu 2.0 图生视频", method="POST", base="v3", path="/async/vidu-2.0-img2video", doc_slug="reference-vidu-2.0-img2video"),
    operation(group="video", family="vidu", name="vidu-2.0-reference2video", title="Vidu 2.0 参考生视频", method="POST", base="v3", path="/async/vidu-2.0-reference2video", doc_slug="reference-vidu-2.0-reference2video"),
    operation(group="video", family="vidu", name="vidu-2.0-startend2video", title="Vidu 2.0 首末帧", method="POST", base="v3", path="/async/vidu-2.0-startend2video", doc_slug="reference-vidu-2.0-startend2video"),
    operation(group="video", family="vidu", name="vidu-q1-img2video", title="Vidu Q1 图生视频", method="POST", base="v3", path="/async/vidu-q1-img2video", doc_slug="reference-vidu-q1-img2video"),
    operation(group="video", family="vidu", name="vidu-q1-reference2video", title="Vidu Q1 参考生视频", method="POST", base="v3", path="/async/vidu-q1-reference2video", doc_slug="reference-vidu-q1-reference2video"),
    operation(group="video", family="vidu", name="vidu-q1-startend2video", title="Vidu Q1 首末帧", method="POST", base="v3", path="/async/vidu-q1-startend2video", doc_slug="reference-vidu-q1-startend2video"),
    operation(group="video", family="vidu", name="vidu-q1-text2video", title="Vidu Q1 文生视频", method="POST", base="v3", path="/async/vidu-q1-text2video", doc_slug="reference-vidu-q1-text2video"),
    operation(group="video", family="vidu", name="vidu-q2-pro-fast-img2video", title="VIDU Q2 Pro Fast 图生视频", method="POST", base="v3", path="/async/vidu-q2-pro-fast-img2video", doc_slug="reference-vidu-q2-pro-fast-img2video"),
    operation(group="video", family="vidu", name="vidu-q2-pro-fast-startend2video", title="VIDU Q2 Pro Fast 首尾帧", method="POST", base="v3", path="/async/vidu-q2-pro-fast-startend2video", doc_slug="reference-vidu-q2-pro-fast-startend2video"),
    operation(group="video", family="vidu", name="vidu-q2-pro-img2video", title="VIDU Q2 Pro 图生视频", method="POST", base="v3", path="/async/vidu-q2-pro-img2video", doc_slug="reference-vidu-q2-pro-img2video"),
    operation(group="video", family="vidu", name="vidu-q2-pro-multiframe", title="VIDU Q2 Pro 智能多帧", method="POST", base="v3", path="/async/vidu-q2-pro-multiframe", doc_slug="reference-vidu-q2-pro-multiframe"),
    operation(group="video", family="vidu", name="vidu-q2-pro-startend2video", title="VIDU Q2 Pro 首尾帧", method="POST", base="v3", path="/async/vidu-q2-pro-startend2video", doc_slug="reference-vidu-q2-pro-startend2video"),
    operation(group="video", family="vidu", name="vidu-q2-reference2video", title="VIDU Q2 参考生视频", method="POST", base="v3", path="/async/vidu-q2-reference2video", doc_slug="reference-vidu-q2-reference2video"),
    operation(group="video", family="vidu", name="vidu-q2-template2video", title="VIDU Q2 场景模板", method="POST", base="v3", path="/async/vidu-q2-template2video", doc_slug="reference-vidu-q2-template2video"),
    operation(group="video", family="vidu", name="vidu-q2-text2video", title="VIDU Q2 文生视频", method="POST", base="v3", path="/async/vidu-q2-text2video", doc_slug="reference-vidu-q2-text2video"),
    operation(group="video", family="vidu", name="vidu-q2-turbo-img2video", title="VIDU Q2 Turbo 图生视频", method="POST", base="v3", path="/async/vidu-q2-turbo-img2video", doc_slug="reference-vidu-q2-turbo-img2video"),
    operation(group="video", family="vidu", name="vidu-q2-turbo-multiframe", title="VIDU Q2 Turbo 智能多帧", method="POST", base="v3", path="/async/vidu-q2-turbo-multiframe", doc_slug="reference-vidu-q2-turbo-multiframe"),
    operation(group="video", family="vidu", name="vidu-q2-turbo-startend2video", title="VIDU Q2 Turbo 首尾帧", method="POST", base="v3", path="/async/vidu-q2-turbo-startend2video", doc_slug="reference-vidu-q2-turbo-startend2video"),
    operation(group="video", family="vidu", name="vidu-q3-pro-i2v", title="Vidu Q3 Pro 图生视频", method="POST", base="v3", path="/async/vidu-q3-pro-i2v", doc_slug="reference-vidu-q3-pro-i2v"),
    operation(group="video", family="vidu", name="vidu-q3-pro-t2v", title="Vidu Q3 Pro 文生视频", method="POST", base="v3", path="/async/vidu-q3-pro-t2v", doc_slug="reference-vidu-q3-pro-t2v"),
)
