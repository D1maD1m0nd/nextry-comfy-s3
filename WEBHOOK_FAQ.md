# ❓ FAQ - Nextry Webhook Sender Node

## Общие вопросы

### 1. Что такое Webhook Sender Node?

**Ответ:** Это кастомная нода для ComfyUI, которая отправляет HTTP POST запросы на указанный endpoint с информацией о сгенерированных изображениях. Это позволяет интегрировать ComfyUI с внешними системами.

---

### 2. Зачем мне это нужно?

**Ответ:** Webhook Sender позволяет:
- Уведомлять ваш backend о завершении генерации
- Автоматически запускать пост-обработку изображений
- Интегрировать ComfyUI в более крупные пайплайны
- Отправлять уведомления пользователям
- Сохранять метаданные в базу данных

---

### 3. Это безопасно?

**Ответ:** Нода отправляет только те данные, которые вы явно указываете (пути к изображениям). Для продакшена рекомендуется:
- Использовать HTTPS endpoints
- Аутентифицировать запросы (добавьте токены в payload)
- Валидировать webhook signatures на стороне сервера
- Использовать приватные сети для коммуникации

---

## Установка и настройка

### 4. Как установить ноду?

**Ответ:**
```bash
# 1. Перейдите в директорию
cd e:\ai\ComfyUI_windows_portable\ComfyUI\custom_nodes\nextry-comfy-s3

# 2. Установите зависимости
pip install -r requirements.txt

# 3. Перезапустите ComfyUI
```

---

### 5. Нода не появляется в ComfyUI. Что делать?

**Ответ:** Проверьте:

1. **Установлены ли зависимости?**
   ```bash
   pip install requests>=2.31.0
   ```

2. **Есть ли ошибки в консоли ComfyUI?**
   - Посмотрите на вывод при запуске ComfyUI
   - Ищите строки с "ERROR" или "Traceback"

3. **Перезапустили ли вы ComfyUI?**
   - После установки нужен полный перезапуск

4. **Правильно ли обновлен nodes_mappings.py?**
   ```python
   from .nodes.webhook_sender import NextryWebhookSender
   ```

---

### 6. Где найти ноду в интерфейсе?

**Ответ:** В ComfyUI:
- Нажмите правую кнопку мыши → Add Node
- Найдите категорию **NEXTRY_ComfyS3**
- Выберите **"Nextry Webhook Sender"**

---

## Использование

### 7. Какой URL использовать в поле endpoint?

**Ответ:** 

**Для локальной разработки:**
```
http://localhost:8000/generation/comfy_webhook
```

**Для тестирования (httpbin):**
```
https://httpbin.org/post
```

**Для продакшена:**
```
https://api.yourdomain.com/webhooks/comfy
```

---

### 8. Что передавать в preview_image и stock_image?

**Ответ:** Эти поля обычно подключаются к выходу ноды "Save Image to S3":

```
[Save Image to S3] → s3_image_paths
         ↓
[Webhook Sender]
  preview_image ← первый путь
  stock_image ← второй путь
```

Можно также указать вручную:
```
s3://my-bucket/path/to/preview.webp
s3://my-bucket/path/to/stock.png
```

---

### 9. Как подключить ноду к Save Image S3?

**Ответ:** 

1. Добавьте ноду "Save Image to S3"
2. Добавьте ноду "Webhook Sender"
3. Соедините выход `s3_image_paths` с входами `preview_image` и `stock_image`
4. Укажите endpoint URL

См. `example_workflow_webhook.json` для примера.

---

### 10. Можно ли использовать без S3?

**Ответ:** Да! Вы можете передать любые строки в preview_image и stock_image:

```
preview_image: /path/to/local/image.png
stock_image: https://example.com/image.jpg
```

Нода просто отправит эти строки в webhook.

---

## Ошибки и troubleshooting

### 11. Ошибка "Connection refused"

**Причины:**
- Сервер не запущен
- Неправильный порт или хост
- Firewall блокирует соединение

**Решение:**
```bash
# Проверьте, что сервер запущен
curl http://localhost:8000/health

# Или запустите тестовый сервер
python example_webhook_server.py

# Проверьте firewall
# Windows: Разрешите входящие соединения на порт 8000
```

---

### 12. Ошибка "Timeout"

**Причины:**
- Сервер не отвечает
- Сервер обрабатывает запрос слишком долго
- Сетевые проблемы

**Решение:**
```python
# Увеличьте timeout в webhook_sender.py
def __init__(self):
    self.type = 'output'
    self.timeout = 60  # Было 30, стало 60 секунд
```

---

### 13. Сервер получает пустые данные

**Причина:** Неправильно подключены входы ноды

**Решение:**
1. Проверьте соединения в ComfyUI
2. Убедитесь, что Save Image S3 выполняется до Webhook Sender
3. Проверьте логи ComfyUI на предмет ошибок

---

### 14. Ошибка "Module 'requests' not found"

**Решение:**
```bash
pip install requests>=2.31.0
# Затем перезапустите ComfyUI
```

---

## Тестирование

### 15. Как протестировать ноду без реального сервера?

**Ответ:** Используйте httpbin.org:

```
endpoint: https://httpbin.org/post
```

httpbin.org - это бесплатный сервис для тестирования HTTP запросов.

Или запустите тестовый скрипт:
```bash
python test_webhook.py --httpbin
```

---

### 16. Как запустить тестовый сервер?

**Ответ:**
```bash
# Установите Flask
pip install flask

# Запустите сервер
python example_webhook_server.py

# Сервер будет доступен на http://localhost:8000
```

Сервер покажет все полученные webhooks в консоли.

---

### 17. Как посмотреть историю webhook'ов?

**Ответ:** Если вы используете `example_webhook_server.py`:

```bash
# В браузере или curl
curl http://localhost:8000/webhooks/history
```

Ответ:
```json
{
  "total": 5,
  "webhooks": [...]
}
```

---

## Разработка и кастомизация

### 18. Как добавить дополнительные параметры в webhook?

**Ответ:** Отредактируйте `webhook_sender.py`:

```python
@classmethod
def INPUT_TYPES(cls):
    return {
        'required': {
            'endpoint': ('STRING', {...}),
            'preview_image': ('STRING', {...}),
            'stock_image': ('STRING', {...}),
            # Добавьте новый параметр
            'user_id': ('STRING', {'default': ''}),
        }
    }

def send_webhook(self, endpoint, preview_image, stock_image, user_id):
    payload = {
        'preview_image': preview_image,
        'stock_image': stock_image,
        'user_id': user_id,  # Добавьте в payload
    }
    # ... остальной код
```

---

### 19. Как добавить аутентификацию?

**Ответ:** Добавьте headers в запрос:

```python
# В методе send_webhook
response = requests.post(
    endpoint,
    json=payload,
    headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer YOUR_TOKEN',  # Добавьте токен
        'X-API-Key': 'your-api-key',
    },
    timeout=self.timeout
)
```

Или добавьте токен как параметр ноды:
```python
'auth_token': ('STRING', {'default': ''}),
```

---

### 20. Как отправить дополнительные метаданные?

**Ответ:** Расширьте payload:

```python
payload = {
    'preview_image': preview_image,
    'stock_image': stock_image,
    'metadata': {
        'timestamp': datetime.now().isoformat(),
        'workflow_id': 'some_id',
        'resolution': '1024x1024',
    }
}
```

---

## Backend интеграция

### 21. Пример Flask сервера?

**Ответ:**
```python
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/generation/comfy_webhook', methods=['POST'])
def webhook():
    data = request.json
    
    # Получите данные
    preview = data.get('preview_image')
    stock = data.get('stock_image')
    
    # Ваша логика
    print(f'Received: {preview}, {stock}')
    
    # TODO: Скачать из S3, обработать, сохранить в БД
    
    return jsonify({'status': 'success'})

if __name__ == '__main__':
    app.run(port=8000)
```

---

### 22. Пример FastAPI сервера?

**Ответ:**
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
    await process_images(data.preview_image, data.stock_image)
    return {'status': 'success'}
```

---

### 23. Как обработать webhook асинхронно?

**Ответ:** Используйте очередь задач (Celery, RQ, etc):

```python
from celery import Celery

celery = Celery('tasks', broker='redis://localhost')

@celery.task
def process_images(preview, stock):
    # Длительная обработка
    pass

@app.route('/generation/comfy_webhook', methods=['POST'])
def webhook():
    data = request.json
    
    # Добавьте в очередь
    process_images.delay(
        data['preview_image'],
        data['stock_image']
    )
    
    # Немедленный ответ
    return jsonify({'status': 'queued'}), 202
```

---

### 24. Как скачать изображения из S3?

**Ответ:**
```python
import boto3

s3 = boto3.client('s3')

def download_from_s3(s3_path):
    # Парсим s3://bucket/path
    bucket = s3_path.replace('s3://', '').split('/')[0]
    key = '/'.join(s3_path.replace('s3://', '').split('/')[1:])
    
    # Скачиваем
    s3.download_file(bucket, key, f'/tmp/{key}')
    return f'/tmp/{key}'

# В webhook handler
preview_local = download_from_s3(data['preview_image'])
stock_local = download_from_s3(data['stock_image'])
```

---

## Производительность

### 25. Замедляет ли webhook работу ComfyUI?

**Ответ:** Минимально. Нода ждет ответа от сервера (до 30 секунд по умолчанию), но это происходит после генерации изображения. Если нужно избежать ожидания:

1. Используйте асинхронный сервер (FastAPI, aiohttp)
2. Отвечайте сразу (202 Accepted), обрабатывайте в фоне
3. Или уменьшите timeout в ноде

---

### 26. Можно ли отправлять несколько webhook'ов?

**Ответ:** Да! Добавьте несколько нод Webhook Sender в workflow:

```
[Save Image] → [Webhook 1] → Backend 1
            ↘ [Webhook 2] → Backend 2
            ↘ [Webhook 3] → Backend 3
```

Каждая нода отправит независимый запрос.

---

## Логирование и отладка

### 27. Где смотреть логи?

**Ответ:** 
- **ComfyUI:** В консоли, где запущен ComfyUI
- **Backend:** В логах вашего сервера
- **Webhook Node:** Логирует все в консоль ComfyUI

Ищите строки с:
```
INFO: Preparing webhook request to: ...
INFO: Webhook sent successfully
ERROR: Webhook request failed: ...
```

---

### 28. Как увеличить детальность логов?

**Ответ:** В `webhook_sender.py` добавьте дополнительные логи:

```python
logger.debug(f'Full payload: {payload}')
logger.debug(f'Headers: {headers}')
logger.info(f'Request took {elapsed_time}s')
```

---

## Продакшен

### 29. Готово ли это для продакшена?

**Ответ:** Да, но рекомендуется:
- ✅ Использовать HTTPS endpoints
- ✅ Добавить аутентификацию
- ✅ Настроить retry логику на backend
- ✅ Мониторить webhook deliveries
- ✅ Настроить алерты на ошибки
- ✅ Использовать rate limiting

---

### 30. Как добавить retry логику?

**Ответ:** Используйте библиотеку `tenacity`:

```python
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10)
)
def send_webhook_with_retry(self, endpoint, payload):
    response = requests.post(endpoint, json=payload, timeout=30)
    response.raise_for_status()
    return response
```

---

## Прочее

### 31. Можно ли отправлять файлы вместо путей?

**Ответ:** В текущей версии - нет. Нода отправляет только пути. Файлы должен скачать backend из S3 или другого источника.

Если нужна такая функциональность - можно расширить ноду для загрузки файлов.

---

### 32. Есть ли ограничения на размер данных?

**Ответ:** 
- **Paths:** Практически нет ограничений
- **Payload:** Зависит от вашего сервера (обычно несколько MB)
- **Timeout:** 30 секунд по умолчанию

---

### 33. Можно ли использовать с другими нодами (не S3)?

**Ответ:** Да! Нода работает с любыми STRING входами. Примеры:

- Локальные пути: `/path/to/image.png`
- URLs: `https://example.com/image.jpg`
- S3 URIs: `s3://bucket/key`
- Любые другие строки

---

### 34. Где найти полную документацию?

**Ответ:**
- **Быстрый старт:** `QUICKSTART_WEBHOOK.md`
- **Полное руководство:** `WEBHOOK_NODE_USAGE.md`
- **Диаграммы:** `WORKFLOW_DIAGRAM.md`
- **Изменения:** `CHANGELOG_WEBHOOK.md`
- **Summary:** `WEBHOOK_IMPLEMENTATION_SUMMARY.md`

---

### 35. Куда сообщать о проблемах?

**Ответ:** 
1. Проверьте этот FAQ
2. Проверьте документацию
3. Запустите тестовый скрипт: `python test_webhook.py --httpbin`
4. Проверьте логи ComfyUI
5. Создайте issue в репозитории проекта

---

## 🎉 Не нашли ответ?

Проверьте:
- 📖 [WEBHOOK_NODE_USAGE.md](./WEBHOOK_NODE_USAGE.md)
- 🚀 [QUICKSTART_WEBHOOK.md](./QUICKSTART_WEBHOOK.md)
- 📊 [WORKFLOW_DIAGRAM.md](./WORKFLOW_DIAGRAM.md)

Или запустите пример:
```bash
python example_webhook_server.py
```

---

**Последнее обновление:** 2025-10-10  
**Версия:** 1.0.0

