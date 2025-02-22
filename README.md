# OllamaChatBot

Telegram-бот с интеграцией Ollama для обработки сообщений через LLM-модель, использующий Kafka, Redis и FastAPI для масштабируемой асинхронной архитектуры.

## 📋 Особенности
- **Асинхронная обработка** сообщений через Kafka.
- **Кэширование ответов** в Redis для снижения нагрузки на модель.
- **Веб-интерфейс** на FastAPI для мониторинга и управления.
- **Docker-контейнеризация** всех компонентов (Zookeeper, Kafka, Redis, Ollama, бот).
- Поддержка модели **Vikhr-Llama-3.2-1B-instruct** (HF) через Ollama.

## 🚀 Быстрый старт

### Предварительные требования
- Установленные [Docker](https://docs.docker.com/get-docker/) и [Docker Compose](https://docs.docker.com/compose/install/).

### Установка
1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/sergey-brovko/OllamaChatBot.git
   cd OllamaChatBot
   ```
2. Запустите сервисы:
   ```bash
   docker-compose up --build
   ```

## ⚙️ Конфигурация
Настройки через переменные окружения (`.env`):
```env
TELEGRAM_BOT_TOKEN=ваш_токен_бота
OLLAMA_MODEL=hf.co/Vikhrmodels/Vikhr-Llama-3.2-1B-instruct-GGUF:F16
OLLAMA_BASE_URL=http://ollama:11434
REDIS_URL=redis://redis:6379/0
KAFKA_BOOTSTRAP_SERVERS=kafka:9092
KAFKA_TOPIC=chat_messages
```

## 🏗 Архитектура
1. **Telegram Bot (aiogram3)**: Принимает сообщения → отправляет в Kafka.
2. **Kafka**: Очередь для асинхронной обработки.
3. **Ollama Worker**: Получает задачи из Kafka → генерирует ответ через LLM → сохраняет в Redis.
4. **Redis**: Кэш для быстрого доступа к ответам.
5. **FastAPI**: Веб-интерфейс для статистики и управления.
6. **Zookeeper**: Координация Kafka-кластера.

## 📖 Примеры использования
### Через Telegram
1. Найдите бота в Telegram.
2. Отправьте сообщение:
   ```
   /start
   Привет! Как настроить Kafka?
   ```

### Через API
Отправить запрос:
```bash
curl -X POST -H "Content-Type: application/json" -d '{"prompt":"Why is the sky blue?"}' http://localhost:8000/generate
```
Проверить результат (используйте возвращенный request_id):
```bash
curl http://localhost:8000/result/<request_id>
```

## 🤝 Как помочь проекту
- Сообщайте о багах в [Issues](https://github.com/sergey-brovko/OllamaChatBot/issues).
- Присылайте улучшения через Pull Requests.

## 📄 Лицензия
MIT License. Подробнее в файле [LICENSE](LICENSE).

