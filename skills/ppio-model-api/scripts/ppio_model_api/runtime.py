from __future__ import annotations

import base64
from email.message import Message
import json
import mimetypes
import os
from pathlib import Path
import re
import secrets
import sys
from typing import Any
import urllib.error
import urllib.parse
import urllib.request

from .specs import DEFAULT_BASES, OperationSpec, PATH_PARAMETER_RE

DEFAULT_TIMEOUT = 30.0
MEDIA_HINT_TOKENS = ("image", "video", "audio", "media", "artifact", "thumbnail", "poster", "download", "result", "output")
EXACT_MEDIA_HINTS = {
    "image",
    "images",
    "video",
    "videos",
    "audio",
    "audios",
    "media",
    "medias",
    "artifact",
    "artifacts",
    "thumbnail",
    "thumbnails",
    "poster",
    "posters",
}


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


def parse_key_value(item: str, *, option_name: str) -> tuple[str, str]:
    key, separator, value = item.partition("=")
    if not separator or not key:
        raise CliError(f"Invalid {option_name} value: {item!r}. Expected key=value.")
    return key, value


def parse_path_parameters(items: list[str] | None) -> dict[str, str]:
    result: dict[str, str] = {}
    for item in items or []:
        key, value = parse_key_value(item, option_name="--path-param")
        result[key] = value
    return result


def parse_query_parameters(items: list[str] | None) -> list[tuple[str, Any]]:
    result: list[tuple[str, Any]] = []
    for item in items or []:
        key, value = parse_key_value(item, option_name="--query")
        result.append((key, parse_value(value)))
    return result


def parse_form_fields(items: list[str] | None) -> list[tuple[str, str]]:
    result: list[tuple[str, str]] = []
    for item in items or []:
        key, value = parse_key_value(item, option_name="--form")
        result.append((key, value))
    return result


def parse_file_fields(items: list[str] | None) -> list[tuple[str, Path]]:
    result: list[tuple[str, Path]] = []
    for item in items or []:
        key, value = parse_key_value(item, option_name="--file-field")
        path = Path(value).expanduser()
        if not path.is_file():
            raise CliError(f"File field {key!r} points to a missing file: {value}")
        result.append((key, path))
    return result


def ensure_container_for_segment(next_segment: str) -> Any:
    return [] if next_segment.isdigit() else {}


def set_nested_value(root: Any, key: str, value: Any) -> None:
    if not key:
        raise CliError("Empty override key is not allowed.")
    segments = key.split(".")
    current = root
    for index, segment in enumerate(segments):
        is_last = index == len(segments) - 1
        next_segment = segments[index + 1] if not is_last else ""
        if segment.isdigit():
            if not isinstance(current, list):
                raise CliError(f"Cannot index into non-list object at {segment!r}.")
            position = int(segment)
            while len(current) <= position:
                current.append(None)
            if is_last:
                current[position] = value
                return
            if current[position] is None:
                current[position] = ensure_container_for_segment(next_segment)
            current = current[position]
            continue
        if not isinstance(current, dict):
            raise CliError(f"Cannot assign nested key {segment!r} inside a non-object payload.")
        if is_last:
            current[segment] = value
            return
        if segment not in current or current[segment] is None:
            current[segment] = ensure_container_for_segment(next_segment)
        current = current[segment]


def merge_object_payload(base: Any, extra: Any, *, source_name: str) -> Any:
    if base is None:
        return extra
    if not isinstance(base, dict) or not isinstance(extra, dict):
        raise CliError(f"{source_name} can only be combined with an object JSON payload.")
    merged = dict(base)
    merged.update(extra)
    return merged


def load_json_file(path: str) -> Any:
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def load_json_text(raw: str) -> Any:
    return json.loads(raw)


def build_json_body(
    *,
    body_file: str | None = None,
    body_json: str | None = None,
    overrides: list[str] | None = None,
) -> Any:
    body: Any = None
    if body_file:
        body = merge_object_payload(body, load_json_file(body_file), source_name="--body-file")
    if body_json:
        body = merge_object_payload(body, load_json_text(body_json), source_name="--body-json")
    if overrides:
        if body is None:
            body = {}
        if not isinstance(body, dict):
            raise CliError("Dotted --set overrides require the request body to be a JSON object.")
        for item in overrides:
            key, raw_value = parse_key_value(item, option_name="--set")
            set_nested_value(body, key, parse_value(raw_value))
    return body


def stringify_query_value(value: Any) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=False, separators=(",", ":"))
    return str(value)


def encode_query(query_items: list[tuple[str, Any]] | None) -> str:
    if not query_items:
        return ""
    pairs: list[tuple[str, str]] = []
    for key, value in query_items:
        if value is None:
            continue
        if isinstance(value, (list, tuple)):
            for item in value:
                pairs.append((key, stringify_query_value(item)))
        else:
            pairs.append((key, stringify_query_value(value)))
    return urllib.parse.urlencode(pairs)


def encode_path_value(value: str) -> str:
    return urllib.parse.quote(value, safe="")


def expand_path_template(path: str, path_params: dict[str, str]) -> str:
    missing: list[str] = []

    def replace(match: re.Match[str]) -> str:
        key = match.group(1)
        if key not in path_params:
            missing.append(key)
            return match.group(0)
        return encode_path_value(path_params[key])

    expanded = PATH_PARAMETER_RE.sub(replace, path)
    if missing:
        joined = ", ".join(sorted(missing))
        raise CliError(f"Missing required --path-param values for: {joined}")
    return expanded


def resolve_base_urls(args: Any) -> dict[str, str]:
    legacy_openai = args.api_base or os.environ.get("PPIO_MODEL_API_BASE")
    return {
        "openai": args.openai_base or os.environ.get("PPIO_MODEL_OPENAI_BASE") or legacy_openai or DEFAULT_BASES["openai"],
        "openapi": args.openapi_base or os.environ.get("PPIO_MODEL_OPENAPI_BASE") or DEFAULT_BASES["openapi"],
        "v3": args.v3_base or os.environ.get("PPIO_MODEL_V3_BASE") or DEFAULT_BASES["v3"],
    }


def resolve_url(base_url: str, path: str) -> str:
    if path.startswith("http://") or path.startswith("https://"):
        return path
    return f"{base_url.rstrip('/')}/{path.lstrip('/')}"


def build_operation_url(spec: OperationSpec, args: Any) -> str:
    base_urls = resolve_base_urls(args)
    path_params = parse_path_parameters(getattr(args, "path_param", None))
    return resolve_url(base_urls[spec.base], expand_path_template(spec.path, path_params))


def build_request_url(args: Any) -> str:
    if args.path.startswith("http://") or args.path.startswith("https://"):
        return args.path
    base_urls = resolve_base_urls(args)
    base_url = base_urls[args.base_family]
    path_params = parse_path_parameters(getattr(args, "path_param", None))
    return resolve_url(base_url, expand_path_template(args.path, path_params))


def encode_multipart(fields: list[tuple[str, str]], files: list[tuple[str, Path]]) -> tuple[str, bytes]:
    boundary = f"ppio-model-api-{secrets.token_hex(12)}"
    chunks: list[bytes] = []
    for key, value in fields:
        chunks.append(f"--{boundary}\r\n".encode("utf-8"))
        chunks.append(f'Content-Disposition: form-data; name="{key}"\r\n\r\n'.encode("utf-8"))
        chunks.append(value.encode("utf-8"))
        chunks.append(b"\r\n")
    for key, path in files:
        filename = path.name
        content_type = mimetypes.guess_type(filename)[0] or "application/octet-stream"
        chunks.append(f"--{boundary}\r\n".encode("utf-8"))
        chunks.append(
            f'Content-Disposition: form-data; name="{key}"; filename="{filename}"\r\n'.encode("utf-8")
        )
        chunks.append(f"Content-Type: {content_type}\r\n\r\n".encode("utf-8"))
        chunks.append(path.read_bytes())
        chunks.append(b"\r\n")
    chunks.append(f"--{boundary}--\r\n".encode("utf-8"))
    return f"multipart/form-data; boundary={boundary}", b"".join(chunks)


def build_request_body(args: Any) -> tuple[bytes | None, str | None]:
    has_json = bool(args.body_file or args.body_json or args.set)
    has_form = bool(args.form or args.file_field)
    if has_json and has_form:
        raise CliError("JSON body options and multipart form options cannot be combined in one request.")
    if has_form:
        fields = parse_form_fields(args.form)
        files = parse_file_fields(args.file_field)
        if not fields and not files:
            return None, None
        content_type, body = encode_multipart(fields, files)
        return body, content_type
    if has_json:
        payload = build_json_body(body_file=args.body_file, body_json=args.body_json, overrides=args.set)
        if payload is None:
            return None, None
        return json.dumps(payload, ensure_ascii=False).encode("utf-8"), "application/json"
    return None, None


def parse_http_error(error: urllib.error.HTTPError) -> str:
    raw_error = error.read().decode("utf-8", errors="replace")
    try:
        payload: Any = json.loads(raw_error)
    except json.JSONDecodeError:
        payload = raw_error or error.reason
    return json.dumps(payload, ensure_ascii=False)


def request_http(
    *,
    method: str,
    url: str,
    api_key: str,
    timeout: float,
    query_items: list[tuple[str, Any]] | None = None,
    body: bytes | None = None,
    content_type: str | None = None,
) -> tuple[bytes, Message]:
    encoded_query = encode_query(query_items)
    if encoded_query:
        separator = "&" if "?" in url else "?"
        url = f"{url}{separator}{encoded_query}"
    headers = {"Authorization": f"Bearer {api_key}"}
    if content_type:
        headers["Content-Type"] = content_type
    request = urllib.request.Request(url=url, data=body, headers=headers, method=method.upper())
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return response.read(), response.headers
    except urllib.error.HTTPError as error:
        raise CliError(f"HTTP {error.code} for {method.upper()} {url}: {parse_http_error(error)}") from error
    except urllib.error.URLError as error:
        raise CliError(f"Request failed for {method.upper()} {url}: {error.reason}") from error


def decode_response_body(raw: bytes, headers: Message) -> Any:
    if not raw:
        return {}
    content_type = headers.get_content_type()
    charset = headers.get_content_charset() or "utf-8"
    if content_type.endswith("/json") or content_type == "application/problem+json":
        decoded = raw.decode(charset, errors="replace")
        try:
            return json.loads(decoded)
        except json.JSONDecodeError:
            return {"raw": decoded}
    try:
        decoded = raw.decode(charset)
    except UnicodeDecodeError:
        return {
            "contentType": content_type,
            "rawBase64": base64.b64encode(raw).decode("ascii"),
        }
    try:
        return json.loads(decoded)
    except json.JSONDecodeError:
        return {"raw": decoded, "contentType": content_type}


def format_saved_output(path: Path, headers: Message, raw: bytes) -> dict[str, Any]:
    return {
        "savedTo": str(path),
        "bytes": len(raw),
        "contentType": headers.get_content_type(),
    }


def iter_media_candidates(payload: Any, path: tuple[str, ...] = ()) -> list[tuple[tuple[str, ...], str]]:
    candidates: list[tuple[tuple[str, ...], str]] = []
    if isinstance(payload, dict):
        for key, value in payload.items():
            candidates.extend(iter_media_candidates(value, path + (str(key),)))
        return candidates
    if isinstance(payload, list):
        for index, value in enumerate(payload):
            candidates.extend(iter_media_candidates(value, path + (str(index),)))
        return candidates
    if isinstance(payload, str) and payload.startswith(("http://", "https://")) and is_media_candidate_path(path):
        candidates.append((path, payload))
    return candidates


def is_media_candidate_path(path: tuple[str, ...]) -> bool:
    segments = [segment.lower() for segment in path if not segment.isdigit()]
    if not segments:
        return False
    for segment in segments:
        if segment in EXACT_MEDIA_HINTS:
            return True
        if segment.endswith(("_url", "_urls", "_uri", "_uris", "_file", "_files")) and any(
            token in segment for token in MEDIA_HINT_TOKENS
        ):
            return True
        if any(token in segment for token in MEDIA_HINT_TOKENS):
            return True
    last = segments[-1]
    if last in {"url", "urls"}:
        return any(segment in {"result", "results", "output", "outputs"} for segment in segments[:-1])
    return False


def parse_content_disposition_filename(header_value: str | None) -> str | None:
    if not header_value:
        return None
    star_match = re.search(r"filename\\*=UTF-8''([^;]+)", header_value, flags=re.IGNORECASE)
    if star_match:
        return urllib.parse.unquote(star_match.group(1).strip())
    quoted_match = re.search(r'filename=\"([^\"]+)\"', header_value, flags=re.IGNORECASE)
    if quoted_match:
        return quoted_match.group(1).strip()
    plain_match = re.search(r"filename=([^;]+)", header_value, flags=re.IGNORECASE)
    if plain_match:
        return plain_match.group(1).strip().strip('"')
    return None


def sanitize_filename(name: str) -> str:
    sanitized = re.sub(r"[^A-Za-z0-9._-]+", "-", name).strip(".-")
    return sanitized or "artifact"


def guess_extension_from_headers(headers: Message) -> str:
    content_type = headers.get_content_type()
    if content_type == "image/jpeg":
        return ".jpg"
    if content_type == "audio/mpeg":
        return ".mp3"
    return mimetypes.guess_extension(content_type) or ""


def infer_remote_filename(url: str, headers: Message, *, index: int) -> str:
    from_header = parse_content_disposition_filename(headers.get("Content-Disposition"))
    if from_header:
        return sanitize_filename(Path(from_header).name)
    remote_name = urllib.parse.unquote(Path(urllib.parse.urlsplit(url).path).name)
    if remote_name and remote_name not in {".", ".."}:
        suffix = Path(remote_name).suffix
        if suffix:
            return sanitize_filename(remote_name)
    extension = guess_extension_from_headers(headers)
    stem = sanitize_filename(remote_name or f"artifact-{index}")
    if not Path(stem).suffix and extension:
        return f"{stem}{extension}"
    return stem


def unique_path(path: Path) -> Path:
    if not path.exists():
        return path
    stem = path.stem or "artifact"
    suffix = path.suffix
    counter = 2
    while True:
        candidate = path.with_name(f"{stem}-{counter}{suffix}")
        if not candidate.exists():
            return candidate
        counter += 1


def download_media_url(url: str, *, timeout: float) -> tuple[bytes, Message]:
    request = urllib.request.Request(url=url, method="GET")
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return response.read(), response.headers
    except urllib.error.HTTPError as error:
        raise CliError(f"HTTP {error.code} while downloading media {url}: {parse_http_error(error)}") from error
    except urllib.error.URLError as error:
        raise CliError(f"Failed to download media {url}: {error.reason}") from error


def save_media_candidates(payload: Any, target: str, *, timeout: float) -> list[dict[str, Any]]:
    candidates = iter_media_candidates(payload)
    if not candidates:
        raise CliError("No downloadable media URLs were found in the JSON response.")
    target_path = Path(target).expanduser()
    treat_as_directory = len(candidates) > 1 or target.endswith(("/", os.sep)) or target_path.is_dir()
    if len(candidates) > 1 and target_path.exists() and not target_path.is_dir():
        raise CliError("--save-media must point to a directory when the response contains multiple artifacts.")
    results: list[dict[str, Any]] = []
    for index, (source_path, url) in enumerate(candidates, start=1):
        raw, headers = download_media_url(url, timeout=timeout)
        if treat_as_directory:
            target_path.mkdir(parents=True, exist_ok=True)
            filename = infer_remote_filename(url, headers, index=index)
            save_path = unique_path(target_path / filename)
        else:
            save_path = target_path
            save_path.parent.mkdir(parents=True, exist_ok=True)
        save_path.write_bytes(raw)
        results.append(
            {
                "sourcePath": ".".join(source_path),
                "sourceUrl": url,
                "savedTo": str(save_path),
                "bytes": len(raw),
                "contentType": headers.get_content_type(),
            }
        )
    return results


def maybe_write_output(raw: bytes, headers: Message, output_file: str | None) -> Any:
    if not output_file:
        return decode_response_body(raw, headers)
    path = Path(output_file).expanduser()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(raw)
    return format_saved_output(path, headers, raw)


def require_api_key(args: Any) -> str:
    api_key = args.api_key or os.environ.get("PPIO_API_KEY")
    if not api_key:
        raise CliError("Missing API key. Set PPIO_API_KEY or pass --api-key.")
    return api_key


def require_timeout(args: Any) -> float:
    if args.timeout is not None:
        return float(args.timeout)
    return float(os.environ.get("PPIO_TIMEOUT", str(DEFAULT_TIMEOUT)))


def execute_operation(spec: OperationSpec, args: Any) -> Any:
    body, content_type = build_request_body(args)
    raw, headers = request_http(
        method=spec.method,
        url=build_operation_url(spec, args),
        api_key=require_api_key(args),
        timeout=require_timeout(args),
        query_items=parse_query_parameters(args.query),
        body=body,
        content_type=content_type,
    )
    decoded = decode_response_body(raw, headers)
    response_payload = format_saved_output(Path(args.output_file).expanduser(), headers, raw) if args.output_file else decoded
    if args.output_file:
        path = Path(args.output_file).expanduser()
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(raw)
    if not args.save_media:
        return response_payload
    saved_media = save_media_candidates(decoded, args.save_media, timeout=require_timeout(args))
    return {"response": response_payload, "savedMedia": saved_media}


def execute_request(args: Any) -> Any:
    body, content_type = build_request_body(args)
    raw, headers = request_http(
        method=args.method,
        url=build_request_url(args),
        api_key=require_api_key(args),
        timeout=require_timeout(args),
        query_items=parse_query_parameters(args.query),
        body=body,
        content_type=content_type,
    )
    decoded = decode_response_body(raw, headers)
    response_payload = format_saved_output(Path(args.output_file).expanduser(), headers, raw) if args.output_file else decoded
    if args.output_file:
        path = Path(args.output_file).expanduser()
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(raw)
    if not args.save_media:
        return response_payload
    saved_media = save_media_candidates(decoded, args.save_media, timeout=require_timeout(args))
    return {"response": response_payload, "savedMedia": saved_media}


def print_output(payload: Any) -> None:
    print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))


def fail(error: Exception) -> int:
    print(f"Error: {error}", file=sys.stderr)
    return 1
