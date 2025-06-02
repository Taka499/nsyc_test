import openai


class AnalysisAgent:
    """
    取得したテキストに対して、感情分析やキーワード抽出を行うエージェント
    """
    def __init__(self, model: str = "gpt-4o"):
        self.model = model

    async def run(self, text: str) -> dict:
        """
        textを受け取り、OpenAI API に感情分析とキーワード抽出を指示
        レスポンスとして辞書で返す (例: {"sentiment": "...", "keywords": [...]})
        """
        prompt = (
            "以下の文章を解析してください。\n"
            "1. 全体を要約せずに、文章のトーン（ポジティブ、ニュートラル、ネガティブのいずれか）を返してください。\n"
            "2. 文章のキーワードを3つ抽出してください。\n\n"
            f"文章:\n{text}\n"
            "\n"
            "出力形式:\n"
            "{\n"
            '  "sentiment": "ポジティブ など",\n'
            '  "keywords": ["キーワード1", "キーワード2", "キーワード3"]\n'
            "}"
        )

        client = openai.AsyncClient()

        # 非同期でChatCompletionを呼び出す
        response = await client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "あなたは文章解析の専門家です。"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.0
        )
        # レスポンスからJSON的な文字列を抜き出し、Pythonの辞書に変換
        content = response.choices[0].message.content.strip()
        # 簡易的に eval で辞書化（実運用では安全な JSON パーサーを使うことを推奨）
        try:
            result_dict = eval(content)
        except Exception as e:
            # パースに失敗した場合は、空の辞書を返す
            print("AnalysisAgent: レスポンスのパースに失敗:", e)
            result_dict = {}

        return result_dict
