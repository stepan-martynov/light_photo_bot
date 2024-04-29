.PHONY: run
run:
	poetry run python -m src.bot.main

.PHONY: dadata
dadata:
	poetry run python -m src.api.dadata.api_requests

.PHONY: yadisk
yadisk:
	poetry run python -m src.api.ya_disk.api_requests
