.PHONY: setup scrape etl test app clean lint notebooks

PYTHON := .venv/bin/python
UV := uv

setup:
	@echo "==> Inicializando entorno virtual con uv..."
	$(UV) venv .venv
	@echo "==> Instalando dependencias del proyecto..."
	$(UV) pip install -e ".[dev]"
	@echo "==> Entorno listo."

scrape:
	@echo "==> Ejecutando scrapers e ingesta de datos..."
	$(PYTHON) -m src.scrapers.run_all

etl:
	@echo "==> Ejecutando pipeline ETL analítico..."
	$(PYTHON) -m src.etl.build_analytical_mart

test:
	@echo "==> Ejecutando suite de pruebas unitarias..."
	$(PYTHON) -m pytest tests/ -v

app:
	@echo "==> Lanzando aplicación Streamlit..."
	$(PYTHON) -m streamlit run app/Home.py

lint:
	@echo "==> Ejecutando linter ruff..."
	$(PYTHON) -m ruff check src/ tests/ app/

clean:
	@echo "==> Limpiando archivos temporales y cachés..."
	rm -rf __pycache__ .pytest_cache .ruff_cache htmlcov .coverage
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
