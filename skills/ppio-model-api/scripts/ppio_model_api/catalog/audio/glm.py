from __future__ import annotations

from ...specs import operation

OPERATIONS = (
    operation(group="audio", family="glm", name="glm-asr", title="GLM 音频转文字", method="POST", base="v3", path="/glm-asr", doc_slug="reference-glm-asr"),
    operation(group="audio", family="glm", name="glm-tts", title="GLM 语音合成", method="POST", base="v3", path="/glm-tts", doc_slug="reference-glm-tts"),
    operation(group="audio", family="glm", name="glm-tts-voice-clone", title="GLM 音频复刻", method="POST", base="v3", path="/glm-tts-voice-clone", doc_slug="reference-glm-tts-voice-clone"),
)
