.PHONY: install uninstall test clean build

PYTHON := python3
PIP := pip3
PREFIX := /usr/local
BINDIR := $(PREFIX)/bin
LIBDIR := $(PREFIX)/lib/gemini-scanner

install:
	@echo "Installing Gemini Scanner..."
	@$(PIP) install --user colorama pyperclip
	@mkdir -p $(LIBDIR)
	@cp -r src/* $(LIBDIR)/
	@echo '#!/bin/bash' > $(BINDIR)/gemini
	@echo 'exec $(PYTHON) $(LIBDIR)/gemini_scanner.py "$$@"' >> $(BINDIR)/gemini
	@chmod +x $(BINDIR)/gemini
	@echo "✅ Installation complete! Run 'gemini --help' to get started."

uninstall:
	@echo "Uninstalling Gemini Scanner..."
	@rm -rf $(LIBDIR)
	@rm -f $(BINDIR)/gemini
	@echo "✅ Uninstallation complete!"

test:
	@$(PYTHON) -m pytest tests/

clean:
	@find . -type d -name __pycache__ -exec rm -rf {} +
	@find . -type f -name "*.pyc" -delete
	@rm -rf build/ dist/ *.egg-info/

build:
	@$(PYTHON) setup.py sdist bdist_wheel