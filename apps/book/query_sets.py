from django.db.models import Q, QuerySet

class BookQuerySet(QuerySet):
    """
    Manager and queryset methods
    """

    def search(self, query):
        """
        Search in listed items of a user by `__icontains` policy in phone numbers.
        """
        return self.filter(Q(title__icontains=query)).distinct() if query else self
