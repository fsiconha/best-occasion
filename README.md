# best-occasion
A Python library for meta-recommendation and dynamic model selection, designed to serve the right recommendation algorithm for the right occasion.

## Local development

- Install dependencies with `poetry install`.

- Start a local Qdrant instance (requires Docker):
	```bash
	docker run -p 6333:6333 -p 6334:6334 qdrant/qdrant
	```
- Export the vector-store endpoint and launch the API with Uvicorn:
	```bash
	export BEST_OCCASION_VECTOR_STORE_URL="http://127.0.0.1:6333"
	poetry run uvicorn best_occasion.api.app:create_app --factory --reload
	```
- Embeddings are generated via the `sentence-transformers` package using the compact E5 model (`intfloat/e5-small-v2`). Override the model or instruction by setting the `BEST_OCCASION_EMBEDDING_MODEL_NAME` and `BEST_OCCASION_EMBEDDING_INSTRUCTION` environment variables.

- Run `poetry run pytest` to execute the test suite.

### Inspecting collections in Qdrant

- You can visit the built-in UI at `http://127.0.0.1:6333/dashboard` and open *Collections* to inspect `best_occasion_models` and `best_occasion_occasions` (payloads, vectors, filters).
- Alternatively, call the REST API directly:
	```bash
	curl -X POST "http://127.0.0.1:6333/collections/best_occasion_occasions/points/scroll" \
			 -H "Content-Type: application/json" \
			 -d '{"limit": 10, "with_payload": true, "with_vectors": true}'
	```
