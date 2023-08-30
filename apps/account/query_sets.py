from django.db.models import Q, QuerySet

class UserQuerySet(QuerySet):
    """
    Manager and queryset methods
    """

    def search(self, query):
        """
        Search in listed items of a user by `__icontains` policy in phone numbers.
        """
        return self.filter(Q(phone_number__icontains=query)).distinct() if query else self

class AuthorQuerySet(QuerySet):
    """
    Manager and queryset methods
    """

    def search(self, query):
        """
        Search in listed items of a user by `__icontains` policy in phone numbers.
        """
        return self.filter(Q(first_name__icontains=query) | Q(last_name__icontains=query)).distinct() if query else self
