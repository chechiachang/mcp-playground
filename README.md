### Demonstration of LLM Agent with MCP

https://openai.github.io/openai-agents-python/mcp/

### Requirements

```
uv sync
```

### prepare .env

Create a `.env` file in the root directory of the project with the following content:

##### LLM Provider Configuration

OpenAI API

```
OPENAI_API_KEY=
OPENAI_MODEL=gpt-4.1-mini
```

Or if you are using the Azure OpenAI API, use the following configuration:

```
AZURE_OPENAI_API_KEY=
OPENAI_API_VERSION=
AZURE_OPENAI_ENDPOINT=
OPENAI_MODEL= gpt-4.1-mini
```

Or if you are using the OpenAI SDK Compatible API (ex. Gemini API), use the following configuration:

```
OPENAI_API_KEY=<your-google-api-key>
OPENAI_BASE_URL="https://generativelanguage.googleapis.com/v1beta/openai/"
OPENAI_MODEL="gemini-2.0-flash"
API_TYPE="chat_completions"
OPENAI_AGENTS_DISABLE_TRACING=1 # (Optional) Disable tracing provided by the OpenAI SDK
```

##### (Optional) Firecrawl Configuration

```
# Firecrawl Configuration
FIRECRAWL_API_KEY=
```

##### (Optional) Langfuse Configuration for tracing

```
# Langfuse
LANGFUSE_PUBLIC_KEY="pk-..."
LANGFUSE_SECRET_KEY="sk-..."
LANGFUSE_HOST="..."
```

### Run

```bash
uv run chainlit run main.py
```

### Development

Linting and type checking can be run with:

```bash
make lint type
```