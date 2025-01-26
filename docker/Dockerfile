# Используем официальный образ Ubuntu 22.04
FROM ubuntu:22.04

# Устанавливаем переменные окружения для избежания вопросов при установке пакетов
ENV DEBIAN_FRONTEND=noninteractive

# Обновляем систему и устанавливаем необходимые пакеты
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3.10-venv \
    git \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем pydoc-markdown для генерации документации
RUN pip3 install pydoc-markdown

# Устанавливаем рабочую директорию
WORKDIR /workspace

# Команда по умолчанию
CMD ["sh"]