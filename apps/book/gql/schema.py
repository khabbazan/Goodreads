from apps.book.gql.book.mutations import BookAdd
from apps.book.gql.book.mutations import BookEdit

from apps.book.gql.book.queries import BookList
from apps.book.gql.book.queries import BookDetail

class Query(BookList, BookDetail):
    pass


class Mutation:

    book_add = BookAdd.Field()
    book_edit = BookEdit.Field()
