from __future__ import annotations

from ...specs import operation

OPERATIONS = (
    operation(group="audio", family="minimax", name="minimax-speech-02-hd", title="MiniMax Speech-02-hd 同步语音合成", method="POST", base="v3", path="/minimax-speech-02-hd", doc_slug="reference-minimax-speech-02-hd"),
    operation(group="audio", family="minimax", name="minimax-speech-02-hd-async", title="MiniMax Speech-02-hd 异步语音合成", method="POST", base="v3", path="/async/minimax-speech-02-hd", doc_slug="reference-minimax-speech-02-hd-async"),
    operation(group="audio", family="minimax", name="minimax-speech-02-turbo", title="MiniMax Speech-02-turbo 同步语音合成", method="POST", base="v3", path="/minimax-speech-02-turbo", doc_slug="reference-minimax-speech-02-turbo"),
    operation(group="audio", family="minimax", name="minimax-speech-02-turbo-async", title="MiniMax Speech-02-turbo 异步语音合成", method="POST", base="v3", path="/async/minimax-speech-02-turbo", doc_slug="reference-minimax-speech-02-turbo-async"),
    operation(group="audio", family="minimax", name="minimax-speech-2.5-hd-preview", title="MiniMax Speech-2.5-hd-preview 同步语音合成", method="POST", base="v3", path="/minimax-speech-2.5-hd-preview", doc_slug="reference-minimax-speech-2.5-hd-preview"),
    operation(group="audio", family="minimax", name="minimax-speech-2.5-hd-preview-async", title="MiniMax Speech-2.5-hd-preview 异步语音合成", method="POST", base="v3", path="/async/minimax-speech-2.5-hd-preview", doc_slug="reference-minimax-speech-2.5-hd-preview-async"),
    operation(group="audio", family="minimax", name="minimax-speech-2.5-turbo-preview", title="MiniMax Speech-2.5-turbo-preview 同步语音合成", method="POST", base="v3", path="/minimax-speech-2.5-turbo-preview", doc_slug="reference-minimax-speech-2.5-turbo-preview"),
    operation(group="audio", family="minimax", name="minimax-speech-2.5-turbo-preview-async", title="MiniMax Speech-2.5-turbo-preview 异步语音合成", method="POST", base="v3", path="/async/minimax-speech-2.5-turbo-preview", doc_slug="reference-minimax-speech-2.5-turbo-preview-async"),
    operation(group="audio", family="minimax", name="minimax-speech-2.6-hd", title="MiniMax Speech-2.6-hd 同步语音合成", method="POST", base="v3", path="/minimax-speech-2.6-hd", doc_slug="reference-minimax-speech-2.6-hd"),
    operation(group="audio", family="minimax", name="minimax-speech-2.6-hd-async", title="MiniMax Speech-2.6-hd 异步语音合成", method="POST", base="v3", path="/async/minimax-speech-2.6-hd", doc_slug="reference-minimax-speech-2.6-hd-async"),
    operation(group="audio", family="minimax", name="minimax-speech-2.6-turbo", title="MiniMax Speech-2.6-turbo 同步语音合成", method="POST", base="v3", path="/minimax-speech-2.6-turbo", doc_slug="reference-minimax-speech-2.6-turbo"),
    operation(group="audio", family="minimax", name="minimax-speech-2.6-turbo-async", title="MiniMax Speech-2.6-turbo 异步语音合成", method="POST", base="v3", path="/async/minimax-speech-2.6-turbo", doc_slug="reference-minimax-speech-2.6-turbo-async"),
    operation(group="audio", family="minimax", name="minimax-speech-2.8-hd", title="MiniMax Speech 2.8 HD 同步语音合成", method="POST", base="v3", path="/minimax-speech-2.8-hd", doc_slug="reference-minimax-speech-2.8-hd"),
    operation(group="audio", family="minimax", name="minimax-speech-2.8-hd-async", title="MiniMax Speech 2.8 HD 异步语音合成", method="POST", base="v3", path="/async/minimax-speech-2.8-hd", doc_slug="reference-minimax-speech-2.8-hd-async"),
    operation(group="audio", family="minimax", name="minimax-speech-2.8-turbo", title="MiniMax Speech 2.8 Turbo 同步语音合成", method="POST", base="v3", path="/minimax-speech-2.8-turbo", doc_slug="reference-minimax-speech-2.8-turbo"),
    operation(group="audio", family="minimax", name="minimax-speech-2.8-turbo-async", title="MiniMax Speech 2.8 Turbo 异步语音合成", method="POST", base="v3", path="/async/minimax-speech-2.8-turbo", doc_slug="reference-minimax-speech-2.8-turbo-async"),
    operation(group="audio", family="minimax", name="minimax-voice-cloning", title="MiniMax 音频快速复刻", method="POST", base="v3", path="/minimax-voice-cloning", doc_slug="reference-minimax-voice-cloning"),
)
