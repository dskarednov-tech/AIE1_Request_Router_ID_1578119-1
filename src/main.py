import argparse
import csv
import json
from collections import Counter


def read_json(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def read_csv(file_path):
    with open(file_path, "r", encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)
        return list(reader)


def normalize_record(raw):
    if "id" not in raw or "text" not in raw:
        raise ValueError

    record = {
        "id": str(raw["id"]).strip(),
        "text": str(raw["text"]).strip()
    }

    if not record["id"] or not record["text"]:
        raise ValueError

    return record


def load_requests(file_path):
    if file_path.endswith(".json"):
        raw_data = read_json(file_path)
    elif file_path.endswith(".csv"):
        raw_data = read_csv(file_path)
    else:
        raise ValueError

    requests = []

    for raw in raw_data:
        requests.append(normalize_record(raw))

    return requests


def normalize_text(text):
    text = text.lower()
    text = text.replace("ё", "е")

    return text


def detect_category(text):
    access_keywords = ("войти", "пароль", "нет доступа")
    billing_keywords = ("оплата", "счет", "тариф", "спис")
    bug_keywords = ("ошибка", "не работает", "падает", "недоступен")

    for keyword in access_keywords:
        if keyword in text:
            return "access"

    for keyword in billing_keywords:
        if keyword in text:
            return "billing"

    for keyword in bug_keywords:
        if keyword in text:
            return "bug"

    return "other"


def detect_priority(text, category):
    high_keywords = ("срочно", "критично", "недоступен всем")

    for keyword in high_keywords:
        if keyword in text:
            return "high"

    if category == "access" or category == "bug":
        return "medium"

    return "low"


def route_record(record):
    text = normalize_text(record["text"])
    category = detect_category(text)
    priority = detect_priority(text, category)

    return {
        "id": record["id"],
        "category": category,
        "priority": priority
    }


def route_requests(requests):
    routes = []

    for record in requests:
        route = route_record(record)
        routes.append(route)

    return routes


def print_category_stats(routes: list[dict[str, str]]) -> None:
    category_order = ("access", "billing", "bug", "other")
    counts = Counter(route["category"] for route in routes)

    print("Статистика по категориям:")
    for category in category_order:
        print(f"{category}: {counts[category]}")


def save_routes(routes, output_file):
    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(routes, file, ensure_ascii=False, indent=4)


def parse_args():
    parser = argparse.ArgumentParser(
        description="Маршрутизация обращений из JSON или CSV"
    )

    parser.add_argument(
        "--input",
        required=True,
        help="Путь к входному JSON или CSV файлу"
    )

    parser.add_argument(
        "--output",
        required=True,
        help="Путь к JSON файлу с результатом"
    )

    return parser.parse_args()


def main():
    args = parse_args()

    try:
        requests = load_requests(args.input)
        routes = route_requests(requests)

        save_routes(routes, args.output)
        print_category_stats(routes)
    except FileNotFoundError:
        print("Ошибка: входной файл не найден")
        return 1
    except json.JSONDecodeError:
        print("Ошибка: поврежденный JSON")
        return 1
    except ValueError:
        print("Ошибка: в записи отсутствует или пустое поле id или text")
        return 1
    return 0


raise SystemExit(main())
