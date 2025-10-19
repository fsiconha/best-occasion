# best-occasion
A Python library for meta-recommendation and dynamic model selection, designed to serve the right recommendation algorithm for the right occasion.

## Local development

- Install dependencies with `poetry install`.
- The vector store uses Qdrant. For fast iteration the API defaults to an in-memory Qdrant instance; provide `BEST_OCCASION_VECTOR_STORE_URL` to connect to a persistent server (for example, a local Docker container).
- Run `poetry run pytest` to execute the test suite.
