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


class Book:
    DEFAULT_STATUS = "В наличии"
    ALT_STATUS = "Выдана"

    def __init__(self, id: int, title: str, author: str, year: str, status: str = DEFAULT_STATUS):
        self.id = id
        self.title = title
        self.author = author
        self.year = year
        self.status = status

    def change_status(self):
        """Меняет статус книги"""
        self.status = self.ALT_STATUS if self.status == self.DEFAULT_STATUS else self.DEFAULT_STATUS

    def __str__(self):
        return f"ID: {self.id}, Название: {self.title}, Автор: {self.author}, Год: {self.year}, Статус: {self.status}"


class Library:
    def __init__(self):
        self.books = []

    def add_book(self, title: str, author: str, year: str):
        """Добавляет новую книгу"""
        if not title:
            print("Название не может быть пустым!")
            return
        id = self.books[-1].id + 1 if self.books else 1
        new_book = Book(id, title, author, year)
        self.books.append(new_book)

    def remove_book(self, id: int):
        """Удаляет книгу по ID"""
        book = self.find_book(id)
        if book:
            self.books.remove(book)
            print("Книга удалена")
        else:
            print("Книга с таким ID не найдена")

    def find_book(self, search_id: int):
        """Находит книгу по ID"""
        for book in self.books:
            if book.id == search_id:
                return book
        return None

    def search_books(self, title, author, year):
        """Ищет книги по критериям"""
        results = [
            book for book in self.books
            if (not title or title.lower() in book.title.lower()) and
               (not author or author.lower() in book.author.lower()) and
               (not year or year == book.year)
        ]
        return results

    def list_books(self):
        """Выводит все книги"""
        for book in self.books:
            print(book)


class Storage:
    @staticmethod
    def load_data(file_path: str) -> List[Book]:
        """Загружает данные из json файла"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                raw_data = json.load(file)
                data = [Book(**item) for item in raw_data]
                return data
        except (FileNotFoundError, json.JSONDecodeError):
            print("Не найден data.json, будет создан новый")
            return []

    @staticmethod
    def save_data(file_path: str, books: List[Book]):
        """Сохраняет данные в JSON файл"""
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump([book.__dict__ for book in books], file, ensure_ascii=False, indent=2)


def main():
    library = Library()
    library.books = Storage.load_data("data.json")

    while True:
        print("\nМеню:")
        for key, value in COMMANDS.items():
            print(f"{key}: {value}")

        user_choice = input("Введите номер опции: ").strip()

        match user_choice:
            case "1":
                title = input("Введите название книги: ")
                author = input("Введите автора книги: ")
                year = input("Введите год издания: ")
                library.add_book(title, author, year)
            case "2":
                id = int(input("Введите ID книги для удаления: "))
                library.remove_book(id)
            case "3":
                title = input("Название (оставьте пустым для пропуска): ")
                author = input("Автор (оставьте пустым для пропуска): ")
                year = input("Год (оставьте пустым для пропуска): ")
                results = library.search_books(title, author, year)
                if results:
                    print("Найденные книги:")
                    for book in results:
                        print(book)
                else:
                    print("Книги не найдены.")
            case "4":
                library.list_books()
            case "5":
                id = int(input("Введите ID книги для изменения статуса: "))
                book = library.find_book(id)
                if book:
                    book.change_status()
                    print("Статус изменён.")
                else:
                    print("Книга с таким ID не найдена.")
            case "0":
                Storage.save_data("data.json", library.books)
                print("Данные сохранены")
                break
            case _:
                print("Неверный выбор")


if __name__ == "__main__":
    main()
