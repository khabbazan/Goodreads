from django.db.models import Q, QuerySet

class UserQuerySet(QuerySet):
    """
    Custom query set for the 'User' model.

    Attributes:
        None

    Methods:
        - search(query): Searches for users by phone number using `__icontains` policy.
    """

    def search(self, query):
        """
        Searches for users by phone number using `__icontains` policy.

        Args:
            query (str): The search query.

        Returns:
            QuerySet: Filtered query set of users.
        """
        return self.filter(Q(phone_number__icontains=query)).distinct() if query else self

class AuthorQuerySet(QuerySet):
    """
    Custom query set for the 'Author' model.

    Attributes:
        None

    Methods:
        - search(query): Searches for authors by first name or last name using `__icontains` policy.
    """

    def search(self, query):
        """
        Searches for authors by first name or last name using `__icontains` policy.

        Args:
            query (str): The search query.

        Returns:
            QuerySet: Filtered query set of authors.
        """
        return self.filter(Q(first_name__icontains=query) | Q(last_name__icontains=query)).distinct() if query else self
