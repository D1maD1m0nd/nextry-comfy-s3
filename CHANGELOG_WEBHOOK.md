# Changelog - Webhook Sender Node

## [1.0.0] - 2025-10-10

### 🎉 Added
- **Nextry Webhook Sender Node** - новая кастомная нода для отправки вебхук уведомлений
  - Отправка POST запросов на произвольные endpoints
  - Поддержка передачи путей к изображениям (preview_image, stock_image)
  - Встроенная обработка ошибок (timeout, network errors, etc.)
  - Детальное логирование всех операций
  - Возврат статуса выполнения запроса

### 📝 Documentation
- `WEBHOOK_NODE_USAGE.md` - подробная документация по использованию ноды
- `QUICKSTART_WEBHOOK.md` - краткая инструкция для быстрого старта
- `example_webhook_server.py` - пример Flask сервера для приема вебхуков
- `test_webhook.py` - скрипт для тестирования функциональности
- `example_workflow_webhook.json` - пример workflow для ComfyUI

### 🔧 Technical Details

#### Входные параметры:
- `endpoint` (STRING) - URL для отправки вебхука
- `preview_image` (STRING) - путь к preview изображению
- `stock_image` (STRING) - путь к stock изображению

#### Выходные данные:
- `webhook_response` (STRING) - JSON строка с результатом выполнения

#### Категория:
- `NEXTRY_ComfyS3` - нода доступна в той же категории, что и другие S3 ноды

### 📦 Dependencies
- Добавлена зависимость `requests>=2.31.0` в `requirements.txt`

### 🔄 Integration
- Нода зарегистрирована в `src/nodes_mappings.py`
- Полностью интегрирована с существующей архитектурой проекта
- Использует тот же logger для единообразного логирования

### ✨ Features
- **OUTPUT_NODE**: нода является завершающей в workflow
- **Error Handling**: обработка timeout, network errors, и неожиданных исключений
- **Logging**: детальное логирование всех операций для отладки
- **Flexible**: работает с любыми HTTP endpoints
- **Type Safety**: использование type hints для лучшей читаемости кода

### 🧪 Testing
- Включен тестовый скрипт для проверки функциональности
- Пример сервера для локального тестирования
- Поддержка тестирования с httpbin.org

### 📖 Use Cases
- Уведомление backend при завершении генерации изображений
- Триггеринг пост-процессинга
- Интеграция ComfyUI workflows с внешними системами
- Автоматизация пайплайнов обработки изображений

### 🔐 Security Considerations
- Таймаут по умолчанию: 30 секунд
- Отправка только указанных данных (preview_image, stock_image)
- Content-Type: application/json
- Обработка всех исключений для предотвращения падения workflow

### 🚀 Performance
- Асинхронная отправка (не блокирует UI)
- Настраиваемый timeout
- Минимальные overhead

---

## Структура файлов проекта

```
nextry-comfy-s3/
├── src/
│   ├── nodes/
│   │   ├── webhook_sender.py      # 🆕 Новая нода
│   │   ├── save_image_s3.py
│   │   └── load_image_s3.py
│   └── nodes_mappings.py          # 🔄 Обновлено
├── WEBHOOK_NODE_USAGE.md          # 🆕 Документация
├── QUICKSTART_WEBHOOK.md          # 🆕 Быстрый старт
├── CHANGELOG_WEBHOOK.md           # 🆕 Этот файл
├── example_webhook_server.py      # 🆕 Тестовый сервер
├── test_webhook.py                # 🆕 Тестовый скрипт
├── example_workflow_webhook.json  # 🆕 Пример workflow
├── requirements.txt               # 🔄 Добавлен requests
└── README.md                      # 🔄 Обновлено
```

## Благодарности

Спасибо за использование Nextry ComfyS3! 

Если у вас есть вопросы или предложения, пожалуйста, создайте issue в репозитории.

