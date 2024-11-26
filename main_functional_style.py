import json
from typing import List, Dict


COMMANDS = {
    1: 'Добавление книги',
    2: 'Удаление книги',
    3: 'Поиск книги',
    4: 'Отображение всех книг',
    5: "Изменение статуса книги",
    0: 'Выход',
}

DEFAULT_STATUS = "В наличии"
ALT_STATUS = "Выдана"


def read_file() -> List:
    """
    Чтение данных из файла 'data.json'

    Returns:
        Список книг из файла или пустой список, если файл не найден
    """
    try:
        with open(file='data.json', mode='r', encoding='utf-8') as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        return []


def save_to_file(data: List) -> None:
    """
    Сохранение данных в файл 'data.json'. Происход, когда пользовать выбриает вариант выхода из программы.

    Args:
        data: Список книг
    """
    with open(file='data.json', mode='w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=2)


def add_new_book(data: List) -> List:
    """
    Добавление новой книги

    Args:
        data: Список книг

    Returns:
        List: Обновленный список книг
    """
    new_book = {
        # для простоты id генерируется на основе последнего элемента, но лучше использовать встроенный модуль uuid или аналоги
        "id": data[-1]["id"] + 1 if data else 1,
        "title": input("Введите название книги: "),
        "author": input("Введите автора: "),
        "year": input("Введите год: "),
        "status": DEFAULT_STATUS,
    }

    if not new_book["title"]:
        print("Название не может быть пустым.")
        return data

    data.append(new_book)
    return data


def search_book(data: List) -> None:
    """
    Поиск книг по нескольким критериям: название, автор, год.

    Args:
        data: Список книг
    """
    title = input("Название книги (оставьте пустым для пропуска): ").lower()
    author = input("Автор книги (оставьте пустым для пропуска): ").lower()
    year = input("Год книги (оставьте пустым для пропуска): ").lower()

    results = [
        book for book in data
        if (not title or title in book["title"].lower()) and
           (not author or author in book["author"].lower()) and
           (not year or year == book["year"])
    ]

    if results:
        print("Найденные книги:")
        for book in results:
            print(book)
    else:
        print("Книги не найдены")


def show_all(data: List) -> None:
    """
    Вывод списка книг в консоль

    Args:
        data: Список книг
    """
    if not data:
        print("Список пуст")
    else:
        for item in data:
            print(item)


def find_book_by_id(data: List[Dict], id: int) -> Dict:
    """
    Поиск конкретной книги по id

    Args:
        data: Список книг
        id: id искомой книги

    Returns:
        List: Обновленный список книг
    """
    for book in data:
        if book["id"] == id:
            return book
    return {}


def del_book(data: List) -> List:
    """
    Удаление книги по id

    Args:
        data: Список книг

    Returns:
        List: Обновленный список книг
    """
    id = int(input("Введите id книги для удаления: "))
    book = find_book_by_id(data, id)
    if not book:
        print("Неверный id")
        return data
    data.remove(book)
    return data


def change_status(data: List) -> List:
    """
    Изменение статуса книги по id

    Args:
        data: Список книг

    Returns:
        Обновлённый список книг
    """
    id_to_change_status = int(input("Введите  id книги: "))

    book = find_book_by_id(data, id_to_change_status)
    if not book:
        print("Неверный id")
        return data

    if book["status"] == DEFAULT_STATUS:
        book["status"] = ALT_STATUS
    else:
        book["status"] = DEFAULT_STATUS

    print("Статус успешно изменен!")
    return data


def main() -> None:
    """
    Основная функция программы
    Запускает взаимодействие с пользователем и обрабатывает команды
    """
    data = read_file()

    while True:
        print()
        for key, value in COMMANDS.items():
            print(key, value)

        print('Введите номер опции: ', end='')
        user_choice = input()

        match user_choice:
            case "0":
                save_to_file(data)
                return
            case "1":
                data = add_new_book(data)
            case "2":
                data = del_book(data)
            case "3":
                search_book(data)
            case "4":
                show_all(data)
            case "5":
                data = change_status(data)
            case _:
                print("Неверный ввод")


if __name__ == "__main__":
    main()
