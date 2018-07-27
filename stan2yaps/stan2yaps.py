'''
 * Copyright 2018 IBM Corporation
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
'''

import sys
from antlr4 import *
from parser.stanLexer import stanLexer
from parser.stanParser import stanParser

def stream2parsetree(stream):
    lexer = stanLexer(stream)
    stream = CommonTokenStream(lexer)
    parser = stanParser(stream)
    tree = parser.program()
    return tree

def parsetree2astpy(tree):
    return tree # XXX TODO XXX
    # stan2astpy = Stan2Astpy()
    # walker = ParseTreeWalker()
    # walker.walk(stan2astpy, tree)
    # return tree.ir

def stan2astpy(stream):
    tree = stream2parsetree(stream)
    astpy = parsetree2astpy(tree)
    return astpy

def stan2astpyFile(filename):
    stream = FileStream(filename)
    return stan2astpy(stream)

def stan2astpyStr(str):
    stream = InputStream(str)
    return stan2astpy(stream)

def do_compile(code_string = None, code_file = None):
    if not (code_string or code_file) or (code_string and code_file):
        assert False, "Either string or file but not both must be provided."
    if code_string:
        ast_ = stan2astpyStr(code_string)
    else:
        ast_ = stan2astpyFile(code_file)
    return ast_

def main(argv):
    if (len(argv) > 1):
        return stan2astpyFile(argv[1])


if __name__ == '__main__':
    ast_ = main(sys.argv)
    # co = compile(ast_, "<ast>", 'exec')
    # eval(co)
    print(ast_)
