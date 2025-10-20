# best-occasion
A Python library for meta-recommendation and dynamic model selection, designed to serve the right recommendation algorithm for the right occasion.

## Local development

- Install dependencies with `poetry install`.
- The vector store uses Qdrant. For fast iteration the API defaults to an in-memory Qdrant instance; provide `BEST_OCCASION_VECTOR_STORE_URL` to connect to a persistent server (for example, a local Docker container).
- Embeddings are generated via the `sentence-transformers` package using the compact E5 model (`intfloat/e5-small-v2`). Override the model or instruction by setting the `BEST_OCCASION_EMBEDDING_MODEL_NAME` and `BEST_OCCASION_EMBEDDING_INSTRUCTION` environment variables.
- Run `poetry run pytest` to execute the test suite.
