import doctest
import sys


def reverse_words(src_text: str) -> str:
    """
    >>> reverse_words("abcd")
    'dcba'
    >>> reverse_words("abcd efgh")
    'dcba hgfe'
    >>> reverse_words("")
    ''
    >>> reverse_words("a1bcd efg!h")
    'd1cba hgf!e'
    >>> reverse_words(123)
    Traceback (most recent call last):
        ...
    TypeError: Переданий аргумент повинен бути строкою (str).
    """
    if not isinstance(src_text, str):
        raise TypeError("Переданий аргумент повинен бути строкою (str).")

    if not src_text.isascii():
        raise ValueError("Текст повинен містити тільки ASCII символи.")

    def reverse_token(token: str) -> str:
        letters_stack = [ch for ch in token if ch.isalpha()]
        formatted_chars = []

        for ch in token:
            if ch.isalpha():
                formatted_chars.append(letters_stack.pop())
            else:
                formatted_chars.append(ch)

        return "".join(formatted_chars)

    tokens = src_text.split(" ")
    processed_tokens = [reverse_token(item) for item in tokens]

    return " ".join(processed_tokens)


def start_cli():
    print("Введіть 'exit' або 'quit' для виходу.\n")

    while True:
        try:
            raw_input = input("Введіть текст: ")

            if raw_input.strip().lower() in ("exit", "quit"):
                print("Завершення роботи.")
                break

            output = reverse_words(raw_input)
            print(f"Результат: {output}\n")

        except ValueError as val_err:
            print(f"Помилка введення: {val_err}\n")
        except KeyboardInterrupt:
            print("\nПрограму примусово завершено.")
            break
        except Exception as err:
            print(f"Виникла непередбачена помилка: {err}\n")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        print("Запуск doctest...")
        failed_cnt, total_cnt = doctest.testmod()
        print(
            f"Тестування завершено: {total_cnt - failed_cnt}/{total_cnt} тестів пройдено успішно."
        )
    else:
        failed_cnt, _ = doctest.testmod()
        if failed_cnt == 0:
            start_cli()
        else:
            print("Виявлено помилки у функціоналі! Запуск зупинено.")