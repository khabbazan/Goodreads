# Goodreads GraphQL API Project

This Django project utilizes Django 4.2 and GraphQL v3 to provide GraphQL APIs for a simplified version of Goodreads. Goodreads is a website where users can share books and organize them on their shelves with labels such as want-to-read, read, and currently-read.

## GraphQL APIs

This project offers the following GraphQL APIs:

### Queries
- `UserList`: List of users.
- `UserDetail`: User details.
- `AuthorList`: List of authors.
- `AuthorDetail`: Author details.
- `UserFollowerList`: List of followers for a user.
- `UserFollowingList`: List of users a user is following.
- `BookList`: List of books.
- `BookDetail`: Book details.
- `UserShelfList`: List of books on a user's shelf.
- `TagList`: List of tags.

### Mutations
- `verifyToken`: Verify a user's token.
- `refreshToken`: Refresh a user's token.
- `createLogin`: Create a login session.
- `logout`: Log a user out.
- `userEdit`: Edit user information.
- `authorEdit`: Edit author information.
- `userFollow`: Follow a user.

## Features

- Rate limiting settings.
- Image handling through an S3 object server using Django Storage.
- Redis cache system for queries, with cache expiration for related mutations.
- Load testing scenario using Locust in the test directory to evaluate API performance.
- Notification handling via Django signals with email.

## Setup and Installation

1. Clone this repository.
2. Create a .env file for storing the environment variables.
3. Install the required dependencies using `pip install -r requirements.txt`.
4. Configure your Django settings and database connection.
5. Migrate the database using `python manage.py migrate`.
6. Run the development server with `python manage.py runserver`.

### Configuration (When Debug Mode is Turned Off)

When running this project under practical mode, you should provide the following configurations in the .env file:

#### 1. PostgreSQL Configuration
   Configure your PostgreSQL database connection in the project's .env file.

```python
DATABASES = {
  "default": {
      "ENGINE": "django.db.backends.postgresql",
      "NAME": os.getenv("DATABASE_NAME"),
      "USER": os.getenv("DATABASE_USERNAME"),
      "PASSWORD": os.getenv("DATABASE_PASSWORD"),
      "HOST": os.getenv("DATABASE_HOST"),
      "PORT": os.getenv("DATABASE_PORT"),
  }
}
```
#### 2. Email Configuration for Welcome Notification
Configure your email settings for sending welcome notifications when users authenticate.

```python
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_PORT = os.getenv("EMAIL_PORT")
EMAIL_USE_TLS = True
EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
  ```

#### 3. S3 Settings for Image Model
Configure S3 settings for the image model, which serves as an object server for handling images and static files.

```python
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = os.getenv("AWS_STORAGE_BUCKET_NAME")
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
STATIC_URL = "https://%s/" % AWS_S3_CUSTOM_DOMAIN
MEDIA_URL = "https://%s/" % AWS_S3_CUSTOM_DOMAIN
```


## Project Documentation

You can find Entity-Relationship (ER) diagrams in the `documents` directory. These diagrams have been generated using Django Extensions and Graphviz to help you understand the project's database schema.

## Testing

You can run the load test scenario using Locust by following the instructions in the `tests` directory.

## Contributors

- [Alireza Khabbazan](https://github.com/khabbazan)

## License

This project is open for contributions, and contributions are welcome from the community. It is licensed under the terms of MIT. Feel free to fork, contribute, and make this project even better!
