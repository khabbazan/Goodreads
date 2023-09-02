from apps.book.gql.book.mutations import BookAdd
from apps.book.gql.book.mutations import BookEdit
from apps.book.gql.shelf.mutations import AddBookToShelf
from apps.book.gql.shelf.mutations import RemoveBookFromShelf
from apps.book.gql.shelf.mutations import ChangeBookFromShelf

from apps.book.gql.book.queries import BookList
from apps.book.gql.book.queries import BookDetail
from apps.book.gql.shelf.queries import UserShelfList

class Query(BookList, BookDetail, UserShelfList):
    pass


class Mutation:

    book_add = BookAdd.Field()
    book_edit = BookEdit.Field()
    add_book_shelf = AddBookToShelf.Field()
    remove_book_shelf = RemoveBookFromShelf.Field()
    change_book_shelf = ChangeBookFromShelf.Field()
