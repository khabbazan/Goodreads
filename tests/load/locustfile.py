from locust import HttpUser, task, between

class GraphQLUser(HttpUser):
    """
    Load testing user for a GraphQL API.

    This class defines a Locust user for load testing a GraphQL API. It performs authentication
    to obtain a JWT token and then sends various GraphQL queries as tasks.

    Attributes:
        wait_time (tuple): A tuple specifying the range of time to wait between tasks.
            Default is between 1 and 5 seconds.

    """

    wait_time = between(1, 5)

    def on_start(self):
        """
        Perform authentication to obtain the JWT token.

        This method is automatically called when a user starts. It performs the authentication
        process and stores the JWT token for use in GraphQL queries.

        """

        # Perform authentication to obtain the JWT token
        login_response = self._perform_login()
        self.jwt_token = login_response['data']['createLogin']['token']

    @task
    def user_list(self):
        """
        Task to fetch a list of users.

        This task sends a GraphQL query to fetch a list of users and records the response time.

        """

        query = """
        query{
            userList{
                data{
                    id
                    phoneNumber
                }
                pageCount
                count
            }
        }
        """
        self._perform_query(query, name="User List")

    @task
    def author_list(self):
        """
        Task to fetch a list of authors.

        This task sends a GraphQL query to fetch a list of authors and records the response time.

        """

        query = """
        query{
            authorList{
                data{
                    id
                    firstName
                    lastName
                }
                pageCount
                count
            }
        }
        """
        self._perform_query(query, name="Author List")

    @task
    def book_list(self):
        """
        Task to fetch a list of books.

        This task sends a GraphQL query to fetch a list of books and records the response time.

        """

        query = """
            query{
                bookList{
                    data {
                        id
                        ISBN
                        title
                    }
                    pageCount
                    count
                }
            }
        """
        self._perform_query(query, name="Book List")

    @task
    def tag_list(self):
        """
        Task to fetch a list of tags.

        This task sends a GraphQL query to fetch a list of tags and records the response time.

        """

        query = """
            query {
                tagList {
                    id
                    name
                    displayName
                }
            }
        """
        self._perform_query(query, name="Tag List")

    def _perform_login(self):
        """
        Perform the login operation to obtain the JWT token.

        This method sends a GraphQL mutation to perform the login operation and obtain a JWT token.

        Returns:
            dict: A dictionary containing the login response.

        """

        login_data = {
            'phoneNumber': '<USER PHONENUMBER>',
            'password': '<USER PASSWORD>',
        }
        headers = {'Content-Type': 'application/json'}
        login_mutation = """
        mutation createLogin($data: UserInputType!) {
          createLogin(userInput: $data) {
              ... on ResponseWithToken {
                            token
                        }
                    }
                }
        """
        variables = {'data': login_data}

        login_response = self.client.post('graphql/', name="Login", headers=headers, json={'query': login_mutation, 'variables': variables})
        return login_response.json()

    def _perform_query(self, query, name):
        """
        Perform a GraphQL query.

        This method sends a GraphQL query with the provided query string and records the response time.

        Args:
            query (str): The GraphQL query string to be sent.
            name (str): The name to be associated with this request.

        """

        headers = {
            "Accept": "application/json",
            "Accept-Language": "en-US,en;q=0.9,fa;q=0.8",
            "Authorization": f"JWT {self.jwt_token}"
        }
        response = self.client.post('graphql/', name=name, headers=headers, json={'query': query})
