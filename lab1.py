def get_temp() -> int:
    while True:
        try:
            temp = int(input("Enter temperature in F: "))
            return temp
        except ValueError:
            print("Please enter a valid integer.")


def to_celsius(temp: float) -> float:
    celsius = (temp - 32) * 5 / 9
    return round(celsius, 1)


def main():
    while True:
        temp = get_temp()
        celsius = to_celsius(temp)
        print(f"Celsius: {celsius:.1f}")

        print(f"Temperature in C: {celsius}")

        answer = input("Want to proceed? yes/no: ").strip().lower()

        if answer != "yes":
            break


if __name__ == "__main__":
    main()

