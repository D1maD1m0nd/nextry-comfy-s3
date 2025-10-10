# 🚀 Быстрый старт - Webhook Sender Node

## Шаг 1: Установка зависимостей

```bash
cd e:\ai\ComfyUI_windows_portable\ComfyUI\custom_nodes\nextry-comfy-s3
pip install -r requirements.txt
```

## Шаг 2: Перезапустите ComfyUI

Перезапустите ComfyUI, чтобы новая нода загрузилась.

## Шаг 3: Найдите ноду в ComfyUI

В ComfyUI найдите ноду в категории **NEXTRY_ComfyS3**:
- Нода называется: **"Nextry Webhook Sender"**

## Шаг 4 (Опционально): Запустите тестовый сервер

Для тестирования запустите пример сервера:

```bash
# Установите Flask
pip install flask

# Запустите тестовый сервер
python example_webhook_server.py
```

Сервер запустится на `http://localhost:8000`

## Шаг 5: Настройте ноду в ComfyUI

### Параметры ноды:

1. **endpoint**: URL для отправки вебхука
   - Пример: `http://localhost:8000/generation/comfy_webhook`
   
2. **preview_image**: Путь к preview изображению
   - Обычно подключается из выхода ноды "Save Image to S3"
   
3. **stock_image**: Путь к stock изображению
   - Обычно подключается из выхода ноды "Save Image to S3"

## Пример workflow

```
1. [Load Image или генерация]
        ↓
2. [Обработка изображения]
        ↓
3. [Nextry Save Image to S3]
        ↓ (preview_image и stock_image)
4. [Nextry Webhook Sender]
   - endpoint: http://localhost:8000/generation/comfy_webhook
   - preview_image: <из Save Image to S3>
   - stock_image: <из Save Image to S3>
```

## Что отправляется на endpoint?

POST запрос с JSON body:

```json
{
  "preview_image": "s3://bucket/path/preview_abc123.webp",
  "stock_image": "s3://bucket/path/stock_abc123.png"
}
```

## Что возвращает нода?

JSON строка с результатом:

### ✅ Успешно:
```json
{
  "success": true,
  "status_code": 200,
  "response": { /* ответ от сервера */ }
}
```

### ❌ Ошибка:
```json
{
  "success": false,
  "error": "timeout",
  "message": "Webhook request timed out after 30 seconds"
}
```

## Проверка логов

Все операции логируются в консоль ComfyUI. Проверьте консоль для отладки.

## Тестирование без локального сервера

Используйте httpbin.org для тестирования:

```python
# В параметре endpoint используйте:
https://httpbin.org/post
```

Или запустите тестовый скрипт:

```bash
# Тест с httpbin.org
python test_webhook.py --httpbin
```

## Интеграция с вашим backend

### Python Flask пример:

```python
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/generation/comfy_webhook', methods=['POST'])
def comfy_webhook():
    data = request.json
    preview = data.get('preview_image')
    stock = data.get('stock_image')
    
    # Ваша логика
    print(f'Received: {preview}, {stock}')
    
    return jsonify({'status': 'success'})

if __name__ == '__main__':
    app.run(port=8000)
```

### Python FastAPI пример:

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class WebhookData(BaseModel):
    preview_image: str
    stock_image: str

@app.post('/generation/comfy_webhook')
async def comfy_webhook(data: WebhookData):
    print(f'Received: {data.preview_image}, {data.stock_image}')
    return {'status': 'success'}
```

### Node.js Express пример:

```javascript
const express = require('express');
const app = express();

app.use(express.json());

app.post('/generation/comfy_webhook', (req, res) => {
    const { preview_image, stock_image } = req.body;
    console.log(`Received: ${preview_image}, ${stock_image}`);
    res.json({ status: 'success' });
});

app.listen(8000);
```

## Troubleshooting

### Ошибка: "Connection refused"
- Убедитесь, что ваш сервер запущен
- Проверьте правильность URL (host:port)

### Ошибка: "Timeout"
- Увеличьте таймаут в коде ноды (по умолчанию 30 сек)
- Проверьте, что сервер отвечает быстро

### Нода не появляется в ComfyUI
- Перезапустите ComfyUI
- Проверьте, что нет ошибок в консоли при загрузке
- Убедитесь, что `requests` установлен: `pip install requests`

## Дополнительная информация

См. подробную документацию: [WEBHOOK_NODE_USAGE.md](./WEBHOOK_NODE_USAGE.md)

