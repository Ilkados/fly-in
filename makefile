# --- Variables ---
PYTHON = python3
PIP = pip3
# Set a default map file so 'make run' works automatically
MAP ?= map.txt

.PHONY: install run debug clean lint lint-strict

# Install project dependencies (including the linters)
install:
	$(PIP) install flake8 mypy
	# If you add external libraries later, uncomment the line below:
	# $(PIP) install -r requirements.txt

# Execute the main script
run:
	$(PYTHON) main.py $(MAP)

# Run the main script in debug mode using python's built-in pdb
debug:
	$(PYTHON) -m pdb main.py $(MAP)

# Remove temporary files and caches
clean:
	rm -rf __pycache__ .mypy_cache
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	@echo "Cleaned up cache files."

# Standard linting as required by the subject
lint:
	flake8 .
	mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

# Strict linting (Strongly recommended by the subject)
lint-strict:
	flake8 .
	mypy . --strict