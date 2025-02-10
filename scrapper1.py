import asyncio
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig
from crawl4ai.content_filter_strategy import PruningContentFilter
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator

async def main(in_url,
               mode # 1 - весь markdown, 2 - с цитатами, 3 - с ссылками , 4 - обрезанный если есть, иначе весь
               ):
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
            url=in_url, 
            config=config
        )

        if result.success:
            # Доступ к различным вариантам Markdown
            if result.markdown_v2:
                md_res = result.markdown_v2
                if mode == 1:
                    return("Оригинальный Markdown:" + md_res.raw_markdown)
                elif mode == 2:
                    return("Markdown с цитатами:" + md_res.markdown_with_citations)
                elif mode == 3:
                    return("Ссылки:" + md_res.references_markdown)
                elif mode == 4:
                    if md_res.fit_markdown:
                        return("Обрезанный текст:" + md_res.fit_markdown)
                    else:
                        return("Оригинальный Markdown:" + md_res.raw_markdown)
            else:
                print("Markdown:", result.markdown[:200] if result.markdown else "N/A")
        else:
            print("Ошибка:", result.error_message)

if __name__ == "__main__":
    website_markdown = asyncio.run(main("https://brandshop.ru/muzhskoe/", 4))
    print(website_markdown)
