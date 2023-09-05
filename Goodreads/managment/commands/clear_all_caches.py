from django.core.management.base import BaseCommand
from django.core.cache import cache

class Command(BaseCommand):
    """
    A Django management command to clear all caches.

    This custom management command allows you to clear all cached data in your Django application's cache backend.
    It provides a convenient way to refresh cached information when needed.

    Attributes:
        help (str): A short description of the command displayed in the command-line help.

    Methods:
        handle(self, *args, **options):
            Clears all caches and provides feedback on the operation's success or failure.

            Args:
                *args: Additional positional arguments.
                **options: Additional keyword arguments.

            Raises:
                Exception: If there is an error during the cache clearing process, an exception is raised.

            Example:
                To clear all caches, you can run the following command:

                ```
                python manage.py clearcaches
                ```

                This command will clear all the caches and print a success message if the operation is successful.
                If there is an error while clearing the caches, it will display an error message.
    """

    help = 'Clear all caches'

    def handle(self, *args, **options):
        """
        Clears all caches and provides feedback on the operation's success or failure.

        Args:
            *args: Additional positional arguments.
            **options: Additional keyword arguments.

        Raises:
            Exception: If there is an error during the cache clearing process, an exception is raised.
        """
        try:
            cache.clear()
            self.stdout.write(self.style.SUCCESS('Successfully cleared all caches.'))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f'Failed to clear caches: {str(e)}'))

