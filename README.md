# PPIO Model API Skill

[![License: MIT](https://img.shields.io/badge/License-MIT-22C55E)](https://opensource.org/licenses/MIT)
[![Stage: Alpha](https://img.shields.io/badge/Stage-Alpha-F59E0B)](https://github.com/Nishikori-Yui/ppio-model-api-skills)

[简体中文](README.zh-CN.md)

## Overview

This repository provides a Python CLI tool for wrapping the full official PPIO model API surface. It can be used directly from the command line or invoked by AI assistants such as Claude Code and Codex.

The repository covers the official model API families under `https://ppio.com/docs/models/`:

- base account and billing endpoints,
- OpenAI-compatible LLM endpoints,
- batch inference and file management,
- image generation and editing endpoints,
- video generation endpoints,
- audio generation and transcription endpoints,
- web search,
- async task lookup.

Read-only discovery remains the default operating mode. Billable generation and inference requests stay explicit.

## Repository Layout

- `skills/ppio-model-api/`: the skill package, including metadata, references, and the modular CLI package.
- `skills/ppio-model-api/scripts/ppio_models.py`: thin entrypoint for the grouped CLI.
- `skills/ppio-model-api/scripts/ppio_model_api/`: modular runtime package.
- `skills/ppio-model-api/scripts/ppio_model_api/catalog/`: grouped endpoint declarations split by API family and provider series.

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/Nishikori-Yui/ppio-model-api-skills.git
cd ppio-model-api-skills
```

### 2. Configure API Key

Create `.env` from the example file:

```bash
cp .env.example .env
```

Edit `.env` and set your API key, or export it directly:

```bash
export PPIO_API_KEY="your-api-key"
```

### 3. Run Commands

```bash
# Print the wrapped official command catalog
python3 skills/ppio-model-api/scripts/ppio_models.py catalog

# Query account data
python3 skills/ppio-model-api/scripts/ppio_models.py base user-info
python3 skills/ppio-model-api/scripts/ppio_models.py base bill-list \
  --query cycleType='"Day"' \
  --query productCategory='"llm"' \
  --query pageSize=20

# List and inspect models
python3 skills/ppio-model-api/scripts/ppio_models.py llm list-models
python3 skills/ppio-model-api/scripts/ppio_models.py llm retrieve-model --path-param model=qwen/qwen3-32b

# Run an explicit image request
python3 skills/ppio-model-api/scripts/ppio_models.py image seedream-4.5 --body-file /absolute/path/seedream-45.json

# Run an explicit video request
python3 skills/ppio-model-api/scripts/ppio_models.py video unified-video-generation --body-file /absolute/path/video.json

# Save a generated image or task result to a chosen local path
python3 skills/ppio-model-api/scripts/ppio_models.py image seedream-4.5 \
  --body-file /absolute/path/seedream-45.json \
  --save-media /absolute/path/output.png
python3 skills/ppio-model-api/scripts/ppio_models.py audio minimax-speech-02-turbo \
  --body-file /absolute/path/audio.json \
  --save-media /absolute/path/output.mp3
python3 skills/ppio-model-api/scripts/ppio_models.py tasks async-task-result \
  --query task_id='"task-id"' \
  --save-media /absolute/path/output.mp4

# Upload a batch input file
python3 skills/ppio-model-api/scripts/ppio_models.py batch upload-batch-input-file \
  --form purpose=batch \
  --file-field file=/absolute/path/batch.jsonl
```

The CLI automatically loads `.env` files from the skill directory or parent directories. The OpenAI-compatible base keeps the legacy `PPIO_MODEL_API_BASE` environment variable for backward compatibility, and the grouped runtime also supports dedicated overrides for the `openai`, `openapi`, and `v3` API families.

When a generation or task-result response includes downloadable media URLs, `--save-media PATH` downloads them locally. If the response contains one artifact, `PATH` may be a file path; if it contains multiple artifacts, `PATH` is treated as a directory and filenames are inferred from the remote response.

## Command Groups

- `catalog`: print the wrapped official endpoint registry.
- `base`: account information and billing lookups.
- `llm`: model listing, model retrieval, embeddings, rerank, chat completions, and completions.
- `batch`: batch requests and file operations.
- `image`: documented image generation and editing endpoints.
- `video`: documented video generation endpoints.
- `audio`: documented audio generation and transcription endpoints.
- `search`: web search.
- `tasks`: async task result lookups.
- `request`: generic fallback for relative or absolute endpoints.

Legacy flat commands such as `models`, `model`, `chat`, and `embeddings` remain available for compatibility.

## Architecture

The runtime is intentionally modular:

- endpoint declarations are grouped by API family and provider series instead of being kept in one script,
- parser construction is generated from those grouped declarations,
- request building, environment loading, path parameter expansion, query encoding, JSON payload assembly, and multipart uploads are handled by shared standard-library helpers,
- the entrypoint script remains thin so future endpoint additions mostly touch the registry modules and reference notes.

## Resources

- [Model Service API Reference](https://ppio.com/docs/models/reference-authentication)

## License

This repository is released under the MIT License.
