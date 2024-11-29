from main import BooksCollector
import pytest


# класс TestBooksCollector объединяет набор тестов, которыми мы покрываем наше приложение BooksCollector
# обязательно указывать префикс Test
class TestBooksCollector:

    # пример теста:
    # обязательно указывать префикс test_
    # дальше идет название метода, который тестируем add_new_book_
    # затем, что тестируем add_two_books - добавление двух книг
    # ЗАККОМЕНТИРОВАЛ ПОТОМУ ЧТО НЕТ МЕТОДА ДОБАВЛЕНИЯ ДВУХ КНИГ
    # def test_add_new_book_add_two_books(self):
    #     # создаем экземпляр (объект) класса BooksCollector
    #     collector = BooksCollector()
    #
    #     # добавляем две книги
    #     collector.add_new_book('Гордость и предубеждение и зомби')
    #     collector.add_new_book('Что делать, если ваш кот хочет вас убить')
    #
    #     # проверяем, что добавилось именно две
    #     # словарь books_rating, который нам возвращает метод get_books_rating, имеет длину 2
    #     assert len(collector.get_books_rating()) == 2

    # напиши свои тесты ниже
    # чтобы тесты были независимыми в каждом из них создавай отдельный экземпляр класса BooksCollector()

    @pytest.fixture
    def collector(self):
        return BooksCollector()

    def test_add_new_book(self, collector):
        collector.add_new_book("Новая книга")
        assert "Новая книга" in collector.books_genre
        assert collector.books_genre['Новая книга'] == ''

    def test_add_new_book_length_name(self, collector):
        collector.add_new_book("a" * 41)
        assert len(collector.books_genre) == 0
        collector.add_new_book("Новая книга")
        assert len(collector.books_genre) == 1

    @pytest.mark.parametrize("genre", ['Фантастика', 'Ужасы', 'Детективы', 'Мультфильмы', 'Комедии'])
    def test_set_book_genre_allowed(self, collector, genre):
        collector.add_new_book("book1")
        collector.set_book_genre("book1", genre)
        assert collector.get_book_genre("book1") == genre

    def test_set_book_genre_not_allowed(self, collector):
        collector.add_new_book("book1")
        collector.set_book_genre("book1", "Некорректный жанр")
        assert collector.get_book_genre("book1") == ''

    def test_set_book_genre_no_book(self, collector):
        collector.set_book_genre("book1", "Ужасы")
        assert collector.get_book_genre("book1") is None

    def test_get_book_genre(self, collector):
        collector.add_new_book("book1")
        assert collector.get_book_genre("book1") == ''
        collector.set_book_genre("book1", "Фантастика")
        assert collector.get_book_genre("book1") == "Фантастика"
        assert collector.get_book_genre("неизвестная книга") is None

    @pytest.mark.parametrize("genre, expected_books", [
        ("Фантастика", ["book2"]),
        ("Комедии", []),
        ("Неизвестный", [])
    ])
    def test_get_books_with_specific_genre(self, collector, genre, expected_books):
        collector.add_new_book("book2")
        collector.set_book_genre("book2", "Фантастика")
        books = collector.get_books_with_specific_genre(genre)
        assert books == expected_books

    def test_get_books_genre(self, collector):
        collector.add_new_book("book3")
        collector.set_book_genre("book3", "Детективы")
        books = collector.get_books_genre()
        assert books == {"book3": "Детективы"}

    def test_get_books_for_children(self, collector):
        collector.add_new_book("book4")
        collector.set_book_genre("book4", "Фантастика")
        collector.add_new_book("book5")
        collector.set_book_genre("book5", "Детективы")
        children_books = collector.get_books_for_children()
        assert "book4" in children_books
        assert "book5" not in children_books

    def test_add_book_in_favorites(self, collector):
        collector.add_new_book("book6")
        collector.set_book_genre("book6", "Фантастика")
        collector.add_book_in_favorites("book6")
        assert "book6" in collector.get_list_of_favorites_books()
        collector.add_book_in_favorites("book6")
        assert collector.get_list_of_favorites_books().count("book6") == 1

    def test_delete_book_from_favorites(self, collector):
        collector.add_new_book("book7")
        collector.set_book_genre("book7", "Фантастика")
        collector.add_book_in_favorites("book7")
        collector.delete_book_from_favorites("book7")
        assert "book7" not in collector.get_list_of_favorites_books()

    def test_delete_book_from_favorites_no_book(self, collector):
        assert len(collector.get_list_of_favorites_books()) == 0
        collector.delete_book_from_favorites('book7')
        assert len(collector.get_list_of_favorites_books()) == 0

    def test_get_list_of_favorites_books(self, collector):
        collector.add_new_book("book8")
        collector.set_book_genre("book8", "Фантастика")
        collector.add_book_in_favorites("book8")
        favorites = collector.get_list_of_favorites_books()
        assert "book8" in favorites