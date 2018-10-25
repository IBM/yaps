all: yaps/stanLexer.py yaps/stanParser.py

yaps/stanLexer.py yaps/stanParser.py: yaps/stan.g4
	antlr4 -Dlanguage=Python3 yaps/stan.g4

test:
	nosetests -v tests/stan/test_stan.py .

doc:
	cp README.md docs/source/
	cd docs; make clean html

distrib:
	python setup.py sdist bdist_wheel

upload:
	twine upload dist/*

clean:
	-rm -f	yaps/stan.tokens yaps/stanLexer.tokens \
		yaps/stan.interp yaps/stanLexer.interp
	-rm -rf __pycache__ yaps/__pycache__

cleanall: clean
	-rm -f *~ */*~ */*/*~
	cd docs; make clean
	-rm -rf build/
	-rm -rf dist/
	-rm -rf yaps.egg-info
