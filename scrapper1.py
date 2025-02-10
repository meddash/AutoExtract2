import asyncio
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig
from crawl4ai.content_filter_strategy import PruningContentFilter
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator

async def main():
    # Настройка фильтра обрезки контента
    prune_filter = PruningContentFilter(
        threshold=0.45,           # Порог обрезки; ниже — больше контента сохраняется
        threshold_type="dynamic", # Тип порога: "fixed" или "dynamic"
        min_word_threshold=5      # Минимальное количество слов для учета узла
    )

    # Настройка генератора Markdown с фильтром
    md_generator = DefaultMarkdownGenerator(content_filter=prune_filter)

    # Конфигурация запуска краулера
    config = CrawlerRunConfig(
        markdown_generator=md_generator
    )

    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(
            url="https://brandshop.ru/muzhskoe/", 
            config=config
        )

        if result.success:
            # Доступ к различным вариантам Markdown
            if result.markdown_v2:
                md_res = result.markdown_v2
                print("Оригинальный Markdown:", md_res.raw_markdown[:300])
                print("Markdown с цитатами:", md_res.markdown_with_citations[:300])
                print("Ссылки:", md_res.references_markdown)
                if md_res.fit_markdown:
                    print("Обрезанный текст:", md_res.fit_markdown[:300])
            else:
                print("Markdown:", result.markdown[:200] if result.markdown else "N/A")
        else:
            print("Ошибка:", result.error_message)

if __name__ == "__main__":
    asyncio.run(main())
