ASDF_VERSION := v0.20.0

ensure-asdf:
	@if ! command -v asdf >/dev/null 2>&1; then \
		echo "asdf is not installed. Installing asdf..."; \
		wget "https://github.com/asdf-vm/asdf/releases/download/$(ASDF_VERSION)/asdf-$(ASDF_VERSION)-linux-amd64.tar.gz"; \
		tar -xzf asdf-$(ASDF_VERSION)-linux-amd64.tar.gz; \
		mv ./asdf ~/.local/bin/; \
		rm asdf-$(ASDF_VERSION)-linux-amd64.tar.gz; \
	else \
		echo "asdf is already installed."; \
	fi

ensure-python: ensure-asdf
	asdf plugin add python
	asdf install python

ensure-uv: ensure-python
	asdf plugin add uv
	asdf install uv

install-pre-commit:
	uv run pre-commit install

pre-commit:
	uv run pre-commit run --all-files

install: ensure-uv
	uv sync

ruff-format:
	uv run ruff format .

ruff-format-check:
	uv run ruff format --check .

ruff-check:
	uv run ruff check .

ruff-fix:
	uv run ruff check --fix .

clean-venv:
	@rm -rf .venv

dev: clean-venv install install-pre-commit
prod: clean-venv install
style: ruff-fix ruff-format
checks: ruff-check ruff-format-check
