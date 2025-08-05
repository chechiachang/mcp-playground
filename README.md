### Demonstration of LLM Agent with MCP

https://openai.github.io/openai-agents-python/mcp/

### Requirements

```
uv sync
```

### prepare .env

```
# Azure OpenAI API Configuration
AZURE_OPENAI_API_KEY=
OPENAI_API_VERSION=
AZURE_OPENAI_ENDPOINT=
OPENAI_MODEL= gpt-4o

# Firecrawl Configuration
FIRECRAWL_API_KEY=

# Langfuse
LANGFUSE_PUBLIC_KEY="pk-..."
LANGFUSE_SECRET_KEY="sk-..."
LANGFUSE_HOST="..."
```

### Run

```bash
uv run chainlit run main.py
```

### Lint

```bash
make lint type
```