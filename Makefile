.PHONY: install uninstall test clean build

PYTHON := python3
PIP := pip3
PREFIX := /usr/local
BINDIR := $(PREFIX)/bin
LIBDIR := $(PREFIX)/lib/codeprint

install:
	@echo "Installing CodePrint..."
	@$(PIP) install --user colorama pyperclip
	@mkdir -p $(LIBDIR)
	@cp -r src/* $(LIBDIR)/
	@echo '#!/bin/bash' > $(BINDIR)/codeprint
	@echo 'exec $(PYTHON) $(LIBDIR)/codeprint.py "$$@"' >> $(BINDIR)/codeprint
	@chmod +x $(BINDIR)/codeprint
	@echo "✅ Installation complete! Run 'gemini --help' to get started."

uninstall:
	@echo "Uninstalling CodePrint..."
	@rm -rf $(LIBDIR)
	@rm -f $(BINDIR)/codeprint
	@echo "✅ Uninstallation complete!"

test:
	@$(PYTHON) -m pytest tests/

clean:
	@find . -type d -name __pycache__ -exec rm -rf {} +
	@find . -type f -name "*.pyc" -delete
	@rm -rf build/ dist/ *.egg-info/

build:
	@$(PYTHON) setup.py sdist bdist_wheel