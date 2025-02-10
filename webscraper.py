import asyncio
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig
from crawl4ai.content_filter_strategy import PruningContentFilter
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator

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
