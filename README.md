# PPIO Model API Skill

[![License: MIT](https://img.shields.io/badge/License-MIT-22C55E)](https://opensource.org/licenses/MIT)
[![Stage: Alpha](https://img.shields.io/badge/Stage-Alpha-F59E0B)](https://github.com/Nishikori-Yui/ppio-model-api-skills)

[简体中文](README.zh-CN.md)

## Overview

This repository packages a Codex skill for discovering and calling the official PPIO model-service API with an OpenAI-compatible command surface.

The repository is designed around a compact workflow:

- verify authentication setup,
- discover available models,
- inspect a model by identifier,
- send explicit inference requests only when the user asks for them,
- fall back to a generic request command for additional documented endpoints.

## Repository Layout

- `skills/ppio-model-api/`: the skill package, including metadata, references, and automation scripts.

## Quick Start

1. Create a local environment file from the sample:

```bash
cp .env.example .env
```

2. Fill in your API key in `.env`, or export it directly:

```bash
export PPIO_API_KEY="your-api-key"
```

3. List available models:

```bash
python3 skills/ppio-model-api/scripts/ppio_models.py models
```

4. Inspect a model:

```bash
python3 skills/ppio-model-api/scripts/ppio_models.py model --model-id "qwen/qwen3-32b"
```

The CLI loads a local `.env` file automatically when present and does not require a manual `source` step.

## Resources

- [PPIO Model API Reference](https://ppio.com/docs/models/reference-authentication)

## License

This repository is released under the MIT License.
