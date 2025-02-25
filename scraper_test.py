# import asyncio

# # Создаём экземпляр класса WebScraper
# scraper = WebScraper()

# async def main():
#     # Указываем URL сайта, который нужно спарсить
#     url = "https://example.com"
    
#     # Вызываем метод для получения Markdown
#     markdown = await scraper.fetch_markdown(url)
    
#     # Печатаем полученный Markdown
#     print(markdown)

# # Запускаем асинхронную функцию
# asyncio.run(main())

import os
import json
from webscraper import WebScraper

if __name__ == "__main__":
    scraper = WebScraper()
    url = "https://brandshop.ru/muzhskoe/" # Замени на реальный URL
    prompt = """
Приведи список товаров из следующего текста в JSON-формате со следующими полями:
- "Название" (string)
- "Цена" (string)
- "Фото" (URL к реальному изображению товара)

Убери дубликаты товаров и проверь, чтобы у каждого товара была правильная ссылка на фото.
"""
    
    try:
        result = scraper.run(url, prompt)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    except Exception as e:
        print(f"Ошибка: {e}")