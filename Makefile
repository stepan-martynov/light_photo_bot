.PHONY: run
run:
	poetry run python -m src.bot.main

.PHONY: dadata
dadata:
	poetry run python -m src.api.dadata.api_requests
