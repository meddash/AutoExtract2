import webscraper as ws
import os
import json


if __name__ == "__main__":
    # scraper = ws.WebScraper()
    # web_url = "https://brandshop.ru/muzhskoe/"
    # web_url = "https://3dmechanika.com/"
    # try:
    #     markdown_content = scraper.get_markdown(web_url, mode=4)
    #     print(markdown_content)
    #     # Здесь вы можете передать markdown_content в вашу LLM для дальнейшей обработки
    # except Exception as e:
    #     print(f"Произошла ошибка: {e}")

    parser = ws.UniversalWebParser(llm_api_key=os.getenv("OPENAI_API_KEY"))
    url = "https://brandshop.ru/muzhskoe/"
    prompt = "Достань мне все товары, их цены и фотографии с данного сайта"
    result = parser.run(url, prompt)
    print(json.dumps(result, indent=2, ensure_ascii=False))