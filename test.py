import webscraper as ws

if __name__ == "__main__":
    scraper = ws.WebScraper()
    web_url = "https://brandshop.ru/muzhskoe/"
    try:
        markdown_content = scraper.get_markdown(web_url, mode=4)
        print(markdown_content)
        # Здесь вы можете передать markdown_content в вашу LLM для дальнейшей обработки
    except Exception as e:
        print(f"Произошла ошибка: {e}")