from __future__ import annotations

import argparse

from .registry import GROUP_ORDER, LEGACY_ALIASES, get_group_operations, get_operation, iter_operations
from .runtime import bootstrap_environment, CliError, execute_operation, execute_request, fail, print_output
from .specs import GROUP_LABELS, OperationSpec


def add_runtime_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--api-key", help="Override PPIO_API_KEY for this command only.")
    parser.add_argument(
        "--api-base",
        help="Legacy alias for --openai-base. Kept for compatibility with the earlier OpenAI-only CLI.",
    )
    parser.add_argument(
        "--openai-base",
        help="Override the OpenAI-compatible API base. Default: https://api.ppio.com/openai/v1",
    )
    parser.add_argument(
        "--openapi-base",
        help="Override the openapi billing base. Default: https://api.ppio.com/openapi/v1",
    )
    parser.add_argument(
        "--v3-base",
        help="Override the v3 media-service base. Default: https://api.ppio.com/v3",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=None,
        help="Request timeout in seconds. Default: 30.0",
    )


def add_request_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--path-param", action="append", default=[], help="Set path parameters as key=value.")
    parser.add_argument("--query", action="append", default=[], help="Set query parameters as key=value.")
    parser.add_argument("--body-file", help="Load a JSON request body from a file.")
    parser.add_argument("--body-json", help="Pass a JSON request body inline.")
    parser.add_argument("--set", action="append", default=[], help="Apply JSON body overrides as dotted key=value.")
    parser.add_argument("--form", action="append", default=[], help="Send multipart fields as key=value.")
    parser.add_argument("--file-field", action="append", default=[], help="Send multipart files as field=/absolute/path.")
    parser.add_argument("--output-file", help="Write the raw response body to a local file instead of printing it.")
    parser.add_argument(
        "--save-media",
        help="Download media URLs from the JSON response to a local path. Single artifacts may use a file path; multiple artifacts use a directory.",
    )


def build_catalog_payload(group_filter: str | None = None, family_filter: str | None = None) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for spec in iter_operations():
        if group_filter and spec.group != group_filter:
            continue
        if family_filter and spec.family != family_filter:
            continue
        rows.append(
            {
                "group": spec.group,
                "family": spec.family,
                "name": spec.name,
                "title": spec.title,
                "method": spec.method,
                "base": spec.base,
                "path": spec.path,
                "docSlug": spec.doc_slug,
                "docUrl": spec.doc_url,
                "explicitIntent": spec.explicit_intent,
            }
        )
    return rows


def add_operation_subparser(parent: argparse._SubParsersAction[argparse.ArgumentParser], spec: OperationSpec) -> None:
    parser = parent.add_parser(
        spec.name,
        help=f"{spec.title} ({spec.method} {spec.path})",
        description=f"{spec.title}\n\nOfficial docs: {spec.doc_url}",
    )
    add_request_arguments(parser)
    parser.set_defaults(handler="operation", operation_spec=spec)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Manage the full official PPIO model API through grouped commands.")
    add_runtime_arguments(parser)
    subparsers = parser.add_subparsers(dest="command", required=True)

    catalog = subparsers.add_parser("catalog", help="Print the wrapped official endpoint registry.")
    catalog.add_argument("--group", choices=GROUP_ORDER, help="Filter the catalog by command group.")
    catalog.add_argument("--family", help="Filter the catalog by family inside the selected group.")
    catalog.set_defaults(handler="catalog")

    for group in GROUP_ORDER:
        group_parser = subparsers.add_parser(group, help=GROUP_LABELS[group], description=GROUP_LABELS[group])
        group_subparsers = group_parser.add_subparsers(dest="operation", required=True)
        for spec in get_group_operations(group):
            add_operation_subparser(group_subparsers, spec)

    request = subparsers.add_parser("request", help="Send a generic request to one of the documented base families.")
    request.add_argument("method", choices=["GET", "POST", "PUT", "PATCH", "DELETE"])
    request.add_argument("path", help="Relative API path such as /models, or an absolute URL.")
    request.add_argument(
        "--base-family",
        choices=["openai", "openapi", "v3"],
        default="openai",
        help="Choose the base family for relative paths. Default: openai",
    )
    add_request_arguments(request)
    request.set_defaults(handler="request")

    models = subparsers.add_parser("models", help="Legacy alias for `llm list-models`.")
    add_request_arguments(models)
    models.set_defaults(handler="legacy", legacy_name="models")

    model = subparsers.add_parser("model", help="Legacy alias for `llm retrieve-model`.")
    model.add_argument("--model-id", required=True, help="Model identifier, for example qwen/qwen3-32b.")
    add_request_arguments(model)
    model.set_defaults(handler="legacy", legacy_name="model")

    chat = subparsers.add_parser("chat", help="Legacy alias for `llm create-chat-completion`.")
    add_request_arguments(chat)
    chat.set_defaults(handler="legacy", legacy_name="chat")

    embeddings = subparsers.add_parser("embeddings", help="Legacy alias for `llm create-embeddings`.")
    add_request_arguments(embeddings)
    embeddings.set_defaults(handler="legacy", legacy_name="embeddings")

    return parser


def execute_legacy(args: argparse.Namespace) -> object:
    group, name = LEGACY_ALIASES[args.legacy_name]
    spec = get_operation(group, name)
    if args.legacy_name == "model":
        args.path_param = [f"model={args.model_id}"]
        args.query = []
        args.body_file = None
        args.body_json = None
        args.set = []
        args.form = []
        args.file_field = []
        args.output_file = None
        args.save_media = None
    return execute_operation(spec, args)


def main(argv: list[str] | None = None) -> int:
    bootstrap_environment()
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        if args.handler == "catalog":
            payload = build_catalog_payload(group_filter=args.group, family_filter=args.family)
        elif args.handler == "request":
            payload = execute_request(args)
        elif args.handler == "legacy":
            payload = execute_legacy(args)
        else:
            payload = execute_operation(args.operation_spec, args)
        print_output(payload)
        return 0
    except CliError as error:
        return fail(error)
