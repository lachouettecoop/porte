ASDF_VERSION := v0.20.0

ensure-asdf:
	@if ! command -v asdf >/dev/null 2>&1; then \
		echo "asdf is not installed. Detecting architecture..."; \
		MACHINE="$$(uname -m)"; \
		case "$$MACHINE" in \
			x86_64|amd64) ASDF_ARCH="amd64" ;; \
			i386|i686) ASDF_ARCH="386" ;; \
			aarch64|arm64) ASDF_ARCH="arm64" ;; \
			armv7l|armv6l|arm) echo "No prebuilt asdf $(ASDF_VERSION) archive for 32-bit ARM ($$MACHINE)."; exit 1 ;; \
			*) echo "Unsupported architecture: $$MACHINE"; exit 1 ;; \
		esac; \
		ARCHIVE="asdf-$(ASDF_VERSION)-linux-$$ASDF_ARCH.tar.gz"; \
		echo "Installing asdf for linux-$$ASDF_ARCH..."; \
		wget "https://github.com/asdf-vm/asdf/releases/download/$(ASDF_VERSION)/$$ARCHIVE"; \
		tar -xzf "$$ARCHIVE"; \
		mv ./asdf ~/.local/bin/; \
		rm "$$ARCHIVE"; \
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
