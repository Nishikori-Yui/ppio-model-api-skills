from __future__ import annotations

from collections import defaultdict

from .catalog import OPERATIONS
from .specs import OperationSpec

GROUP_ORDER = ("base", "llm", "batch", "image", "video", "audio", "search", "tasks")

LEGACY_ALIASES: dict[str, tuple[str, str]] = {
    "models": ("llm", "list-models"),
    "model": ("llm", "retrieve-model"),
    "chat": ("llm", "create-chat-completion"),
    "embeddings": ("llm", "create-embeddings"),
}


def _validate_operations(operations: tuple[OperationSpec, ...]) -> tuple[OperationSpec, ...]:
    seen: set[tuple[str, str]] = set()
    for spec in operations:
        key = (spec.group, spec.name)
        if key in seen:
            raise RuntimeError(f"Duplicate operation registration for {spec.group}:{spec.name}")
        seen.add(key)
    return tuple(sorted(operations, key=lambda item: (GROUP_ORDER.index(item.group), item.family, item.name)))


ALL_OPERATIONS = _validate_operations(tuple(OPERATIONS))
OPERATIONS_BY_GROUP: dict[str, tuple[OperationSpec, ...]] = {
    group: tuple(spec for spec in ALL_OPERATIONS if spec.group == group) for group in GROUP_ORDER
}
OPERATIONS_BY_KEY = {(spec.group, spec.name): spec for spec in ALL_OPERATIONS}
OPERATIONS_BY_FAMILY: dict[str, tuple[OperationSpec, ...]] = defaultdict(tuple)
for spec in ALL_OPERATIONS:
    family_key = f"{spec.group}:{spec.family}"
    OPERATIONS_BY_FAMILY[family_key] = (*OPERATIONS_BY_FAMILY[family_key], spec)


def get_group_operations(group: str) -> tuple[OperationSpec, ...]:
    return OPERATIONS_BY_GROUP[group]


def get_operation(group: str, name: str) -> OperationSpec:
    return OPERATIONS_BY_KEY[(group, name)]


def iter_operations() -> tuple[OperationSpec, ...]:
    return ALL_OPERATIONS
