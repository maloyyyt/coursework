import json
import logging
from logging import Logger
from pathlib import Path
from typing import Any

import pandas as pd


def setup_logging(name: str = __name__) -> Logger:
    """
    Функция, которая настраивает логирование.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # Создаем обработчик для записи в файл
    file_handler = logging.FileHandler("logs.log", mode="w", encoding="utf-8")
    file_handler.setLevel(logging.INFO)

    # Создаем форматтер для сообщений лога
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(formatter)

    # Добавляем обработчик к логгеру
    logger.addHandler(file_handler)

    # Создаем обработчик для вывода в консоль (если нужно)
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)


    return logger


logger = setup_logging()


def read_files(file_path: Any) -> pd.DataFrame:
    """Открытие файла '.xls' или '.xlsx'."""
    if file_path is None:
        raise ValueError("Путь к файлу не может быть None")

    file_path = Path(file_path)
    suffix = file_path.suffix.lower()

    if suffix in [".xls", ".xlsx"]:
        try:
            engine = "openpyxl" if suffix == ".xlsx" else "xlrd"
            df = pd.read_excel(file_path, engine=engine)
            logger.info(f"Успешно прочитан Excel-файл: {file_path}")
            return df
        except FileNotFoundError:
            logger.error(f"Файл не найден: {file_path}")
            raise ValueError(f"Файл не найден: {file_path}")
        except Exception as e:
            logger.error(f"Не удалось прочитать Excel-файл {file_path}: {e}")
            raise ValueError(f"Не удалось прочитать Excel-файл {file_path}: {e}") from e
    elif suffix == ".json":
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            df = pd.DataFrame(data)
            logger.info(f"Успешно прочитан JSON-файл: {file_path}")
            return df
        except FileNotFoundError:
            logger.error(f"Файл не найден: {file_path}")
            raise ValueError(f"Файл не найден: {file_path}")
        except json.JSONDecodeError as e:
            logger.error(f"Ошибка декодирования JSON в файле {file_path}: {e}")
            raise ValueError(f"Ошибка декодирования JSON в файле {file_path}: {e}") from e
        except Exception as e:
            logger.error(f"Не удалось прочитать JSON-файл {file_path}: {e}")
            raise ValueError(f"Не удалось прочитать JSON-файл {file_path}: {e}") from e
    else:
        logger.error(f"Неверный формат файла: {file_path}")
        raise ValueError(f"Неверный формат файла: {file_path}")


def write_data(file_: str, results: Any) -> None:
    """
    Функция, которая записывает результаты в указанный файл.
    """
    try:
        if file_.endswith(".txt"):
            with open(file_, "a", encoding="utf-8") as file:
                if isinstance(results, str):
                    file.write(results)
                else:
                    file.write(str(results))  # Преобразуем в строку
                logger.info(f"Успешно записаны результаты в текстовый файл: {file_}")
        else:
            with open(file_, "w", encoding="utf8") as f:
                json.dump(results, f, indent=4, ensure_ascii=False)
                logger.info(f"Успешно записаны результаты в JSON-файл: {file_}")
    except Exception as e:
        logger.error(f"Ошибка записи в файл {file_}: {e}")
        raise


if __name__ == '__main__':
    try:
        # Чтение Excel
        excel_data = read_files("data/operations.xls")
        print("Excel data (first 5 rows):\n", excel_data.head())

        # Чтение JSON
        json_data = read_files("reports.json")
        print("JSON data (first 5 rows):\n", json_data.head())

        # Запись в JSON
        write_data("output.json", {"key": "value", "data": [1, 2, 3]})

        # Запись в TXT
        write_data("output.txt", "This is a test string.\n")
        write_data("output.txt", "Another line of text.\n")

    except ValueError as e:
        print(f"Ошибка: {e}")
    except Exception as e:
        print(f"Произошла непредвиденная ошибка: {e}")
