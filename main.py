from expression_engine import Tokenizer, Validator

if __name__ == "__main__":
    expr = input()
    tokens = Tokenizer.tokenize(expr)
    Validator(tokens).validate()
