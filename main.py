from expression_engine import Tokenizer, Validator


def main():
    expression = input()
    tokens = Tokenizer.tokenize(expression)
    is_valid = Validator.validate(tokens)
    if not is_valid:
        return


if __name__ == "__main__":
    main()
