from expression_engine import Tokenizer, Validator

if __name__ == "__main__":
    expression = input()
    tokens = Tokenizer.tokenize(expression)
    validation_result = Validator(tokens).validate()
