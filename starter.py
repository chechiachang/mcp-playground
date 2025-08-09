import chainlit as cl


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
            command="code",
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
            message="使用立法院 mcp api 查詢法案資料，列出前五筆。輸出格式：###法案列表 1. 2. 3. 4. 5.",
            icon="https://upload.wikimedia.org/wikipedia/commons/8/84/ROC_Legislative_Yuan_Seal.svg"
        )
    ]
