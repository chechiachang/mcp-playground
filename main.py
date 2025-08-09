# https://github.com/agentika/agentize/blob/main/examples/mcp_chatbot.py
import os

import chainlit as cl
from agentize.model import get_openai_model
from agentize.utils import configure_langfuse
from agents import Agent
from agents import Runner
from agents import TResponseInputItem
from agents import set_tracing_disabled
from agents.mcp import MCPServerStdio
from agents.mcp import MCPServerStdioParams
from dotenv import find_dotenv
from dotenv import load_dotenv
from loguru import logger

from starter import set_starters


class OpenAIAgent:
    def __init__(self) -> None:
        load_dotenv(find_dotenv(), override=True)
        configure_langfuse()
        self.agent = Agent(
            name="agent",
            instructions="You are a helpful assistant.",
            model=get_openai_model(),
            mcp_servers=[
                # https://github.com/narumiruna/yfinance-mcp
                MCPServerStdio(
                    name="yfinance-mcp",
                    params=MCPServerStdioParams(
                        command="uvx",
                        args=["--from", "git+https://github.com/narumiruna/yfinance-mcp", "yfmcp"],
                    ),
                    client_session_timeout_seconds=20
                ),
                # https://github.com/mendableai/firecrawl-mcp-server
                MCPServerStdio(
                    name="firecrawl-mcp",
                    params=MCPServerStdioParams(
                        command="npx",
                        args=["-y", "firecrawl-mcp"],
                        env={"FIRECRAWL_API_KEY": os.getenv("FIRECRAWL_API_KEY", "")},
                    ),
                    client_session_timeout_seconds=20
                ),
                # https://github.com/narumiruna/ly-mcp
                MCPServerStdio(
                    name="ly-mcp",
                    params=MCPServerStdioParams(
                        command="uvx",
                        args=["--from", "git+https://github.com/narumiruna/ly-mcp", "lymcp"],
                    ),
                    client_session_timeout_seconds=20
                ),
            ],
        )
        self.messages: list[TResponseInputItem] = []

    async def connect(self) -> None:
        logger.info("Connecting to MCP server...")
        for server in self.agent.mcp_servers:
            await server.connect()

    async def cleanup(self) -> None:
        logger.info("Cleaning up MCP server...")
        for server in self.agent.mcp_servers:
            await server.cleanup()

    async def run(self, message: str) -> str:
        self.messages.append(
            {
                "role": "user",
                "content": message,
            }
        )

        result = await Runner.run(starting_agent=self.agent, input=self.messages)
        self.messages = result.to_input_list()

        return str(result.final_output)

@cl.on_app_startup
async def connect() -> None:
    await openai_agent.connect()


@cl.on_app_shutdown
async def cleanup() -> None:
    await openai_agent.cleanup()


@cl.on_message
async def chat(message: cl.Message) -> None:
    content = await openai_agent.run(message.content)
    await cl.Message(content=content).send()

# main
set_tracing_disabled(True)
openai_agent = OpenAIAgent()
