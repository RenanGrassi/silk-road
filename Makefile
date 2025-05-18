.PHONY: run setup-env

ENV_DIR = env
REQUIREMENTS = requirements.txt

run: setup-env
	@echo "Running application..."
	@$(ENV_DIR)/bin/python your_script.py

setup-env:
	@if [ ! -d "$(ENV_DIR)" ]; then \
		echo "Virtual environment not found. Creating..."; \
		python3 -m venv $(ENV_DIR); \
		echo "Installing requirements..."; \
		$(ENV_DIR)/bin/pip install -r $(REQUIREMENTS); \
	else \
		echo "Virtual environment already exists."; \
		echo "Updating requirements..."; \
		$(ENV_DIR)/bin/pip install --upgrade -r $(REQUIREMENTS); \
	fi
	@echo "Environment setup complete."
	@echo "To activate the virtual environment, run: source $(ENV_DIR)/bin/activate"