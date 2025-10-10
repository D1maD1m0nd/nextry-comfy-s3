# 📚 Webhook Sender Node - Documentation Index

> Полный путеводитель по кастомной ноде для отправки вебхуков из ComfyUI

---

## 🚀 Быстрый старт

**Хотите начать прямо сейчас?**

👉 **[QUICKSTART_WEBHOOK.md](./QUICKSTART_WEBHOOK.md)**

Краткая инструкция для быстрого запуска:
- Установка за 3 шага
- Базовое использование
- Примеры кода для разных фреймворков

---

## 📖 Документация

### 🎯 Основное руководство

**[WEBHOOK_NODE_USAGE.md](./WEBHOOK_NODE_USAGE.md)**

Полная документация по использованию ноды:
- Детальное описание всех параметров
- Входные и выходные данные
- Обработка ошибок
- Интеграция с backend
- Best practices

### 📊 Диаграммы и workflow

**[WORKFLOW_DIAGRAM.md](./WORKFLOW_DIAGRAM.md)**

Визуальное представление:
- Поток данных между нодами
- HTTP request/response структура
- Примеры различных workflow паттернов
- Схемы интеграции
- Error handling flow

### ❓ Часто задаваемые вопросы

**[WEBHOOK_FAQ.md](./WEBHOOK_FAQ.md)**

35+ вопросов и ответов:
- Установка и настройка
- Использование и подключение
- Troubleshooting
- Backend интеграция
- Производительность
- Продакшен

### 📝 Changelog

**[CHANGELOG_WEBHOOK.md](./CHANGELOG_WEBHOOK.md)**

История изменений:
- Новые возможности
- Технические детали
- Структура файлов
- Use cases

### 📋 Implementation Summary

**[WEBHOOK_IMPLEMENTATION_SUMMARY.md](./WEBHOOK_IMPLEMENTATION_SUMMARY.md)**

Обзор реализации:
- Список всех созданных файлов
- Как начать использовать
- Основные возможности
- Примеры интеграции

---

## 💻 Код и примеры

### 🔧 Основная нода

**`src/nodes/webhook_sender.py`**

Исходный код ноды:
```python
class NextryWebhookSender:
    """Отправка webhook уведомлений"""
    # Полная реализация с обработкой ошибок
```

### 🧪 Тестирование

**`test_webhook.py`**

Тестовый скрипт:
```bash
# Тест с локальным сервером
python test_webhook.py

# Тест с httpbin.org
python test_webhook.py --httpbin
```

**`example_webhook_server.py`**

Flask сервер для тестирования:
```bash
pip install flask
python example_webhook_server.py
# Сервер на http://localhost:8000
```

### 📦 Пример workflow

**`example_workflow_webhook.json`**

Готовый JSON для импорта в ComfyUI:
- Load Image → Save to S3 → Webhook Sender
- Импортируйте и используйте

---

## 📚 Документация по категориям

### Для новичков

1. **[QUICKSTART_WEBHOOK.md](./QUICKSTART_WEBHOOK.md)** - Начните здесь
2. **[WORKFLOW_DIAGRAM.md](./WORKFLOW_DIAGRAM.md)** - Визуализация
3. **[WEBHOOK_FAQ.md](./WEBHOOK_FAQ.md)** - Раздел "Общие вопросы"

### Для разработчиков

1. **[WEBHOOK_NODE_USAGE.md](./WEBHOOK_NODE_USAGE.md)** - Детальная документация
2. **`src/nodes/webhook_sender.py`** - Исходный код
3. **[WEBHOOK_FAQ.md](./WEBHOOK_FAQ.md)** - Раздел "Разработка и кастомизация"

### Для DevOps

1. **[WEBHOOK_NODE_USAGE.md](./WEBHOOK_NODE_USAGE.md)** - Раздел "Требования"
2. **[WEBHOOK_FAQ.md](./WEBHOOK_FAQ.md)** - Раздел "Продакшен"
3. **`example_webhook_server.py`** - Пример сервера

### Для troubleshooting

1. **[WEBHOOK_FAQ.md](./WEBHOOK_FAQ.md)** - Раздел "Ошибки и troubleshooting"
2. **[WEBHOOK_NODE_USAGE.md](./WEBHOOK_NODE_USAGE.md)** - Раздел "Обработка ошибок"
3. ComfyUI Console - Проверьте логи

---

## 🎯 Use Cases и примеры

### Use Case 1: Уведомление backend

```
Workflow: Generate → Save S3 → Webhook
Backend: Получает пути, скачивает изображения
```

**Документация:**
- [WORKFLOW_DIAGRAM.md](./WORKFLOW_DIAGRAM.md) - "Complete Pipeline"
- [WEBHOOK_FAQ.md](./WEBHOOK_FAQ.md) - Q21, Q24

### Use Case 2: Автоматическая пост-обработка

```
Workflow: Generate → Save S3 → Webhook
Backend: Применяет фильтры, создает thumbs, сохраняет в DB
```

**Документация:**
- [WEBHOOK_NODE_USAGE.md](./WEBHOOK_NODE_USAGE.md) - "Интеграция с backend"
- [WEBHOOK_FAQ.md](./WEBHOOK_FAQ.md) - Q23

### Use Case 3: Event-driven архитектура

```
Workflow: Generate → Save S3 → Webhook
Backend: Публикует в Event Bus → Множество сервисов
```

**Документация:**
- [WORKFLOW_DIAGRAM.md](./WORKFLOW_DIAGRAM.md) - "Pattern 3: Event-Driven"

---

## 📥 Установка

### Шаг 1: Зависимости

```bash
cd e:\ai\ComfyUI_windows_portable\ComfyUI\custom_nodes\nextry-comfy-s3
pip install -r requirements.txt
```

### Шаг 2: Перезапуск

Перезапустите ComfyUI

### Шаг 3: Проверка

Найдите "Nextry Webhook Sender" в категории NEXTRY_ComfyS3

**Проблемы с установкой?** → [WEBHOOK_FAQ.md](./WEBHOOK_FAQ.md) Q4-Q6

---

## 🔍 Быстрый поиск

### Ищете как...

**...установить ноду?**
→ [QUICKSTART_WEBHOOK.md](./QUICKSTART_WEBHOOK.md) - Шаг 1

**...подключить к Save Image S3?**
→ [WEBHOOK_FAQ.md](./WEBHOOK_FAQ.md) - Q9

**...настроить свой backend?**
→ [WEBHOOK_NODE_USAGE.md](./WEBHOOK_NODE_USAGE.md) - "Интеграция с backend"

**...обработать ошибки?**
→ [WEBHOOK_NODE_USAGE.md](./WEBHOOK_NODE_USAGE.md) - "Обработка ошибок"

**...протестировать без сервера?**
→ [WEBHOOK_FAQ.md](./WEBHOOK_FAQ.md) - Q15

**...добавить аутентификацию?**
→ [WEBHOOK_FAQ.md](./WEBHOOK_FAQ.md) - Q19

**...использовать в продакшене?**
→ [WEBHOOK_FAQ.md](./WEBHOOK_FAQ.md) - Q29-Q30

**...понять поток данных?**
→ [WORKFLOW_DIAGRAM.md](./WORKFLOW_DIAGRAM.md)

---

## 🛠️ Структура проекта

```
nextry-comfy-s3/
│
├── 📁 src/
│   ├── 📁 nodes/
│   │   ├── webhook_sender.py          ⭐ Основная нода
│   │   ├── save_image_s3.py
│   │   └── load_image_s3.py
│   └── nodes_mappings.py              🔄 Регистрация нод
│
├── 📖 Документация:
│   ├── WEBHOOK_DOCUMENTATION_INDEX.md  👈 Вы здесь
│   ├── QUICKSTART_WEBHOOK.md           🚀 Начните здесь
│   ├── WEBHOOK_NODE_USAGE.md           📚 Полное руководство
│   ├── WORKFLOW_DIAGRAM.md             📊 Диаграммы
│   ├── WEBHOOK_FAQ.md                  ❓ 35+ Q&A
│   ├── CHANGELOG_WEBHOOK.md            📝 История
│   └── WEBHOOK_IMPLEMENTATION_SUMMARY.md
│
├── 🧪 Тестирование:
│   ├── test_webhook.py                 Тестовый скрипт
│   ├── example_webhook_server.py       Flask сервер
│   └── example_workflow_webhook.json   Пример workflow
│
├── ⚙️ Конфигурация:
│   ├── requirements.txt                Зависимости
│   └── README.md                       Общий README
│
└── 📄 Прочее:
    ├── __init__.py
    └── pyproject.toml
```

---

## 📱 Краткая справка

### Параметры ноды

| Параметр | Тип | Описание |
|----------|-----|----------|
| `endpoint` | STRING | URL для webhook |
| `preview_image` | STRING | Путь к preview |
| `stock_image` | STRING | Путь к stock |

### Payload

```json
{
  "preview_image": "s3://...",
  "stock_image": "s3://..."
}
```

### Response (Success)

```json
{
  "success": true,
  "status_code": 200,
  "response": {...}
}
```

### Response (Error)

```json
{
  "success": false,
  "error": "timeout|request_failed|unknown",
  "message": "Error description"
}
```

---

## 🎓 Обучающие материалы

### Шаг за шагом

1. **Установка** → [QUICKSTART_WEBHOOK.md](./QUICKSTART_WEBHOOK.md)
2. **Понимание** → [WORKFLOW_DIAGRAM.md](./WORKFLOW_DIAGRAM.md)
3. **Использование** → [WEBHOOK_NODE_USAGE.md](./WEBHOOK_NODE_USAGE.md)
4. **Тестирование** → `test_webhook.py` + `example_webhook_server.py`
5. **Продакшен** → [WEBHOOK_FAQ.md](./WEBHOOK_FAQ.md) Q29-Q30

### Видео-туториал (если создадите)

1. Установка и настройка
2. Создание первого webhook
3. Интеграция с backend
4. Troubleshooting

---

## 🔗 Ссылки

### Внутренние

- [Main README](./README.md) - Общая информация о проекте
- [Requirements](./requirements.txt) - Зависимости

### Внешние

- [ComfyUI](https://github.com/comfyanonymous/ComfyUI) - Основной проект
- [httpbin.org](https://httpbin.org) - Тестирование HTTP запросов
- [requests docs](https://requests.readthedocs.io/) - Библиотека HTTP

---

## 💡 Tips & Tricks

### Совет 1: Быстрое тестирование

```bash
# Используйте httpbin для быстрой проверки
endpoint: https://httpbin.org/post
```

### Совет 2: Отладка

```python
# Проверяйте логи ComfyUI для деталей
# Все запросы логируются с полными данными
```

### Совет 3: Локальный сервер

```bash
# Всегда держите пример сервера под рукой
python example_webhook_server.py
```

### Совет 4: Импорт workflow

```
File → Load → example_workflow_webhook.json
```

### Совет 5: Множественные webhook'и

```
Добавьте несколько нод Webhook Sender для
отправки на разные endpoints одновременно
```

---

## 🎯 Roadmap (возможные улучшения)

- [ ] Batch processing поддержка
- [ ] Retry логика внутри ноды
- [ ] Webhook signatures для безопасности
- [ ] Async отправка (non-blocking)
- [ ] Custom headers configuration
- [ ] Rate limiting
- [ ] Webhook history/logging UI

---

## 📞 Поддержка

### Вопросы?

1. Проверьте [FAQ](./WEBHOOK_FAQ.md)
2. Изучите [документацию](./WEBHOOK_NODE_USAGE.md)
3. Запустите [тесты](./test_webhook.py)
4. Создайте issue в репозитории

### Нашли баг?

1. Проверьте логи ComfyUI
2. Воспроизведите с тестовым сервером
3. Создайте issue с деталями

### Хотите улучшить?

1. Fork репозитория
2. Внесите изменения
3. Создайте Pull Request

---

## 🙏 Благодарности

Спасибо за использование Nextry Webhook Sender!

Если нода оказалась полезной:
- ⭐ Поставьте звезду репозиторию
- 📢 Расскажите коллегам
- 🐛 Сообщайте о багах
- 💡 Предлагайте улучшения

---

## 📄 Лицензия

См. [LICENSE](./LICENSE) файл в корне проекта.

---

**Версия документации:** 1.0.0  
**Дата создания:** 2025-10-10  
**Последнее обновление:** 2025-10-10

---

<div align="center">

### 🚀 Готовы начать?

**[→ Начать с Quickstart Guide](./QUICKSTART_WEBHOOK.md)**

</div>

