tag=dockertown

regular_packages=dockertown
test_packages=dockertown_tests
cover_packages=$(test_packages),$(regular_packages)

CIRCLE_NODE_INDEX ?= 0
CIRCLE_NODE_TOTAL ?= 1

out=out
coverage_dir=$(out)/coverage
tr=$(out)/test-results
xunit_output=$(tr)/nose-$(CIRCLE_NODE_INDEX)-xunit.xml


parallel=--processes=8 --process-timeout=1000 --process-restartworker
coverage=--cover-html --cover-html-dir=$(coverage_dir) --cover-tests --with-coverage --cover-package=$(cover_packages)

xunitmp=--with-xunitmp --xunitmp-file=$(xunit_output)
extra=--rednose --immediate


# Code formatting

black:
	black --target-version py37 src tests

isort:
	isort src

format: black isort


# Release code

bump-upload:
	$(MAKE) bump
	$(MAKE) upload

bump:
	bumpversion patch

upload:
	git push --tags
	git push
	rm -f dist/*
	rm -rf src/*.egg-info
	python3 setup.py sdist
	twine upload --skip-existing --verbose dist/*







# OLD stuff

_clean:
	coverage erase
	rm -rf $(out) $(coverage_dir) $(tr)

_test:
	./tests/run_tests.sh


_coverage-combine:
	coverage combine


_build:
	docker build -t $(tag) .

_build-no-cache:
	docker build --no-cache -t $(tag) .


_test-docker: build
	docker run -it $(tag) make test


_run:
	mkdir -p out-docker
	docker run -it -v $(PWD)/out-docker:/out $(tag) dt-pc-demo


_run-with-mounted-src:
	mkdir -p out-docker
	docker run -it -v $(PWD)/src:/dockertown/src:ro -v $(PWD)/out-docker:/out $(tag) dt-pc-demo


_coverage-report:
	coverage html  -d $(coverage_dir)

_docs:
	sphinx-build src $(out)/docs
