# --------------------------
# DEFAULT
# --------------------------

all: install

# --------------------------
# INSTALL
# --------------------------

install:
	@if [ ! -d ".venv" ]; then \
		uv venv; \
	fi
	@if ls *.whl 1> /dev/null 2>&1; then \
		uv pip install *.whl; \
	elif ls wheels/*.whl 1> /dev/null 2>&1; then \
		uv pip install wheels/*.whl; \
	fi
	uv sync

# --------------------------
# RUN
# --------------------------

run:
	uv run python pac-man.py config.json

debug:
	uv run python -m pdb pac-man.py config.json

# --------------------------
# TEST
# --------------------------

test:
	uv run pytest

test-cov:
	uv run pytest --cov=src --cov-report=term-missing

# --------------------------
# CLEAN
# --------------------------

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".ruff_cache" -exec rm -rf {} +
	find . -type d -name ".coverage" -exec rm -rf {} +
	rm -f .coverage
	rm -rf htmlcov
	rm -rf .coverage.*

# --------------------------
# FCLEAN
# --------------------------

fclean: clean
	rm -rf .venv
	@echo "💣 Virtual environment removed"

# --------------------------
# LINT (Requirement 42 Subject Chapter III.2)
# --------------------------

lint:
	uv run flake8 src pac-man.py
	uv run mypy src pac-man.py --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	uv run flake8 src pac-man.py
	uv run mypy src pac-man.py --strict

# --------------------------
# PHONY
# --------------------------

.PHONY: all install run debug fclean clean lint lint-strict test test-cov