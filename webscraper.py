import asyncio
import aiohttp
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig
from crawl4ai.content_filter_strategy import PruningContentFilter
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator
import os

class WebScraper:
    def __init__(self, threshold=0.45, threshold_type="dynamic", min_word_threshold=5):
        # Настройка фильтра обрезки контента
        self.prune_filter = PruningContentFilter(
            threshold=threshold,
            threshold_type=threshold_type,
            min_word_threshold=min_word_threshold
        )
        # Настройка генератора Markdown с фильтром
        self.md_generator = DefaultMarkdownGenerator(content_filter=self.prune_filter)
        # Конфигурация запуска краулера
        self.config = CrawlerRunConfig(markdown_generator=self.md_generator)
        # OpenAI API ключ
        self.llm_api_key = os.getenv("OPENAI_API_KEY")
        self.llm_endpoint = "https://api.openai.com/v1/chat/completions"

    async def fetch_markdown(self, url):
        async with AsyncWebCrawler() as crawler:
            result = await crawler.arun(url=url, config=self.config)
            return result.markdown

    async def query_llm(self, markdown, user_prompt):
        headers = {
            "Authorization": f"Bearer {self.llm_api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "gpt-4o",  # Или "gpt-3.5-turbo", если gpt-4 недоступен
            "messages": [{"role": "user", "content": f"{user_prompt}\n\n{markdown}"}]
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(self.llm_endpoint, headers=headers, json=payload) as response:
                if response.status != 200:
                    error_text = await response.text()
                    raise Exception(f"Ошибка LLM API: {response.status}, {error_text}")
                return await response.json()

    async def parse_website(self, url, user_prompt):
        markdown = await self.fetch_markdown(url)
        result = await self.query_llm(markdown, user_prompt)
        return result

    def run(self, url, user_prompt):
        return asyncio.run(self.parse_website(url, user_prompt))
