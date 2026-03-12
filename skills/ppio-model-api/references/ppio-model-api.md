# PPIO Model API Reference

## Sources

- Official docs root: https://ppio.com/docs/models/
- Official auth page: https://ppio.com/docs/models/reference-authentication
- Official error-code page: https://ppio.com/docs/models/reference-error-code

This reference file was refreshed against the official documentation set on March 12, 2026.

## Runtime Layout

- Entry script: `scripts/ppio_models.py`
- Runtime package: `scripts/ppio_model_api/`
- Grouped endpoint declarations:
  - `catalog/base.py`
  - `catalog/llm.py`
  - `catalog/batch.py`
  - `catalog/image/`
  - `catalog/video/`
  - `catalog/audio/`
  - `catalog/search.py`
  - `catalog/tasks.py`

The grouped runtime is data-driven. Most new endpoint additions should require registry updates rather than parser rewrites.

## Authentication And Base Families

- Header: `Authorization: Bearer <PPIO_API_KEY>`
- Base families:
  - `openai`: `https://api.ppio.com/openai/v1`
  - `openapi`: `https://api.ppio.com/openapi/v1`
  - `v3`: `https://api.ppio.com/v3`
- Environment overrides:
  - `PPIO_MODEL_OPENAI_BASE`
  - `PPIO_MODEL_OPENAPI_BASE`
  - `PPIO_MODEL_V3_BASE`
  - `PPIO_TIMEOUT`
- Compatibility note: `PPIO_MODEL_API_BASE` is preserved as a legacy alias for the `openai` base.

## Wrapped Families

- `base`
  - `GET /v3/user`
  - `GET /openapi/v1/billing/bill/list`
- `llm`
  - `GET /models`
  - `GET /models/{model}`
  - `POST /embeddings`
  - `POST /rerank`
  - `POST /chat/completions`
  - `POST /completions`
- `batch`
  - `POST /batches`
  - `GET /batches`
  - `GET /batches/{batch_id}`
  - `POST /batches/{batch_id}/cancel`
  - `POST /files`
  - `GET /files`
  - `GET /files/{file_id}`
  - `DELETE /files/{file_id}`
  - `GET /files/{file_id}/content`
- `image`
  - Seedream, Jimeng, Qwen Image, Hunyuan, Gemini, GLM, Grok Imagine, and image-tool endpoints
- `video`
  - unified video generation plus Wan, Kling, MiniMax, Vidu, PixVerse, Seedance, Wondershare, Heygen, and Grok families
- `audio`
  - MiniMax speech families plus GLM audio families
- `search`
  - `POST /v3/web-search`
- `tasks`
  - `GET /v3/async/task-result`

## Request Notes

- Use `catalog` to inspect wrapped operations and their grouped names before sending billable requests.
- Use `--path-param key=value` for templated path segments such as `{model}`, `{batch_id}`, or `{file_id}`.
- Use `--query key=value` for documented query parameters.
- Use `--body-file` for nested JSON request bodies.
- Use `--set key=value` for small top-level or dotted-path overrides.
- Use `--form key=value` and `--file-field name=/absolute/path/file` when the official docs require multipart uploads.
- Use `--output-file` when an endpoint returns raw content that should be written to disk instead of printed.
- Use `--save-media /absolute/path/...` when a JSON response includes downloadable image, video, or audio URLs and you want the runtime to fetch them locally.
- `--save-media` treats the target as a file path when exactly one artifact URL is found and as a directory when multiple artifact URLs are found.

## Fallback Rule

Use the generic `request` command only when the official docs add a documented endpoint that is not yet present in the grouped registry. Keep relative paths under the chosen base family unless the official docs require an absolute URL on another documented host.
