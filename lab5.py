def validate_brackets(s):
    pairs = {')': '(', '}': '{', ']': '[', '>': '<'}
    opening = set(pairs.values())
    closing = set(pairs.keys())

    stack = []
    invalid_positions = set()

    for i, char in enumerate(s):
        if char in opening:
            stack.append((char, i))
        elif char in closing:
            if not stack:
                invalid_positions.add(i)
            else:
                top_char, top_i = stack.pop()
                if top_char != pairs[char]:

                    invalid_positions.add(top_i)
                    invalid_positions.add(i)


    while stack:
        _, open_i = stack.pop()
        invalid_positions.add(open_i)

    sorted_invalid = sorted(list(invalid_positions))
    return len(sorted_invalid) == 0, sorted_invalid


def process_string(s):
    is_valid, invalid_positions = validate_brackets(s)

    if is_valid:
        return "Строка валідна"

    pos_str = ", ".join(str(p) for p in invalid_positions)

    pointers = []
    for i in range(len(s)):
        if i in invalid_positions:
            pointers.append("^")
        else:
            pointers.append(" ")
    visual_pointer = "".join(pointers)

    raise ValueError(f"Дужки незбалансовані на позиціях {pos_str}\n{s}\n{visual_pointer}")


def main():
    try:
        user_input = input("Введіть строку: ")
        result = process_string(user_input)
        print(result)
    except ValueError as e:
        print(e)


if __name__ == "__main__":
    main()