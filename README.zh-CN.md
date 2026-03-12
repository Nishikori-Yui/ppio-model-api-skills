# PPIO Model API 技能

[![License: MIT](https://img.shields.io/badge/License-MIT-22C55E)](https://opensource.org/licenses/MIT)
[![Stage: Alpha](https://img.shields.io/badge/Stage-Alpha-F59E0B)](https://github.com/Nishikori-Yui/ppio-model-api-skills)

[English](README.md)

## 概览

这个子仓库提供了一个 Python CLI 工具，用于封装 PPIO 官方模型 API 的完整公开能力。它可以由 AI 助手（如 Claude Code、Codex）直接调用，也可以直接从命令行使用。

仓库覆盖 `https://ppio.com/docs/models/` 下的官方能力族：

- 基础账户与账单接口
- OpenAI 兼容的大语言模型接口
- 批量推理与文件管理
- 图像生成与编辑
- 视频生成
- 音频生成与转写
- 联网搜索
- 异步任务查询

默认仍以只读发现类命令为主，所有计费推理或生成请求都应建立在明确用户意图之上。

## 仓库结构

- `skills/ppio-model-api/`：skill 本体，包含元数据、参考资料和模块化 CLI
- `skills/ppio-model-api/scripts/ppio_models.py`：分组 CLI 的薄入口
- `skills/ppio-model-api/scripts/ppio_model_api/`：模块化运行时包
- `skills/ppio-model-api/scripts/ppio_model_api/catalog/`：按 API 家族和模型系列拆分的 endpoint 声明

## 快速开始

### 1. 克隆仓库

```bash
git clone https://github.com/Nishikori-Yui/ppio-model-api-skills.git
cd ppio-model-api-skills
```

### 2. 配置 API Key

从示例文件创建 `.env`：

```bash
cp .env.example .env
```

编辑 `.env` 设置 API key，或直接导出环境变量：

```bash
export PPIO_API_KEY="your-api-key"
```

### 3. 运行命令

```bash
# 打印官方接口封装目录
python3 skills/ppio-model-api/scripts/ppio_models.py catalog

# 查询账户与账单
python3 skills/ppio-model-api/scripts/ppio_models.py base user-info
python3 skills/ppio-model-api/scripts/ppio_models.py base bill-list \
  --query cycleType='"Day"' \
  --query productCategory='"llm"' \
  --query pageSize=20

# 查询模型
python3 skills/ppio-model-api/scripts/ppio_models.py llm list-models
python3 skills/ppio-model-api/scripts/ppio_models.py llm retrieve-model --path-param model=qwen/qwen3-32b

# 发起明确的图像请求
python3 skills/ppio-model-api/scripts/ppio_models.py image seedream-4.5 --body-file /absolute/path/seedream-45.json

# 发起明确的视频请求
python3 skills/ppio-model-api/scripts/ppio_models.py video unified-video-generation --body-file /absolute/path/video.json

# 将生成图片或任务结果保存到指定本地路径
python3 skills/ppio-model-api/scripts/ppio_models.py image seedream-4.5 \
  --body-file /absolute/path/seedream-45.json \
  --save-media /absolute/path/output.png
python3 skills/ppio-model-api/scripts/ppio_models.py audio minimax-speech-02-turbo \
  --body-file /absolute/path/audio.json \
  --save-media /absolute/path/output.mp3
python3 skills/ppio-model-api/scripts/ppio_models.py tasks async-task-result \
  --query task_id='"task-id"' \
  --save-media /absolute/path/output.mp4

# 上传批量推理输入文件
python3 skills/ppio-model-api/scripts/ppio_models.py batch upload-batch-input-file \
  --form purpose=batch \
  --file-field file=/absolute/path/batch.jsonl
```

CLI 会自动加载 skill 目录或父目录中的 `.env` 文件。为兼容旧版本，OpenAI 兼容基地址继续支持 `PPIO_MODEL_API_BASE`；新的分组运行时还额外支持 `openai`、`openapi`、`v3` 三套基地址的单独覆盖。

当生成或任务查询响应中包含可下载的媒体 URL 时，可以使用 `--save-media PATH` 将产物落到本地。若响应只包含一个产物，`PATH` 可以直接是文件路径；若包含多个产物，则 `PATH` 会按目录处理，并根据远端响应自动推断文件名。

## 命令分组

- `catalog`：打印已封装的官方 endpoint 清单
- `base`：账户与账单查询
- `llm`：模型列表、模型检索、embeddings、rerank、chat completions、completions
- `batch`：批量推理与文件操作
- `image`：官方图像生成与编辑接口
- `video`：官方视频生成接口
- `audio`：官方音频生成与转写接口
- `search`：联网搜索
- `tasks`：异步任务结果查询
- `request`：相对路径或绝对 URL 的通用兜底请求

为了兼容已有调用方式，`models`、`model`、`chat`、`embeddings` 这几个旧别名仍会保留。

## 架构说明

新的运行时采用模块化设计：

- endpoint 声明按 API 家族与模型系列拆分，不再放在一个脚本里
- 参数解析器根据这些声明自动生成
- 环境变量加载、路径参数展开、查询串编码、JSON 负载拼装、multipart 上传都下沉到共享标准库工具层
- 入口脚本保持很薄，未来补新接口时主要修改 registry 模块和参考文档即可

## 参考资料

- [模型服务 API 手册](https://ppio.com/docs/models/reference-authentication)

## 许可证

本仓库采用 MIT License。
