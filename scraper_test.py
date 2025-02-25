import os
import json
from webscraper import WebScraper

if __name__ == "__main__":
    scraper = WebScraper(api_key=os.getenv("OPENAI_API_KEY"))
    url = "https://brandshop.ru/muzhskoe/" # Замени на реальный URL
    output = "parsed.json"
    prompt = """
Приведи список товаров из следующего текста в JSON-формате со следующими полями:
- "Название" (string)
- "Цена" (string)
- "Фото" (URL к реальному изображению товара)

Убери дубликаты товаров и проверь, чтобы у каждого товара была правильная ссылка на фото.
"""
    
    try:
        result = scraper.run(url, prompt, output)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    except Exception as e:
        print(f"Ошибка: {e}")