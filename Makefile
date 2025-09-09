.PHONY: create-all compress-all clean clean-gzip

SHELL := /bin/bash

create-all:
	bash scripts/create-all.sh

compress-all:
	bash scripts/compress-all.sh

clean:
	find datasets -type f -name '*.csv' -print -delete || true

clean-gzip:
	find datasets -type f -name '*.csv.gz' -print -delete || true


