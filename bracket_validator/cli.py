from bracket_validator.validator import find_wrong_positions, highlight, validate


def main():
    text = input("Введіть строку: ")
    wrong = find_wrong_positions(text)
    if wrong:
        print(highlight(text, wrong))
    validate(text)
    print("Строка валідна")
