# AutoExtract2

**AutoExtract2** — это веб-скраппер для автоматического извлечения данных с сайтов с помощью `crawl4ai` и OpenAI API.  
Позволяет загружать веб-страницы, парсить HTML в Markdown и анализировать их содержимое с помощью LLM.

---

## 🚀 Установка и запуск

### 1️⃣ **Клонирование репозитория**
Склонируйте проект из GitHub:
```bash
git clone https://github.com/meddash/AutoExtract2.git
cd AutoExtract2
```

### 2️⃣ **Установка зависимостей**
Убедитесь, что у вас установлен Python (версия 3.7+).  
Затем установите необходимые библиотеки:
```bash
pip install -r requirements.txt
```

### 3️⃣ **Запуск скраппера**
Используйте команду:
```bash
python webscraper.py --url "https://example.com" --output "data.json" --prompt "Извлеки все товары с ценами" --api_key "sk-123456"
```

### **Параметры команды:**
| Параметр   | Описание |
|------------|----------|
| `--url`    | Ссылка на веб-страницу, с которой нужно извлечь данные |
| `--output` | Название файла для сохранения результата (`.json`, `.txt`, `.csv` и т. д.) |
| `--prompt` | Текстовый запрос для обработки данных в OpenAI API |
| `--api_key` | API-ключ OpenAI (можно получить [здесь](https://platform.openai.com/signup/)) |

---

## 📌 **Как это работает?**
1. **Скраппер** загружает HTML-страницу по указанному `URL`.  
2. **Код `crawl4ai`** преобразует её в Markdown.  
3. **OpenAI API** анализирует данные с переданным `prompt`.  
4. **Готовый результат сохраняется** в указанный файл (`.json`, `.txt`, `.csv` и т. д.).

---

## 📂 **Структура проекта**
```
📁 AutoExtract2
│── webscraper.py       # Основной файл веб-скраппера
│── scraper_test.py     # Тесты для проверки работы
│── README.md           # Документация по проекту
│── requirements.txt    # Список зависимостей
```

---

## 📄 **Примеры использования**

### ✅ **Сохранение результата в JSON**
```bash
python webscraper.py --url "https://brandshop.ru/muzhskoe/" --output "products.json" --prompt "Извлеки список товаров с ценами" --api_key "sk-123456"
```
📌 **Что произойдёт?**  
1. Данные с `https://brandshop.ru/muzhskoe/` будут проанализированы.  
2. OpenAI API обработает страницу с `prompt: "Извлеки список товаров с ценами"`.  
3. Результат сохранится в `products.json`.

**Пример `products.json`:**
```json
{
    "prompt": "Извлеки список товаров с ценами",
    "choices": [
        {
            "message": {
                "role": "assistant",
                "content": [
                    {
                        "Название": "Dr. Martens Ботинки 1461 Bex Smooth",
                        "Цена": "23 890 ₽",
                        "Фото": "https://brandshop.ru/images/example1.jpg"
                    },
                    {
                        "Название": "Kangol Мужской свитер College Varsity",
                        "Цена": "13 590 ₽",
                        "Фото": "https://brandshop.ru/images/example2.jpg"
                    }
                ]
            }
        }
    ]
}
```

---

### ✅ **Сохранение в текстовый файл**
```bash
python webscraper.py --url "https://brandshop.ru/muzhskoe/" --output "output.txt" --prompt "Определи ключевые темы" --api_key "sk-123456"
```
Результат будет записан в `output.txt`.

---

### ✅ **Сохранение в CSV (при необходимости)**
Если хочешь сохранять в `CSV`, можешь открыть `products.json` и конвертировать его в `CSV` с помощью `pandas`.

```python
import pandas as pd
import json

with open("products.json", "r", encoding="utf-8") as file:
    data = json.load(file)

df = pd.DataFrame(data["choices"][0]["message"]["content"])
df.to_csv("products.csv", index=False)
print("✅ Данные сохранены в products.csv")
```

---

## 🛠 **Зависимости**
Для работы программы необходимо:
- `asyncio`, `aiohttp` — асинхронные запросы
- `crawl4ai` — парсинг веб-страниц в Markdown
- `requests`, `json` — обработка API-запросов и сохранение данных

Установи всё командой:
```bash
pip install -r requirements.txt
```

---

## 🔥 **Планы по улучшению**
- 🔹 Добавить возможность использования локальных LLM
- 🔹 Проработать структуру output файлов
- 🔹 Разобраться с проблемами связанными с ссылками на фотографии
---

## 📄 **Лицензия**
**MIT License**.

