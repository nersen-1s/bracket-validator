PAIRS = {"(": ")", "[": "]", "<": ">", "{": "}"}
CLOSING = set(PAIRS.values())


def find_wrong_positions(text):
    if not isinstance(text, str):
        raise TypeError("Аргумент повинен бути рядком")

    stack = []
    wrong = []

    for position, char in enumerate(text):
        if char in PAIRS:
            stack.append((char, position))
        elif char in CLOSING:
            if stack and PAIRS[stack[-1][0]] == char:
                stack.pop()
            else:
                wrong.append(position)  # закриваюча без пари

    wrong.extend(position for _, position in stack)  # відкриваючі без пари
    return sorted(wrong)


def highlight(text, positions):
    marks = "".join("^" if i in positions else " " for i in range(len(text)))
    return f"{text}\n{marks.rstrip()}"


def validate(text):
    wrong = find_wrong_positions(text)
    if wrong:
        raise ValueError(f"Дужки незбалансовані на позиціях {wrong}")
