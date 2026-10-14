from decimal import Decimal, ROUND_HALF_UP


def get_positive_decimal(prompt: str) -> Decimal:
    while True:
        try:
            value = Decimal(input(prompt).replace(",", "."))
            if value <= 0:
                print("Значення має бути більше 0!")
                continue
            return value
        except Exception:
            print("Будь ласка, вводьте тільки коректні числа!")


def get_deposit_parameters() -> tuple[Decimal, Decimal, int]:
    initial_deposit = get_positive_decimal("Введіть початкову суму депозиту: ")
    annual_rate = get_positive_decimal(
        "Введіть річну відсоткову ставку (наприклад, 0.12 для 12%): "
    )
    deposit_term_months = 24
    return initial_deposit, annual_rate, deposit_term_months


def calculate_monthly_interest(
    current_balance: Decimal, annual_rate: Decimal
) -> Decimal:
    monthly_interest = (current_balance * annual_rate) / Decimal("12")
    return monthly_interest.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def main():
    initial_deposit, annual_rate, deposit_term_months = get_deposit_parameters()

    current_balance = initial_deposit
    print("\n--- Помісячна розбивка депозиту ---")

    for month in range(1, deposit_term_months + 1):
        monthly_profit = calculate_monthly_interest(
            current_balance, annual_rate
        )
        current_balance += monthly_profit
        print(
            f"Місяць: {month:2d} | Прибуток: {monthly_profit:8.2f} грн | "
            f"Баланс: {current_balance:10.2f} грн"
        )

    total_profit = current_balance - initial_deposit
    print("\n--- Підсумок ---")
    print(f"Початкова сума: {initial_deposit:.2f} грн")
    print(f"Загальний прибуток: {total_profit:.2f} грн")
    print(
        f"Підсумкова сума через {deposit_term_months} місяців: {current_balance:.2f} грн"
    )


if __name__ == "__main__":
    main()