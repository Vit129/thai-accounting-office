.PHONY: start test build preview

start: test build

test:
	python3 -m unittest discover -s tests -v

build:
	bash scripts/build.sh

# Plugins have no local web server; preview creates the installable artifact for review.
preview: build
