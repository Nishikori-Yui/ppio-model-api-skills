# PPIO Model API Skill

[![License: MIT](https://img.shields.io/badge/License-MIT-22C55E)](https://opensource.org/licenses/MIT)
[![Stage: Alpha](https://img.shields.io/badge/Stage-Alpha-F59E0B)](https://github.com/Nishikori-Yui/ppio-model-api-skills)

[简体中文](README.zh-CN.md)

## Overview

This repository provides a Python CLI tool for discovering and calling the official PPIO model-service API with an OpenAI-compatible command surface. It can be used directly from the command line or invoked by AI assistants such as Claude Code and Codex.

The repository is designed around a compact workflow:

- verify authentication setup,
- discover available models,
- inspect a model by identifier,
- send explicit inference requests only when the user asks for them,
- fall back to a generic request command for additional documented endpoints.

## Repository Layout

- `skills/ppio-model-api/`: the skill package, including metadata, references, and automation scripts.

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
# List available models
python3 skills/ppio-model-api/scripts/ppio_models.py models

# Inspect a specific model
python3 skills/ppio-model-api/scripts/ppio_models.py model --model-id "qwen/qwen3-32b"

# Send a chat completion
python3 skills/ppio-model-api/scripts/ppio_models.py chat --body-json '{"model":"qwen/qwen3-32b","messages":[{"role":"user","content":"hello"}]}'
```

The CLI automatically loads `.env` files from the skill directory or parent directories.

## Resources

- [Model Service API Reference](https://ppio.com/docs/models/reference-authentication)

## License

This repository is released under the MIT License.
