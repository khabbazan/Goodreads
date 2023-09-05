from django.db.models import Q, QuerySet

class BookQuerySet(QuerySet):
    """
    Custom queryset methods for the 'Book' model.

    Methods:
        - search(query): Filter books by title containing the specified query string.

    Attributes:
        None
    """

    def search(self, query):
        """
        Filter books by title containing the specified query string.

        Args:
            query (str): The query string to search for in book titles.

        Returns:
            QuerySet: A queryset containing books that match the search criteria.
        """
        return self.filter(Q(title__icontains=query)).distinct() if query else self

class TagQuerySet(QuerySet):
    """
    Custom queryset methods for the 'Tag' model.

    Methods:
        - search(query): Filter tags by name containing the specified query string.

    Attributes:
        None
    """

    def search(self, query):
        """
        Filter tags by name containing the specified query string.

        Args:
            query (str): The query string to search for in tag names.

        Returns:
            QuerySet: A queryset containing tags that match the search criteria.
        """
        return self.filter(Q(name__icontains=query)).distinct() if query else self
