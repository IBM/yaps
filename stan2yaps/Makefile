all: parser/stanLexer.py parser/stanParser.py

parser/stanLexer.py parser/stanParser.py: parser/stan.g4
	antlr4 -Dlanguage=Python3 parser/stan.g4

test:
	python stan2yaps.py tests/good/coin.stan

clean:
	-rm -f	parser/stan.tokens parser/stanLexer.tokens \
		parser/stanLexer.py parser/stanParser.py \
		parser/stanListener.py \
		parser/stan.interp parser/stanLexer.interp
	-rm -rf __pycache__ parser/__pycache__

cleanall: clean
	-rm -f *~ */*~
