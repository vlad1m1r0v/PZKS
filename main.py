from expression_engine import Tokenizer, Validator

if __name__ == "__main__":
    expr = "(2*x^2-5*x+7)-(-i)+ (j+1)/0 - 1 + (1*f)*(2 + 7-x)/q + send(-(2*x+7)/A(j, i), 12700.1 ) + 5)"
    it = iter(Tokenizer(expr))
    Validator(it)
