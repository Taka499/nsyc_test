import os
import asyncio
import aiohttp
import openai
from dotenv import load_dotenv

from agents.scraper_agent import ScraperAgent
from agents.analysis_agent import AnalysisAgent
from agents.summarizer_agent import SummarizerAgent


# 環境変数からOpenAI APIキーを取得
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


class Orchestrator:
    """
    ScraperAgent → AnalysisAgent → SummarizerAgent を呼び出し、
    複数URLを並列に処理するオーケストレーター
    """
    def __init__(self):
        # aiohttpのClientSessionを作成してScraperAgentに渡す
        # self.session = aiohttp.ClientSession()
        # self.scraper = ScraperAgent(self.session)
        # self.analyzer = AnalysisAgent()
        # self.summarizer = SummarizerAgent()
        pass

    async def process_url(self, url: str) -> dict:
        """
        1つのURLに対して、①スクレイピング → ②解析 → ③要約 を順に実行
        return: {"url": url, "analysis": {...}, "summary": "..."}
        """
        # ① ScraperAgent: 記事本文を取得
        print(f"Starting scraping for {url} ...")
        text = await self.scraper.run(url)
        print(f"Scraping completed for {url}. Text length: {len(text)}")

        # ② AnalysisAgent: 感情分析・キーワード抽出
        print(f"Starting analysis for {url} ...")
        analysis_result = await self.analyzer.run(text)
        print(f"Analysis completed for {url}. Result: {analysis_result}")

        # ③ SummarizerAgent: 要約生成
        print(f"Starting summarization for {url} ...")
        summary_text = await self.summarizer.run(text, analysis_result)
        print(f"Summarization completed for {url}.")

        return {
            "url": url,
            "analysis": analysis_result,
            "summary": summary_text
        }

    async def run(self, urls: list[str]) -> list[dict]:
        """
        複数URLを並列で処理し、結果をリストで返す
        """
        async with aiohttp.ClientSession() as session:
            # aiohttpのClientSessionを作成してScraperAgentに渡す
            self.scraper = ScraperAgent(session)
            self.analyzer = AnalysisAgent()
            self.summarizer = SummarizerAgent()
            tasks = [self.process_url(u) for u in urls]
            results = await asyncio.gather(*tasks, return_exceptions=False)
            # await self.session.close()
            return results


# エントリポイント
async def main():
    # テスト用に複数URLを並列処理
    urls_to_process = [
        "https://newspicks.com/news/14296399/body/?ref=index",
        "https://newspicks.com/news/14298202/?block=headline&ref=index"
    ]
    orchestrator = Orchestrator()
    results = await orchestrator.run(urls_to_process)

    # 結果を出力
    for res in results:
        print("==========")
        print(f"URL: {res['url']}")
        print("分析結果:", res["analysis"])
        print("要約:", res["summary"])
        print("==========\n")


if __name__ == "__main__":
    # Windowsや他環境でも動くように、イベントループを取得して実行
    asyncio.run(main())
