.PHONY:	check
check:
	mypy simphones test --strict
	flake8 simphones test
	pylint simphones test
	pytest simphones test
