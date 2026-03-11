# PPIO Model API Reference

## Sources

- Authentication: https://ppio.com/docs/models/reference-authentication
- Model list: https://ppio.com/docs/models/reference-model-list
- Model retrieve: https://ppio.com/docs/models/reference-model-retrieve
- Chat completions: https://ppio.com/docs/models/reference-llm-chat-completions
- Embeddings: https://ppio.com/docs/models/reference-embedding

## Authentication

- Header: `Authorization: Bearer <PPIO_API_KEY>`
- Default base URL: `https://api.ppio.com/openai/v1`

## Wrapped Endpoints

- `GET /models`
- `GET /models/{model}`
- `POST /chat/completions`
- `POST /embeddings`

## Request Notes

### List Models

- No request body
- Use this first to confirm canonical model IDs

### Retrieve Model

- Path parameter: `model`
- Use URL encoding for model IDs that contain `/`

### Chat Completions

Minimum practical body:

```json
{
  "model": "qwen/qwen3-32b",
  "messages": [
    {
      "role": "user",
      "content": "Hello"
    }
  ]
}
```

### Embeddings

Minimum practical body:

```json
{
  "model": "BAAI/bge-m3",
  "input": "hello world"
}
```

## Fallback Rule

Use the generic `request` command for other documented PPIO model endpoints that are not wrapped yet. Keep relative paths under the default OpenAI-compatible API base unless the official docs require an absolute URL on another documented host.
