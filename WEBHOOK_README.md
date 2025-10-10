# 🎣 Nextry Webhook Sender для ComfyUI

> Отправляйте webhook уведомления из ComfyUI на ваш backend одним кликом!

[![Status](https://img.shields.io/badge/status-ready-brightgreen)]()
[![Version](https://img.shields.io/badge/version-1.0.0-blue)]()
[![Python](https://img.shields.io/badge/python-3.8+-blue)]()

---

## ✨ Что это?

**Nextry Webhook Sender** — это кастомная нода для ComfyUI, которая автоматически отправляет HTTP POST запросы на ваш backend с путями к сгенерированным изображениям.

### Зачем это нужно?

- ✅ Автоматические уведомления о завершении генерации
- ✅ Интеграция ComfyUI с вашими сервисами
- ✅ Триггер пост-обработки изображений
- ✅ Event-driven архитектура
- ✅ Автоматизация workflow

---

## 🚀 Быстрый старт (3 минуты)

### 1️⃣ Установка

```bash
cd e:\ai\ComfyUI_windows_portable\ComfyUI\custom_nodes\nextry-comfy-s3
pip install -r requirements.txt
```

### 2️⃣ Перезапуск ComfyUI

Перезапустите ComfyUI для загрузки ноды.

### 3️⃣ Использование

1. Найдите **"Nextry Webhook Sender"** в категории **NEXTRY_ComfyS3**
2. Подключите к **"Save Image to S3"**
3. Укажите ваш endpoint URL
4. Готово! 🎉

---

## 📊 Как это работает

```
┌──────────────────┐
│   Generate Image │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  Save Image S3   │
└────────┬─────────┘
         │
         │ preview_image, stock_image
         ▼
┌──────────────────────────┐
│  Webhook Sender          │
│  endpoint: your-url      │
└────────┬─────────────────┘
         │
         │ HTTP POST
         ▼
┌──────────────────┐
│  Your Backend    │
│  • Process       │
│  • Store         │
│  • Notify        │
└──────────────────┘
```

---

## 💻 Пример использования

### В ComfyUI

```
endpoint: http://localhost:8000/generation/comfy_webhook
preview_image: s3://bucket/preview_123.webp
stock_image: s3://bucket/stock_123.png
```

### Что отправляется

```json
POST http://localhost:8000/generation/comfy_webhook
Content-Type: application/json

{
  "preview_image": "s3://bucket/preview_123.webp",
  "stock_image": "s3://bucket/stock_123.png"
}
```

### Ваш backend (Python Flask)

```python
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/generation/comfy_webhook', methods=['POST'])
def webhook():
    data = request.json
    print(f"Preview: {data['preview_image']}")
    print(f"Stock: {data['stock_image']}")
    
    # Ваша логика здесь
    
    return jsonify({'status': 'success'})

app.run(port=8000)
```

---

## 🧪 Тестирование

### Вариант 1: Тестовый сервер (рекомендуется)

```bash
# Установите Flask
pip install flask

# Запустите тестовый сервер
python example_webhook_server.py

# Сервер запустится на http://localhost:8000
```

### Вариант 2: httpbin.org

```
endpoint: https://httpbin.org/post
```

### Вариант 3: Тестовый скрипт

```bash
python test_webhook.py --httpbin
```

---

## 📦 Входные параметры

| Параметр | Тип | Описание | Пример |
|----------|-----|----------|--------|
| **endpoint** | STRING | URL вашего webhook | `http://localhost:8000/generation/comfy_webhook` |
| **preview_image** | STRING | Путь к preview | `s3://bucket/preview.webp` |
| **stock_image** | STRING | Путь к stock | `s3://bucket/stock.png` |

---

## 📤 Выходные данные

### ✅ Успех

```json
{
  "success": true,
  "status_code": 200,
  "response": {
    "status": "success",
    "message": "Images received"
  }
}
```

### ❌ Ошибка

```json
{
  "success": false,
  "error": "timeout",
  "message": "Webhook request timed out after 30 seconds"
}
```

---

## 📚 Документация

### 📖 Полная документация

| Документ | Описание |
|----------|----------|
| **[QUICKSTART_WEBHOOK.md](./QUICKSTART_WEBHOOK.md)** | 🚀 Быстрый старт с примерами |
| **[WEBHOOK_NODE_USAGE.md](./WEBHOOK_NODE_USAGE.md)** | 📚 Детальное руководство |
| **[WORKFLOW_DIAGRAM.md](./WORKFLOW_DIAGRAM.md)** | 📊 Визуальные диаграммы |
| **[WEBHOOK_FAQ.md](./WEBHOOK_FAQ.md)** | ❓ 35+ вопросов и ответов |
| **[WEBHOOK_DOCUMENTATION_INDEX.md](./WEBHOOK_DOCUMENTATION_INDEX.md)** | 📑 Индекс всей документации |

---

## 🎯 Use Cases

### 1. Уведомление backend

```python
# Получите уведомление, когда генерация завершена
@app.route('/webhook', methods=['POST'])
def on_generation_complete():
    send_email_to_user("Your images are ready!")
```

### 2. Автоматическая пост-обработка

```python
# Автоматически обработайте изображения
def webhook_handler(preview, stock):
    apply_filters(preview)
    create_thumbnails(stock)
    save_to_database()
```

### 3. Event-driven архитектура

```python
# Публикуйте события для других сервисов
def webhook_handler(data):
    event_bus.publish('image.generated', data)
```

---

## 🔥 Фичи

- ✅ **OUTPUT_NODE** — завершающая нода в workflow
- ✅ **Error handling** — полная обработка ошибок
- ✅ **Logging** — детальное логирование всех операций
- ✅ **Timeout** — настраиваемый таймаут (по умолчанию 30s)
- ✅ **Type hints** — для лучшей читаемости кода
- ✅ **Status tracking** — возврат статуса выполнения

---

## 🛠️ Troubleshooting

### Нода не появляется?

```bash
# Проверьте установку
pip install requests>=2.31.0

# Перезапустите ComfyUI
```

### Connection refused?

```bash
# Убедитесь, что сервер запущен
python example_webhook_server.py

# Проверьте URL
curl http://localhost:8000/health
```

### Timeout?

```python
# Увеличьте timeout в webhook_sender.py
self.timeout = 60  # было 30
```

**Больше решений:** [WEBHOOK_FAQ.md](./WEBHOOK_FAQ.md)

---

## 📋 Требования

- Python 3.8+
- requests >= 2.31.0
- ComfyUI

---

## 📁 Файлы проекта

```
📁 src/nodes/
   └── webhook_sender.py          ⭐ Основная нода

📖 Документация/
   ├── WEBHOOK_README.md           👈 Вы здесь
   ├── QUICKSTART_WEBHOOK.md       🚀 Начните здесь!
   ├── WEBHOOK_NODE_USAGE.md       📚 Полное руководство
   ├── WORKFLOW_DIAGRAM.md         📊 Диаграммы
   ├── WEBHOOK_FAQ.md              ❓ Q&A
   └── WEBHOOK_DOCUMENTATION_INDEX.md

🧪 Тестирование/
   ├── test_webhook.py             Тестовый скрипт
   ├── example_webhook_server.py   Flask сервер
   └── example_workflow_webhook.json
```

---

## 🎓 Обучение

### Начинающие

1. Прочитайте [QUICKSTART_WEBHOOK.md](./QUICKSTART_WEBHOOK.md)
2. Запустите `example_webhook_server.py`
3. Попробуйте в ComfyUI

### Продвинутые

1. Изучите [WEBHOOK_NODE_USAGE.md](./WEBHOOK_NODE_USAGE.md)
2. Посмотрите исходный код `webhook_sender.py`
3. Кастомизируйте под свои нужды

### DevOps

1. Прочитайте [WEBHOOK_FAQ.md](./WEBHOOK_FAQ.md) Q29-Q30
2. Настройте мониторинг
3. Добавьте retry логику

---

## 🌟 Примеры интеграции

### Flask

```python
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/generation/comfy_webhook', methods=['POST'])
def webhook():
    data = request.json
    # Ваша логика
    return jsonify({'status': 'success'})

app.run(port=8000)
```

### FastAPI

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class WebhookData(BaseModel):
    preview_image: str
    stock_image: str

@app.post('/generation/comfy_webhook')
async def webhook(data: WebhookData):
    # Асинхронная обработка
    return {'status': 'success'}
```

### Express.js

```javascript
const express = require('express');
const app = express();

app.use(express.json());

app.post('/generation/comfy_webhook', (req, res) => {
    const { preview_image, stock_image } = req.body;
    // Ваша логика
    res.json({ status: 'success' });
});

app.listen(8000);
```

---

## 🎉 Готово!

Нода установлена и готова к использованию!

### Следующие шаги:

1. ✅ Установили зависимости
2. ✅ Перезапустили ComfyUI
3. 👉 Найдите ноду в категории **NEXTRY_ComfyS3**
4. 👉 Подключите к вашему workflow
5. 👉 Настройте endpoint
6. 🎊 Начните использовать!

---

## 📞 Поддержка

- 📖 Документация: [WEBHOOK_DOCUMENTATION_INDEX.md](./WEBHOOK_DOCUMENTATION_INDEX.md)
- ❓ FAQ: [WEBHOOK_FAQ.md](./WEBHOOK_FAQ.md)
- 🧪 Тесты: `python test_webhook.py`
- 🐛 Issues: Создайте issue в репозитории

---

## 🙏 Благодарности

Спасибо за использование Nextry Webhook Sender!

- ⭐ Star репозиторий
- 📢 Поделитесь с коллегами
- 🐛 Сообщайте о багах
- 💡 Предлагайте фичи

---

## 📄 Лицензия

См. [LICENSE](./LICENSE) файл.

---

<div align="center">

### 🚀 Начать прямо сейчас!

**[→ Quickstart Guide](./QUICKSTART_WEBHOOK.md)** | **[→ Full Documentation](./WEBHOOK_DOCUMENTATION_INDEX.md)** | **[→ FAQ](./WEBHOOK_FAQ.md)**

---

**Версия:** 1.0.0 | **Дата:** 2025-10-10 | **Статус:** ✅ Production Ready

Made with ❤️ for ComfyUI Community

</div>

