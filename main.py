from expression_engine import Tokenizer, Validator

if __name__ == "__main__":
    expr = ""
    it = iter(Tokenizer(expr))
    Validator(it)
