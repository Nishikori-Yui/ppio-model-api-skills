from __future__ import annotations

from dataclasses import dataclass
import re

DEFAULT_BASES = {
    "openai": "https://api.ppio.com/openai/v1",
    "openapi": "https://api.ppio.com/openapi/v1",
    "v3": "https://api.ppio.com/v3",
}

GROUP_LABELS = {
    "base": "Base account and billing endpoints.",
    "llm": "OpenAI-compatible LLM endpoints.",
    "batch": "Batch inference and file-management endpoints.",
    "image": "Image generation and editing endpoints.",
    "video": "Video generation endpoints.",
    "audio": "Audio generation and transcription endpoints.",
    "search": "Web-search endpoints.",
    "tasks": "Async task lookup endpoints.",
}

PATH_PARAMETER_RE = re.compile(r"{([^{}]+)}")


@dataclass(frozen=True)
class OperationSpec:
    group: str
    family: str
    name: str
    title: str
    method: str
    base: str
    path: str
    doc_slug: str
    explicit_intent: bool

    @property
    def doc_url(self) -> str:
        return f"https://ppio.com/docs/models/{self.doc_slug}"

    @property
    def path_params(self) -> tuple[str, ...]:
        return tuple(PATH_PARAMETER_RE.findall(self.path))

    @property
    def endpoint_label(self) -> str:
        return f"{self.base}:{self.path}"


def operation(
    *,
    group: str,
    family: str,
    name: str,
    title: str,
    method: str,
    base: str,
    path: str,
    doc_slug: str,
    explicit_intent: bool | None = None,
) -> OperationSpec:
    resolved_method = method.upper()
    if explicit_intent is None:
        explicit_intent = resolved_method != "GET"
    return OperationSpec(
        group=group,
        family=family,
        name=name,
        title=title,
        method=resolved_method,
        base=base,
        path=path,
        doc_slug=doc_slug,
        explicit_intent=explicit_intent,
    )
