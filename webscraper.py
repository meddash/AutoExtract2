import asyncio
import aiohttp
import argparse
import json
import os
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig
from crawl4ai.content_filter_strategy import PruningContentFilter
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator

class WebScraper:
    def __init__(self, api_key, threshold=0.45, threshold_type="dynamic", min_word_threshold=5):
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
        
        # OpenAI API ключ (из аргумента)
        self.llm_api_key = api_key
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
            "model": "gpt-4o",
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

    def run(self, url, user_prompt, output_file):
        result = asyncio.run(self.parse_website(url, user_prompt))
        
        with open(output_file, "w", encoding="utf-8") as file:
            json.dump(result, file, ensure_ascii=False, indent=4)

        print(f"✅ Данные сохранены в {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Веб-скраппер для автоматического извлечения данных.")
    parser.add_argument("--url", type=str, required=True, help="URL страницы для скрапинга")
    parser.add_argument("--output", type=str, required=True, help="Файл для сохранения данных (JSON)")
    parser.add_argument("--prompt", type=str, required=True, help="Текстовый запрос для обработки данных")
    parser.add_argument("--api_key", type=str, required=True, help="API-ключ для OpenAI")

    args = parser.parse_args()
    scraper = WebScraper(api_key=args.api_key)
    scraper.run(args.url, args.prompt, args.output)
