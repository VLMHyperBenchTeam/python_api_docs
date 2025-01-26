import subprocess
import os
import shutil
from pathlib import Path


# Функция для клонирования репозитория
def clone_repo(repo_url, version, repo_dir):
    subprocess.run(
        ["git", "clone", "--branch", version, repo_url, repo_dir], check=True
    )


# Функция для создания виртуального окружения
def create_venv(venv_dir):
    subprocess.run(["python3", "-m", "venv", venv_dir], check=True)


# Функция для установки пакета в виртуальное окружение
def install_package(venv_dir, package_dir):
    pip_path = os.path.join(venv_dir, "bin", "pip")
    subprocess.run([pip_path, "install", package_dir], check=True)


# Функция для установки pydoc-markdown в виртуальное окружение
def install_pydoc_markdown(venv_dir):
    pip_path = os.path.join(venv_dir, "bin", "pip")
    subprocess.run([pip_path, "install", "pydoc-markdown"], check=True)


# Функция для генерации документации
def generate_docs(venv_dir, package_dir, output_dir):
    pydoc_markdown_path = os.path.join(venv_dir, "bin", "pydoc-markdown")
    result = subprocess.run(
        [pydoc_markdown_path, "-p", package_dir],
        check=True,
        capture_output=True,
        text=True,
    )

    if result.returncode == 0:
        # Открываем файл для записи (режим "w" — write)
        with open(f"{output_dir}.md", "w", encoding="utf-8") as file:
            file.write(result.stdout)

        print(f"Документация успешно сгенерирована: {output_dir}")
    else:
        print(result.stdou)


# Основная функция
def main():
    # Чтение файла repos.txt
    with open("repos.txt", "r") as file:
        repos = file.readlines()

    # Обработка каждого репозитория
    for repo_line in repos:
        repo_url, version = repo_line.strip().split()
        repo_name = repo_url.split("/")[-1].replace(".git", "")

        # Создание временных путей в /tmp
        tmp_dir = Path("/tmp")
        repo_dir = tmp_dir / repo_name
        venv_dir = tmp_dir / f"venv_{repo_name}"
        output_dir = Path("docs") / repo_name  # Документация сохраняется вне /tmp

        # Удаление старых временных файлов, если они существуют
        if repo_dir.exists():
            shutil.rmtree(repo_dir)
        if venv_dir.exists():
            shutil.rmtree(venv_dir)

        # Клонирование репозитория
        print(f"Клонирование репозитория {repo_url} версии {version}...")
        clone_repo(repo_url, version, repo_dir)

        # Создание виртуального окружения
        print(f"Создание виртуального окружения для {repo_name}...")
        create_venv(venv_dir)

        # Установка pydoc-markdown в виртуальное окружение
        print(f"Установка pydoc-markdown для {repo_name}...")
        install_pydoc_markdown(venv_dir)

        # Установка пакета
        print(f"Установка пакета {repo_name}...")
        install_package(venv_dir, repo_dir)

        # Генерация документации
        print(f"Генерация документации для {repo_name}...")
        generate_docs(venv_dir, repo_dir, output_dir)

        # Удаление временных файлов (репозитория и виртуального окружения)
        print(f"Очистка временных файлов для {repo_name}...")
        shutil.rmtree(repo_dir)
        shutil.rmtree(venv_dir)

        print(
            f"Документация для {repo_name} успешно сгенерирована и сохранена в {output_dir}\n"
        )


if __name__ == "__main__":
    main()
