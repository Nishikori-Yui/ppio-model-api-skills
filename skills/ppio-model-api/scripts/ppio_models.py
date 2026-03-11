#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any

DEFAULT_API_BASE = "https://api.ppio.com/openai/v1"
DEFAULT_TIMEOUT = 30.0


class CliError(Exception):
    pass


def parse_dotenv_line(raw_line: str) -> tuple[str, str] | None:
    line = raw_line.strip()
    if not line or line.startswith("#"):
        return None
    if line.startswith("export "):
        line = line[len("export ") :].strip()
    key, separator, value = line.partition("=")
    if not separator:
        return None
    key = key.strip()
    value = value.strip()
    if not key:
        return None
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
        value = value[1:-1]
    return key, value


def load_dotenv_file(path: Path) -> bool:
    loaded = False
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            parsed = parse_dotenv_line(line)
            if parsed is None:
                continue
            key, value = parsed
            os.environ.setdefault(key, value)
            loaded = True
    return loaded


def iter_parent_env_files(start: Path) -> list[Path]:
    candidates: list[Path] = []
    current = start.resolve()
    if current.is_file():
        current = current.parent
    for directory in [current, *current.parents]:
        candidates.append(directory / ".env")
    return candidates


def bootstrap_environment() -> Path | None:
    roots = [Path(__file__).resolve().parent, Path.cwd()]
    seen: set[Path] = set()
    for root in roots:
        for candidate in iter_parent_env_files(root):
            resolved = candidate.resolve(strict=False)
            if resolved in seen:
                continue
            seen.add(resolved)
            if candidate.is_file():
                load_dotenv_file(candidate)
                return candidate
    return None


def parse_value(raw: str) -> Any:
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return raw


def parse_set_arguments(items: list[str] | None) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for item in items or []:
        key, separator, value = item.partition("=")
        if not separator or not key:
            raise CliError(f"Invalid --set value: {item!r}. Expected key=value.")
        result[key] = parse_value(value)
    return result


def load_json_file(path: str) -> dict[str, Any]:
    with open(path, "r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise CliError(f"JSON file {path!r} must contain a top-level object.")
    return data


def load_json_text(raw: str) -> dict[str, Any]:
    data = json.loads(raw)
    if not isinstance(data, dict):
        raise CliError("Inline JSON must contain a top-level object.")
    return data


def build_body(
    *,
    body_file: str | None = None,
    body_json: str | None = None,
    overrides: list[str] | None = None,
) -> dict[str, Any] | None:
    body: dict[str, Any] = {}
    if body_file:
        body.update(load_json_file(body_file))
    if body_json:
        body.update(load_json_text(body_json))
    if overrides:
        body.update(parse_set_arguments(overrides))
    return body or None


def stringify_query_value(value: Any) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=False, separators=(",", ":"))
    return str(value)


def encode_query(query: dict[str, Any] | None) -> str:
    if not query:
        return ""
    pairs: list[tuple[str, str]] = []
    for key, value in query.items():
        if value is None:
            continue
        if isinstance(value, (list, tuple)):
            for item in value:
                pairs.append((key, stringify_query_value(item)))
        else:
            pairs.append((key, stringify_query_value(value)))
    return urllib.parse.urlencode(pairs)


def resolve_url(base: str, path: str) -> str:
    if path.startswith("http://") or path.startswith("https://"):
        return path
    return f"{base.rstrip('/')}/{path.lstrip('/')}"


def request_json(
    *,
    method: str,
    base_url: str,
    path: str,
    api_key: str,
    timeout: float,
    query: dict[str, Any] | None = None,
    body: dict[str, Any] | None = None,
) -> Any:
    url = resolve_url(base_url, path)
    encoded_query = encode_query(query)
    if encoded_query:
        separator = "&" if "?" in url else "?"
        url = f"{url}{separator}{encoded_query}"

    headers = {"Authorization": f"Bearer {api_key}"}
    data: bytes | None = None
    if body is not None:
        headers["Content-Type"] = "application/json"
        data = json.dumps(body, ensure_ascii=False).encode("utf-8")

    request = urllib.request.Request(url=url, data=data, headers=headers, method=method.upper())

    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            raw = response.read()
            if not raw:
                return {}
            decoded = raw.decode("utf-8")
            try:
                return json.loads(decoded)
            except json.JSONDecodeError:
                return {"raw": decoded}
    except urllib.error.HTTPError as error:
        raw_error = error.read().decode("utf-8", errors="replace")
        payload: Any
        try:
            payload = json.loads(raw_error)
        except json.JSONDecodeError:
            payload = raw_error or error.reason
        raise CliError(f"HTTP {error.code} for {method.upper()} {url}: {json.dumps(payload, ensure_ascii=False)}") from error
    except urllib.error.URLError as error:
        raise CliError(f"Request failed for {method.upper()} {url}: {error.reason}") from error


def print_output(payload: Any) -> None:
    print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))


def require_api_key(args: argparse.Namespace) -> str:
    api_key = args.api_key or os.environ.get("PPIO_API_KEY")
    if not api_key:
        raise CliError("Missing API key. Set PPIO_API_KEY or pass --api-key.")
    return api_key


def common_runtime(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--api-key", help="Override PPIO_API_KEY for this command only.")
    parser.add_argument(
        "--api-base",
        default=os.environ.get("PPIO_MODEL_API_BASE", DEFAULT_API_BASE),
        help=f"Override the API base URL. Default: {DEFAULT_API_BASE}",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=float(os.environ.get("PPIO_TIMEOUT", str(DEFAULT_TIMEOUT))),
        help=f"Request timeout in seconds. Default: {DEFAULT_TIMEOUT}",
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Manage PPIO model APIs through the documented OpenAI-compatible API.")
    common_runtime(parser)
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("models", help="List available models.")

    model = subparsers.add_parser("model", help="Retrieve one model by identifier.")
    model.add_argument("--model-id", required=True)

    chat = subparsers.add_parser("chat", help="Create a chat completion.")
    chat.add_argument("--body-file")
    chat.add_argument("--body-json")
    chat.add_argument("--set", action="append", default=[], help="Set top-level request fields as key=value.")

    embeddings = subparsers.add_parser("embeddings", help="Create embeddings.")
    embeddings.add_argument("--body-file")
    embeddings.add_argument("--body-json")
    embeddings.add_argument("--set", action="append", default=[], help="Set top-level request fields as key=value.")

    request = subparsers.add_parser("request", help="Send a generic request to the PPIO model API.")
    request.add_argument("method", choices=["GET", "POST", "PUT", "PATCH", "DELETE"])
    request.add_argument("path", help="Relative API path such as /models, or an absolute URL.")
    request.add_argument("--query", action="append", default=[], help="Add query parameters as key=value.")
    request.add_argument("--body-file")
    request.add_argument("--body-json")
    request.add_argument("--set", action="append", default=[], help="Override request fields as key=value.")

    return parser


def run_command(args: argparse.Namespace) -> Any:
    api_key = require_api_key(args)
    base_url = args.api_base
    timeout = args.timeout

    if args.command == "models":
        return request_json(method="GET", base_url=base_url, path="/models", api_key=api_key, timeout=timeout)

    if args.command == "model":
        encoded_model = urllib.parse.quote(args.model_id, safe="")
        return request_json(method="GET", base_url=base_url, path=f"/models/{encoded_model}", api_key=api_key, timeout=timeout)

    if args.command == "chat":
        body = build_body(body_file=args.body_file, body_json=args.body_json, overrides=args.set)
        if not body:
            raise CliError("chat requires --body-file, --body-json, or at least one --set.")
        return request_json(
            method="POST",
            base_url=base_url,
            path="/chat/completions",
            api_key=api_key,
            timeout=timeout,
            body=body,
        )

    if args.command == "embeddings":
        body = build_body(body_file=args.body_file, body_json=args.body_json, overrides=args.set)
        if not body:
            raise CliError("embeddings requires --body-file, --body-json, or at least one --set.")
        return request_json(
            method="POST",
            base_url=base_url,
            path="/embeddings",
            api_key=api_key,
            timeout=timeout,
            body=body,
        )

    if args.command == "request":
        query = parse_set_arguments(args.query)
        body = build_body(body_file=args.body_file, body_json=args.body_json, overrides=args.set)
        return request_json(
            method=args.method,
            base_url=base_url,
            path=args.path,
            api_key=api_key,
            timeout=timeout,
            query=query,
            body=body,
        )

    raise CliError(f"Unsupported command: {args.command}")


def main(argv: list[str] | None = None) -> int:
    bootstrap_environment()
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        payload = run_command(args)
        print_output(payload)
        return 0
    except CliError as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
