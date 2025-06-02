import openai


class SummarizerAgent:
    """
    AnalysisAgentの結果と元テキストをもとに、要約文章を生成するエージェント
    """
    def __init__(self, model: str = "gpt-4o"):
        self.model = model

    async def run(self, text: str, analysis: dict) -> str:
        """
        textとanalysis（感情・キーワード）を受け取り、要約を生成して返す
        """
        sentiment = analysis.get("sentiment", "不明")
        keywords = analysis.get("keywords", [])

        prompt = (
            "以下の文章を要約してください。\n"
            f"文章のトーン: {sentiment}\n"
            f"抽出されたキーワード: {', '.join(keywords)}\n\n"
            "文章:\n"
            f"{text}\n\n"
            "要約（200文字以内、日本語）:"
        )

        client = openai.AsyncClient()

        response = await client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "あなたは優秀な要約ライターです。"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5,
            max_tokens=300
        )

        summary = response.choices[0].message.content.strip()
        return summary
