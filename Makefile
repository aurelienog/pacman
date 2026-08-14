# ==============================================================================
#  🟡 PAC-MAN ARCADE CLONE (42 SCHOOL SUBJECT v1.5)
# ==============================================================================

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
# CLEAN
# --------------------------

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	rm -rf build dist *.spec

# --------------------------
# FCLEAN
# --------------------------

fclean: clean
	rm -rf .venv
	@echo "💣 Virtual environment removed"

# --------------------------
# LINT
# --------------------------

lint:
	uv run flake8 src/. pac-man.py
	uv run mypy src/. pac-man.py --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	uv run flake8 src/. pac-man.py
	uv run mypy src/. pac-man.py --strict

# --------------------------
# PACKAGE / BUILD
# --------------------------

build: package

package:
	@echo "🚀 Building standalone executable with PyInstaller..."
	uv run pyinstaller --noconfirm --onefile --windowed \
		--add-data "assets:assets" \
		--name "pacman-linux" \
		pac-man.py
	@echo "📦 Creating ZIP release archive for Itch.io..."
	@rm -rf dist/release dist/pacman-linux.zip
	@mkdir -p dist/release
	@cp dist/pacman-linux dist/release/
	@cp config.json dist/release/
	@cp highscores.json dist/release/
	@cp README.md dist/release/
	@cd dist/release && zip -r ../pacman-linux.zip .
	@echo "✅ Build complete! Archive ready at dist/pacman-linux.zip"

# --------------------------
# PHONY
# --------------------------

.PHONY: all install run debug fclean clean lint lint-strict build package