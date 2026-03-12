---
name: ppio-model-api
description: Manage the official PPIO model-service API through an OpenAI-compatible interface. Use when Codex needs to verify PPIO model authentication, list available models, inspect a model by ID, send explicit chat or embedding requests, or call additional documented model endpoints through a generic request wrapper.
---

# PPIO Model API

## Overview

Use only the official PPIO model API and official PPIO model documentation for this skill.

Default to read-only discovery commands. Treat billable LLM, image, video, audio, and web-search requests as explicit-intent operations.

## Quick Start

1. Create `.env` from `.env.example`, or ensure `PPIO_API_KEY` is exported.
2. Use `scripts/ppio_models.py` for all API calls.
3. Run `catalog` first when you need to inspect the grouped command surface.
4. Read `references/ppio-model-api.md` when you need endpoint families, request patterns, or environment override rules.
5. Prefer the generic `request` subcommand only when the wrapped commands do not cover the needed endpoint.

## Workflow

### Discover State

- Query account state or bills:
  ```bash
  python3 skills/ppio-model-api/scripts/ppio_models.py base user-info
  python3 skills/ppio-model-api/scripts/ppio_models.py base bill-list \
    --query cycleType='"Day"' \
    --query productCategory='"llm"' \
    --query pageSize=20
  ```
- List wrapped commands:
  ```bash
  python3 skills/ppio-model-api/scripts/ppio_models.py catalog
  ```
- Discover and inspect models:
  ```bash
  python3 skills/ppio-model-api/scripts/ppio_models.py llm list-models
  python3 skills/ppio-model-api/scripts/ppio_models.py llm retrieve-model --path-param model=qwen/qwen3-32b
  ```

### Send Explicit Inference Requests

- Create a chat completion from a JSON body file:
  ```bash
  python3 skills/ppio-model-api/scripts/ppio_models.py llm create-chat-completion --body-file /absolute/path/chat.json
  ```
- Create embeddings from inline overrides when the body is small:
  ```bash
  python3 skills/ppio-model-api/scripts/ppio_models.py llm create-embeddings \
    --set model='"BAAI/bge-m3"' \
    --set input='"hello world"'
  ```
- Call an image endpoint:
  ```bash
  python3 skills/ppio-model-api/scripts/ppio_models.py image seedream-4.5 \
    --body-file /absolute/path/seedream-45.json \
    --save-media /absolute/path/output.png
  ```
- Call a video endpoint:
  ```bash
  python3 skills/ppio-model-api/scripts/ppio_models.py video unified-video-generation --body-file /absolute/path/video.json
  ```
- Save a synthesized audio artifact directly:
  ```bash
  python3 skills/ppio-model-api/scripts/ppio_models.py audio minimax-speech-02-turbo \
    --body-file /absolute/path/audio.json \
    --save-media /absolute/path/output.mp3
  ```
- Save a completed async media result:
  ```bash
  python3 skills/ppio-model-api/scripts/ppio_models.py tasks async-task-result \
    --query task_id='"task-id"' \
    --save-media /absolute/path/output.mp4
  ```
- Upload a batch input file:
  ```bash
  python3 skills/ppio-model-api/scripts/ppio_models.py batch upload-batch-input-file \
    --form purpose=batch \
    --file-field file=/absolute/path/batch.jsonl
  ```

When sending billable requests, confirm the model ID first instead of guessing.

## Safety Rules

- Stay read-only unless the user explicitly asks for an inference or generation request.
- Surface the raw API error body when a request fails; do not paraphrase away the remote error.
- Do not store API keys or tokens in repository files.
- Keep secrets only in the local `.env`, the shell environment, or one-shot flags.
- Keep request specs as temporary local JSON files or inline `--set` overrides.
- Prefer `--body-file` for complex nested payloads.
- Use `--file-field` only when the official docs require multipart uploads.
- Use `--path-param` for templated URL segments such as `{model}`, `{batch_id}`, or `{file_id}`.
- Use `--save-media /absolute/path/...` when you want the generated image, video, or audio artifact downloaded locally instead of only printing the returned URL.

## Generic Request Fallback

Use `request` when the official docs expose an endpoint that the wrapper does not yet cover:

```bash
python3 skills/ppio-model-api/scripts/ppio_models.py request GET /models --base-family openai
python3 skills/ppio-model-api/scripts/ppio_models.py request POST /web-search --base-family v3 --body-file /absolute/path/search.json
```

Use relative paths under the selected documented API base by default. Pass an absolute URL only when the upstream API introduces a documented path outside the current base families.

## Resources

### `scripts/ppio_models.py`

A thin entrypoint that loads the modular grouped CLI runtime.

### `references/ppio-model-api.md`

Read this file when you need the grouped endpoint map, base-family conventions, or the compatibility story for legacy aliases.
