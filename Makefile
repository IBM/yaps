all: yaps/stanLexer.py yaps/stanParser.py

yaps/stanLexer.py yaps/stanParser.py: yaps/stan.g4
	antlr4 -Dlanguage=Python3 yaps/stan.g4

test:
	nosetests -v tests/run_tests.py

doc:
	cp README.md docs/source/
	cd docs; make html


clean:
	-rm -f	yaps/stan.tokens yaps/stanLexer.tokens \
		yaps/stanLexer.py yaps/stanParser.py \
		yaps/stanListener.py \
		yaps/stan.interp yaps/stanLexer.interp
	-rm -rf __pycache__ yaps/__pycache__
	cd docs; make clean

cleanall: clean
	-rm -f *~ */*~ */*/*~
