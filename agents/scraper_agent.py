import aiohttp
from bs4 import BeautifulSoup


class ScraperAgent:
    """
    Webページを非同期でスクレイピングし、本文テキストを抽出するエージェント
    """
    def __init__(self, session: aiohttp.ClientSession):
        self.session = session

    async def fetch_html(self, url: str) -> str:
        """
        URLからHTMLを非同期取得
        """
        async with self.session.get(url) as response:
            response.raise_for_status()
            return await response.text()

    def parse_text(self, html: str) -> str:
        """
        BeautifulSoupを使い、<p>タグのテキストを結合して返す
        """
        soup = BeautifulSoup(html, "html.parser")
        # 本文抽出の例として、<p>タグのテキストをすべて連結
        paragraphs = soup.find_all("p")
        text = "\n".join(p.get_text(separator=" ", strip=True) for p in paragraphs)
        return text

    async def run(self, url: str) -> str:
        """
        実行メソッド。URLを受け取り、生テキストを返す
        """
        html = await self.fetch_html(url)
        text = self.parse_text(html)
        return text
