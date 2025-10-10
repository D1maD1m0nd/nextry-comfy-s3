# Nextry Webhook Sender Node

## Описание

Кастомная нода для ComfyUI, которая отправляет вебхук уведомления с путями к изображениям на указанный endpoint.

## Особенности

- ✅ Завершающая нода (OUTPUT_NODE)
- ✅ Отправка POST запросов с JSON payload
- ✅ Обработка ошибок и таймаутов
- ✅ Логирование всех операций
- ✅ Возврат статуса выполнения запроса

## Входные параметры

### Required (Обязательные)

| Параметр | Тип | Описание | Пример |
|----------|-----|----------|--------|
| `endpoint` | STRING | URL endpoint для отправки вебхука | `http://localhost:8000/generation/comfy_webhook` |
| `preview_image` | STRING | Путь к preview изображению | `s3://bucket/preview_123.webp` |
| `stock_image` | STRING | Путь к stock изображению | `s3://bucket/stock_123.png` |

## Выходные данные

Нода возвращает JSON строку с результатом выполнения запроса:

### Успешный ответ
```json
{
  "success": true,
  "status_code": 200,
  "response": {
    // Ответ от сервера
  }
}
```

### Ошибка
```json
{
  "success": false,
  "error": "timeout|request_failed|unknown",
  "message": "Описание ошибки"
}
```

## Пример использования

### В ComfyUI workflow

1. Добавьте ноду "Nextry Webhook Sender" в ваш workflow
2. Подключите выходы от "Nextry Save Image to S3" к входам `preview_image` и `stock_image`
3. Укажите ваш endpoint URL
4. Запустите генерацию

### Пример цепочки нод

```
[Load Image] 
    ↓
[Process Image] 
    ↓
[Save Image S3] 
    ↓
[Webhook Sender] ← endpoint: "http://localhost:8000/generation/comfy_webhook"
```

### Пример payload, отправляемого на endpoint

```json
{
  "preview_image": "s3://my-bucket/output/preview_abc123.webp",
  "stock_image": "s3://my-bucket/output/stock_abc123.png"
}
```

## Настройки

### Timeout

По умолчанию таймаут для запроса составляет 30 секунд. Вы можете изменить это значение, модифицировав `self.timeout` в конструкторе класса:

```python
def __init__(self):
    self.type = 'output'
    self.timeout = 60  # Изменить на нужное значение
```

## Обработка ошибок

Нода обрабатывает следующие типы ошибок:

- **Timeout**: Когда запрос превышает установленный таймаут
- **Request Failed**: Ошибки сети или HTTP ошибки (4xx, 5xx)
- **Unknown**: Непредвиденные ошибки

Все ошибки логируются и возвращаются в результате выполнения ноды.

## Логирование

Нода использует встроенный logger для записи:
- URL endpoint и параметров перед отправкой
- Статус код ответа
- Содержимое ответа
- Все ошибки

Логи можно найти в консоли ComfyUI.

## Требования

- Python 3.8+
- requests>=2.31.0

Установите зависимости:
```bash
pip install -r requirements.txt
```

## Интеграция с вашим backend

Ваш endpoint должен принимать POST запросы с JSON body:

```python
# Пример Flask endpoint
@app.route('/generation/comfy_webhook', methods=['POST'])
def comfy_webhook():
    data = request.json
    preview_image = data.get('preview_image')
    stock_image = data.get('stock_image')
    
    # Ваша логика обработки
    
    return jsonify({'status': 'success', 'message': 'Images received'})
```

## Категория

Нода находится в категории **NEXTRY_ComfyS3** вместе с другими нодами для работы с S3.

