# Variables de entorno

# Modulo por defecto (se puede sobreescribir: make test MODULE=coverage_pruebas)
MODULE ?= unit

# Lista de actividades disponibles
MODULES = unit 2e2 integration
# Flags comunes para pytest (puedes ampliarlas)
PYTEST_FLAGS ?= -q -v
PY_WARNINGS  ?= ignore::DeprecationWarning

# Lint (modo "relajado" por defecto para desarrollo)
LINT_MAX_LINE ?= 88
LINT_IGNORE   ?= E501,W391,W293
# Ignora F401 en reexport del __init__ y E402 solo en archivos de tests
LINT_PER_FILE ?= Actividades/mocking_objetos/models/__init__.py:F401,Actividades/*/tests/*.py:E402

# Terraform
TERRAFORM_DIR ?= infra/terraform

# Audit CLI
AUDIT_HOST ?= google.com
AUDIT_PORT ?= 443
AUDIT_FORMAT ?= console
AUDIT_OUTPUT ?=

# Ayuda

.PHONY: help
help: ## Mostrar ayuda
	@grep -E '^[a-zA-Z0-9_-]+:.*?## ' $(MAKEFILE_LIST) | awk -F':|##' '{printf "  %-20s %s\n", $$1, $$3}'

# Instalar dependencias

.PHONY: install ## Instalar dependencias
install:
	@echo "Instalando dependencias..."
	pip install -r requirements.txt
	@if [ -f requirements-dev.txt ]; then \
		echo "Instalando dependencias de desarrollo..."; \
		pip install -r requirements-dev.txt; \
	fi

# Lint / Formato (una sola diana)

.PHONY: lint
lint: ## Formatea (ruff), ordena imports (ruff I), autofix y pasa flake8 relajado
	@echo "Formateando con Ruff..."
	ruff format src/audit_cli tests
	@echo "Ordenando imports (Ruff rule I)..."
	ruff check src/audit_cli --select I --fix
	@echo "Autofix de reglas con Ruff (whitespace, etc.)..."
	ruff check src/audit_cli --fix
	@echo "Lint con flake8 (relajado: ignora $(LINT_IGNORE); ancho $(LINT_MAX_LINE))..."
	flake8 src/audit_cli \
	    --max-line-length=$(LINT_MAX_LINE) \
	    --extend-ignore=$(LINT_IGNORE) \
	    --per-file-ignores="$(LINT_PER_FILE)"
	@echo "Lint OK"

# Terraform Lint / Formato

.PHONY: lint-terraform validate-iac
lint-terraform: validate-iac ## Formatea y valida código Terraform

validate-iac: ## Valida y formatea código Terraform (requiere terraform instalado)
	@echo "Validando configuracion de Terraform"
	@cd $(TERRAFORM_DIR) && terraform validate
	@echo "Formateando codigo Terraform"
	@cd $(TERRAFORM_DIR) && terraform fmt -recursive
	@echo "Verificando formato de Terraform"
	@cd $(TERRAFORM_DIR) && terraform fmt -check -recursive
	@echo "Terraform lint OK"

# Audit CLI

.PHONY: run-audit audit-json audit-csv
run-audit: ## Ejecuta auditoría TLS (AUDIT_HOST, AUDIT_PORT, AUDIT_FORMAT, AUDIT_OUTPUT)
	@echo "Ejecutando auditoría TLS en $(AUDIT_HOST):$(AUDIT_PORT)..."
	@if [ -n "$(AUDIT_OUTPUT)" ]; then \
		python3 -m src.audit_cli.main check-tls $(AUDIT_HOST) --port $(AUDIT_PORT) --format $(AUDIT_FORMAT) --output $(AUDIT_OUTPUT); \
		echo "Reporte guardado en: $(AUDIT_OUTPUT)"; \
	else \
		python3 -m src.audit_cli.main check-tls $(AUDIT_HOST) --port $(AUDIT_PORT) --format $(AUDIT_FORMAT); \
	fi

audit-json: ## Genera reporte de auditoría en formato JSON
	@echo "Generando reporte JSON para $(AUDIT_HOST):$(AUDIT_PORT)..."
	python3 -m src.audit_cli.main check-tls $(AUDIT_HOST) --port $(AUDIT_PORT) --format json --output audit_$(AUDIT_HOST)_$(AUDIT_PORT).json
	@echo "Reporte JSON guardado en: audit_$(AUDIT_HOST)_$(AUDIT_PORT).json"

# Test

.PHONY: test test_all
test: ## Ejecuta pytest en la actividad indicada (MODULE)
	@echo "Ejecutando pruebas en tests: $(MODULE)"
	cd tests/$(MODULE) && PYTHONWARNINGS="$(PY_WARNINGS)" pytest . $(PYTEST_FLAGS)

test_all: ## Ejecuta pytest en todas la carpeta tests
	@echo "Ejecutando pruebas en TODA la carpeta tests..."
	@set -e; \
	for module in $(MODULES); do \
	   echo "EJECUTANDO PRUEBAS EN $$module"; \
	   ( cd tests/$$module && PYTHONWARNINGS="$(PY_WARNINGS)" pytest . $(PYTEST_FLAGS) ); \
	done

# Coverage

.PHONY: coverage coverage_individual
coverage: 	## Ejecuta pytest con cobertura unificada 
	@echo "Ejecutando cobertura UNIFICADA en toda la carpeta tests..."
	@coverage erase
	@set -e; \
	for module in $(MODULES); do \
	   echo "COVERAGE RUN en $$module"; \
	   ( cd tests/$$module && PYTHONWARNINGS="$(PY_WARNINGS)" coverage run --source=. -m pytest . $(PYTEST_FLAGS) ); \
	done
	@echo "COVERAGE COMBINADO"
	@coverage combine $$(for a in $(MODULES); do echo tests/$$a/.coverage; done) || true
	@coverage report -m
	@coverage html -d htmlcov

coverage_individual: ## Ejecuta la cobertura para cada (MODULE)
	@echo "Ejecutando cobertura"
	cd tests/$(MODULE) && PYTHONWARNINGS="$(PY_WARNINGS)" pytest --cov=. --cov-report=term-missing --cov-report=html:htmlcov_$(MODULE) . $(PYTEST_FLAGS); 

# Limpiar

.PHONY: clean
clean: ## Elimina archivos temporales, caches, etc.
	@echo "Eliminando archivos de caché y reportes..."
	# caches python/pytest
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	rm -rf .pytest_cache
	# coverage
	rm -rf .coverage htmlcov tests/**/htmlcov_* tests/**/.coverage 2>/dev/null || true
	coverage erase || true
	# terraform
	find $(TERRAFORM_DIR) -name "*.tfstate" -type f -exec rm -f {} + 2>/dev/null || true
	find $(TERRAFORM_DIR) -name "*.tfstate.backup" -type f -exec rm -f {} + 2>/dev/null || true
	find $(TERRAFORM_DIR) -name ".terraform" -type d -exec rm -rf {} + 2>/dev/null || true
	find $(TERRAFORM_DIR) -name ".terraform.lock.hcl" -type f -exec rm -f {} + 2>/dev/null || true
	rm -rf $(TERRAFORM_DIR)/.terraform $(TERRAFORM_DIR)/.terraform.lock.hcl 2>/dev/null || true
	# audit reports
	rm -f audit_*.json audit_*.csv 2>/dev/null || true
	@echo "Limpieza completa."