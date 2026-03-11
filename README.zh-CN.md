# PPIO Model API 技能

[![License: MIT](https://img.shields.io/badge/License-MIT-22C55E)](https://opensource.org/licenses/MIT)
[![Stage: Alpha](https://img.shields.io/badge/Stage-Alpha-F59E0B)](https://github.com/Nishikori-Yui/ppio-model-api-skills)

[English](README.md)

## 概览

这个子仓库封装了一个 Codex skill，用于通过 PPIO 官方模型 API 发现和调用模型服务，命令面兼容 OpenAI 风格接口。

仓库围绕一条尽量收敛的工作流设计：

- 验证鉴权配置
- 查询可用模型
- 按模型 ID 查询单个模型
- 仅在用户明确要求时发起推理请求
- 对未封装的官方接口使用通用请求命令

## 仓库结构

- `skills/ppio-model-api/`：skill 本体，包含元数据、参考资料和脚本

## 快速开始

1. 从示例创建本地环境文件：

```bash
cp .env.example .env
```

2. 在 `.env` 中填入 API Key，或直接导出环境变量：

```bash
export PPIO_API_KEY="your-api-key"
```

3. 查询可用模型：

```bash
python3 skills/ppio-model-api/scripts/ppio_models.py models
```

4. 查询单个模型：

```bash
python3 skills/ppio-model-api/scripts/ppio_models.py model --model-id "qwen/qwen3-32b"
```

CLI 会自动加载就近的 `.env` 文件，不需要手工 `source`。

## 参考资料

- [PPIO 模型 API 参考](https://ppio.com/docs/models/reference-authentication)

## 许可证

本仓库采用 MIT License。
