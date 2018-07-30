all: yaps/stanLexer.py yaps/stanParser.py

yaps/stanLexer.py yaps/stanParser.py: yaps/stan.g4
	antlr4 -Dlanguage=Python3 yaps/stan.g4

test:
	python stan2yaps.py tests/good/slicstan.stan

clean:
	-rm -f	yaps/stan.tokens yaps/stanLexer.tokens \
		yaps/stanLexer.py yaps/stanParser.py \
		yaps/stanListener.py \
		yaps/stan.interp yaps/stanLexer.interp
	-rm -rf __pycache__ yaps/__pycache__

cleanall: clean
	-rm -f *~ */*~
