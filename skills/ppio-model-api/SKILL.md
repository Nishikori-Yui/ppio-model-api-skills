---
name: ppio-model-api
description: Manage the official PPIO model-service API through an OpenAI-compatible interface. Use when Codex needs to verify PPIO model authentication, list available models, inspect a model by ID, send explicit chat or embedding requests, or call additional documented model endpoints through a generic request wrapper.
---

# PPIO Model API

## Overview

Use only the official PPIO model API and official PPIO model documentation for this skill.

Default to read-only discovery commands. Treat `chat` and `embeddings` as explicit-intent operations because they may incur usage cost.

## Quick Start

1. Create `.env` from `.env.example`, or ensure `PPIO_API_KEY` is exported.
2. Use `scripts/ppio_models.py` for all API calls.
3. Read `references/ppio-model-api.md` when you need endpoint paths, request fields, or example payloads.
4. Prefer the generic `request` subcommand only when the wrapped commands do not cover the needed endpoint.

## Workflow

### Discover Models

- List models first to confirm the exact model ID:
  ```bash
  python3 skills/ppio-model-api/scripts/ppio_models.py models
  ```
- Retrieve one documented model by identifier:
  ```bash
  python3 skills/ppio-model-api/scripts/ppio_models.py model --model-id "qwen/qwen3-32b"
  ```

### Send Explicit Inference Requests

- Create a chat completion from a JSON body file:
  ```bash
  python3 skills/ppio-model-api/scripts/ppio_models.py chat --body-file /absolute/path/chat.json
  ```
- Create embeddings from inline overrides when the body is small:
  ```bash
  python3 skills/ppio-model-api/scripts/ppio_models.py embeddings \
    --set model='"BAAI/bge-m3"' \
    --set input='"hello world"'
  ```

When sending billable requests, confirm the model ID first instead of guessing.

## Safety Rules

- Stay read-only unless the user explicitly asks for an inference request.
- Surface the raw API error body when a request fails; do not paraphrase away the remote error.
- Do not store API keys or tokens in repository files.
- Keep secrets only in the local `.env`, the shell environment, or one-shot flags.
- Keep request specs as temporary local JSON files or inline `--set` overrides.

## Generic Request Fallback

Use `request` when the official docs expose an endpoint that the wrapper does not yet cover:

```bash
python3 skills/ppio-model-api/scripts/ppio_models.py request GET /models
python3 skills/ppio-model-api/scripts/ppio_models.py request POST /chat/completions --body-json '{"model":"qwen/qwen3-32b","messages":[{"role":"user","content":"hello"}]}'
```

Use relative paths under the documented API base by default. Pass an absolute URL only when the upstream API introduces a documented path outside the default base.

## Resources

### `scripts/ppio_models.py`

A standard-library Python CLI wrapper for common PPIO model discovery and inference operations.

### `references/ppio-model-api.md`

Read this file when you need exact documented endpoint paths, core request fields, or example commands derived from the official PPIO documentation.
