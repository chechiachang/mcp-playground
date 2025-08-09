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

#@cl.password_auth_callback
#def auth_callback(username: str, password: str):
#    if (username, password) == ("coscup", "coscup"):
#        return cl.User(
#            identifier="user", metadata={"role": "user", "provider": "credentials"}
#        )
#    else:
#        return None

@cl.set_starters
async def set_starters():
    return [
        cl.Starter(
            label="取得台積電 TSMC 的公司基本資料、近期股價歷史與新聞",
            message="取得台積電 TSMC 的公司基本資料、近期股價歷史與新聞",
            icon="https://img.favpng.com/2/19/3/scalable-vector-graphics-portable-network-graphics-tsmc-transparency-multi-million-dollar-advocates-forum-png-favpng-9LfgnsLsetKszS1PUh2AHjaJh_t.jpg",
        ),
        cl.Starter(
            label="擷取多檔股票的摘要與新聞，NVDA、TSLA、AAPL、TSMC",
            message="擷取多檔股票的摘要與新聞，NVDA、TSLA、AAPL、TSMC",
            icon="https://png.pngtree.com/element_our/20200609/ourmid/pngtree-rising-arrow-stock-market-image_2231710.jpg",
        ),
        cl.Starter(
            label="股市新聞查詢，firecrawl 爬蟲內容，根據內產生摘要",
            message="""從 yahoo finance 取得台積電 TSMC 的新聞，列出前五筆。
            使用 firecrawl 爬取第一篇新聞，以 markdown 完整印出新聞內容。
            根據爬取新聞內容產生摘要，以 markdown 格式印出摘要。
            輸出格式：###近期新聞列表 1. 2. 3. 4. 5. ###新聞內容 ###摘要""",
            icon="https://raw.githubusercontent.com/mendableai/firecrawl/main/img/firecrawl_logo.png",
        ),
        cl.Starter(
            label="立法院 mcp api 查詢",
            message="使用立法院 mcp api 查詢法案資料，列出前五筆。輸出格式 markdown：###法案列表 1. 2. 3. 4. 5.",
            icon="https://upload.wikimedia.org/wikipedia/commons/8/84/ROC_Legislative_Yuan_Seal.svg"
        ),
        cl.Starter(
            label="列出立法院 mcp 可用的 tool",
            message="列出立法院 mcp 可用的 tool",
            icon="https://upload.wikimedia.org/wikipedia/commons/8/84/ROC_Legislative_Yuan_Seal.svg"
        )
    ]

# main
set_tracing_disabled(True)
openai_agent = OpenAIAgent()
