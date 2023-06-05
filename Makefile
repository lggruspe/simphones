.PHONY:	check
check:
	mypy simphones test tools --strict
	flake8 simphones test tools
	pylint simphones test tools
	pytest simphones test -x

.PHONY:	test
test:
	pytest simphones test -v --cov=simphones
