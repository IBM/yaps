from yaps.lib import *
import yaps as yaps


N = type_var("N")


@yaps.model
def test(AA: int[5],
         A: matrix(lower=0)[5, 6][6],
         B: matrix[5, 6][6],
         C: matrix[5, 6][6, 7],
         D: matrix(lower=0)[5, 6],
         E: simplex[5]):
    F: simplex(lower=0)[5][5, 6]
    G: simplex[5]
    H: simplex(lower=0)[()]
    I: int(upper=5)[3]
    J: int(upper=5)
    K: int
    L: int[6]
    alpha: real


print(test)
