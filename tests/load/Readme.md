# GraphQL API Load Test with Locust

This repository contains a load test script for testing GraphQL APIs using [Locust](https://locust.io/). The load test simulates user behavior for four GraphQL queries: "user_list," "author_list," "book_list," and "tag_list."

## Prerequisites

Before running the load test, ensure you have the following prerequisites:

- Python installed (version 3.10 or higher)
- Locust installed (`pip install locust`)
- Access to the GraphQL API endpoint you want to test

## Usage

1. Clone this repository to your local machine:

   ```bash
   git clone https://github.com/khabbazan/goodreads.git
   cd tests/load/
   ```

2. Open the locustfile.py file.
Modify the GraphQL queries in the GraphQLUser class to match the queries you want to test. You can add or remove fields as needed.
Start the Locust load test by running the following command in your terminal:
    ```bash
    locust -f locustfile.py
    ```

3. Open your web browser and navigate to http://localhost:8089 to access the Locust web UI.

4. Configure the load test parameters in the web UI, including the number of users to simulate, the spawn rate, and the target GraphQL API endpoint.

5. Start the load test using the web UI, and monitor the results and performance metrics in real-time.


## Reporting and Analysis

Locust provides detailed statistics and metrics during and after the load test. You can analyze the results to identify performance bottlenecks and issues.

## Contributing

Feel free to contribute to this project by opening issues or pull requests if you have any improvements, suggestions, or bug fixes.

## Acknowledgments

- [Locust](https://locust.io/) - An open-source load testing tool.
- [GraphQL](https://graphql.org/) - A query language for APIs.

## Author

- [Alireza Khabbazan](https://github.com/khabbazan)

