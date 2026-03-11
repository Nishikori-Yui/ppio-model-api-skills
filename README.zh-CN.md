# PPIO Model API 技能

[![License: MIT](https://img.shields.io/badge/License-MIT-22C55E)](https://opensource.org/licenses/MIT)
[![Stage: Alpha](https://img.shields.io/badge/Stage-Alpha-F59E0B)](https://github.com/Nishikori-Yui/ppio-model-api-skills)

[English](README.md)

## 概览

这个子仓库提供了一个 Python CLI 工具，用于通过 PPIO 官方模型 API 发现和调用模型服务，命令面兼容 OpenAI 风格接口。它可以由 AI 助手（如 Claude Code、Codex）直接调用或从命令行使用。

仓库围绕一条尽量收敛的工作流设计：

- 验证鉴权配置
- 查询可用模型
- 按模型 ID 查询单个模型
- 仅在用户明确要求时发起推理请求
- 对未封装的官方接口使用通用请求命令

## 仓库结构

- `skills/ppio-model-api/`：skill 本体，包含元数据、参考资料和脚本

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
# 查询可用模型
python3 skills/ppio-model-api/scripts/ppio_models.py models

# 查询指定模型
python3 skills/ppio-model-api/scripts/ppio_models.py model --model-id "qwen/qwen3-32b"

# 发送聊天请求
python3 skills/ppio-model-api/scripts/ppio_models.py chat --body-json '{"model":"qwen/qwen3-32b","messages":[{"role":"user","content":"hello"}]}'
```

CLI 会自动加载 skill 目录或父目录中的 `.env` 文件。

## 参考资料

- [模型服务 API 手册](https://ppio.com/docs/models/reference-authentication)

## 许可证

本仓库采用 MIT License。
