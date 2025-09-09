.PHONY: help all create-all compress-all clean clean-gzip
help:
	@echo "Available targets:"
	@echo "  make all         - Alias for make create-all"
	@echo "  make create-all   - Generate all datasets"
	@echo "  make compress-all - Compress all datasets (.csv -> .csv.gz)"
	@echo "  make clean        - Delete all CSV datasets"
	@echo "  make clean-gzip   - Delete all compressed CSV datasets (.csv.gz)"

all: create-all


SHELL := /bin/bash

create-all:
	bash scripts/create-all.sh

compress-all:
	bash scripts/compress-all.sh

clean:
	find datasets -type f -name '*.csv' -print -delete || true

clean-gzip:
	find datasets -type f -name '*.csv.gz' -print -delete || true


