import asyncio
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig
from crawl4ai.content_filter_strategy import PruningContentFilter
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator
import aiohttp

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

    async def fetch_markdown(self, url, mode=1):
        async with AsyncWebCrawler() as crawler:
            result = await crawler.arun(url=url, config=self.config)
            if result.success:
                if result.markdown_v2:
                    md_res = result.markdown_v2
                    if mode == 1:
                        return md_res.raw_markdown
                    elif mode == 2:
                        return md_res.markdown_with_citations
                    elif mode == 3:
                        return md_res.references_markdown
                    elif mode == 4:
                        return md_res.fit_markdown if md_res.fit_markdown else md_res.raw_markdown
                else:
                    return result.markdown
            else:
                raise Exception(f"Ошибка: {result.error_message}")

    def get_markdown(self, url, mode=1):
        return asyncio.run(self.fetch_markdown(url, mode))


class UniversalWebParser:
    def __init__(self, llm_api_key, threshold=0.45, threshold_type="dynamic", min_word_threshold=5):
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
        # Ключ API для LLM (например, xAI)
        self.llm_api_key = llm_api_key
        self.llm_endpoint = "https://api.xai.com/grok"  

    async def fetch_markdown(self, url, mode=1):
        async with AsyncWebCrawler() as crawler:
            result = await crawler.arun(url=url, config=self.config)
            if result.success:
                if result.markdown_v2:
                    md_res = result.markdown_v2
                    if mode == 1:
                        return md_res.raw_markdown
                    elif mode == 2:
                        return md_res.markdown_with_citations
                    elif mode == 3:
                        return md_res.references_markdown
                    elif mode == 4:
                        return md_res.fit_markdown if md_res.fit_markdown else md_res.raw_markdown
                else:
                    return result.markdown
            else:
                raise Exception(f"Ошибка: {result.error_message}")

    async def query_llm(self, markdown, user_prompt):
        """Отправка Markdown и промпта в LLM для извлечения данных"""
        headers = {
            "Authorization": f"Bearer {self.llm_api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "grok",  # Или другая модель
            "prompt": (
                f"Вот содержимое сайта в формате Markdown:\n\n{markdown}\n\n"
                f"Выполни следующий запрос: {user_prompt}\n"
                "Верни результат в формате JSON."
            ),
            "max_tokens": 2000,
            "temperature": 0.5
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(self.llm_endpoint, headers=headers, json=payload) as response:
                if response.status == 200:
                    result = await response.json()
                    return json.loads(result["choices"][0]["text"])  # Предполагаем, что LLM вернёт JSON
                else:
                    raise Exception(f"Ошибка LLM API: {response.status}")

    async def parse_website(self, url, user_prompt):
        """Основной метод парсинга"""
        # Шаг 1: Получаем Markdown
        markdown = await self.fetch_markdown(url)
        # Шаг 2: Передаем в LLM для анализа
        result = await self.query_llm(markdown, user_prompt)
        return result

    def run(self, url, user_prompt):
        """Синхронный интерфейс для удобства"""
        return asyncio.run(self.parse_website(url, user_prompt))