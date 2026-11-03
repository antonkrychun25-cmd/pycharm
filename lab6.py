import argparse
import random
from abc import ABC, abstractmethod
from faker import Faker

fake = Faker("uk_UA")


class BaseEmployee(ABC):
    """Абстрактний базовий клас робітника."""

    def __init__(self, emp_id: int, first_name: str, last_name: str):
        self.emp_id = emp_id
        self.first_name = first_name
        self.last_name = last_name

    @abstractmethod
    def calculate_salary(self) -> float:
        pass

    @abstractmethod
    def calculate_tax(self) -> float:
        pass


class HourlyWorker(BaseEmployee):
    """Погодинна оплата праці."""

    def __init__(self, emp_id: int, first_name: str, last_name: str, hourly_rate: float, hours_worked: float = 20.8 * 8):
        super().__init__(emp_id, first_name, last_name)
        self.hourly_rate = hourly_rate
        self.hours_worked = hours_worked

    def calculate_salary(self) -> float:
        return self.hours_worked * self.hourly_rate

    def calculate_tax(self) -> float:
        income = self.calculate_salary()
        return income * 0.18 + income * 0.015


class MonthlyWorker(BaseEmployee):
    """Оплата за фіксованою місячною ставкою."""

    def __init__(self, emp_id: int, first_name: str, last_name: str, fixed_salary: float):
        super().__init__(emp_id, first_name, last_name)
        self.fixed_salary = fixed_salary

    def calculate_salary(self) -> float:
        return self.fixed_salary

    def calculate_tax(self) -> float:
        income = self.calculate_salary()
        return income * 0.18 + income * 0.015


class FopWorker(BaseEmployee):
    """Погодинник, оформлений як ФОП."""

    def __init__(self, emp_id: int, first_name: str, last_name: str, hourly_rate: float, tax_group: int = 3, hours_worked: float = 20.8 * 8):
        super().__init__(emp_id, first_name, last_name)
        self.hourly_rate = hourly_rate
        self.tax_group = tax_group
        self.hours_worked = hours_worked

    def calculate_salary(self) -> float:
        base_pay = self.hours_worked * self.hourly_rate
        return base_pay * 1.10

    def calculate_tax(self) -> float:
        income = self.calculate_salary()
        return (income * 0.05) + 1760.0


class PieceworkWorker(BaseEmployee):
    """Самозайнята особа (оплата за рядки коду)."""

    def __init__(self, emp_id: int, first_name: str, last_name: str, code_lines: int, line_price: float):
        super().__init__(emp_id, first_name, last_name)
        self.code_lines = code_lines
        self.line_price = line_price

    def calculate_salary(self) -> float:
        return self.code_lines * self.line_price

    def calculate_tax(self) -> float:
        income = self.calculate_salary()
        return (income * 0.18) + (income * 0.015) + 1760.0


def determine_category_title(person: BaseEmployee) -> str:
    if isinstance(person, HourlyWorker):
        return "Погодинний"
    elif isinstance(person, MonthlyWorker):
        return "Ставка"
    elif isinstance(person, FopWorker):
        return "ФОП"
    elif isinstance(person, PieceworkWorker):
        return "За рядки коду"
    return "Невідомий"


def create_random_staff(quantity: int = 20) -> list[BaseEmployee]:
    staff_list = []
    for num in range(1, quantity + 1):
        category = random.choice(["hourly", "monthly", "fop", "piecework"])
        fname = fake.first_name()
        lname = fake.last_name()

        if category == "hourly":
            worker = HourlyWorker(
                emp_id=num,
                first_name=fname,
                last_name=lname,
                hourly_rate=random.randint(15, 50),
            )
        elif category == "monthly":
            worker = MonthlyWorker(
                emp_id=num,
                first_name=fname,
                last_name=lname,
                fixed_salary=random.randint(2000, 6000),
            )
        elif category == "fop":
            worker = FopWorker(
                emp_id=num,
                first_name=fname,
                last_name=lname,
                hourly_rate=random.randint(20, 60),
                tax_group=random.choice([2, 3]),
            )
        else:
            worker = PieceworkWorker(
                emp_id=num,
                first_name=fname,
                last_name=lname,
                line_price=random.uniform(0.5, 2.5),
                code_lines=random.randint(1000, 4000),
            )
        staff_list.append(worker)
    return staff_list


def extract_sorting_tuple(person: BaseEmployee):
    return (-person.calculate_salary(), person.last_name)


def arrange_staff_by_salary(staff: list[BaseEmployee]) -> list[BaseEmployee]:
    return sorted(staff, key=extract_sorting_tuple)


def render_staff_report(staff: list[BaseEmployee]):
    print("-----------------------------------------------------------------------------------------")
    print("ID | Прізвище та Ім'я          | Дохід      | Податок    | Категорія")
    print("-----------------------------------------------------------------------------------------")

    sum_taxes = 0.0
    for worker in staff:
        income = worker.calculate_salary()
        tax_val = worker.calculate_tax()
        category = determine_category_title(worker)
        sum_taxes += tax_val

        full_name = f"{worker.last_name} {worker.first_name}"
        print(f"{worker.emp_id:<2} | {full_name:<25} | {income:<10.2f} | {tax_val:<10.2f} | {category}")

    print("-----------------------------------------------------------------------------------------")
    print(f"Сумарний податок: {sum_taxes:.2f}\n")


def main():
    cli_parser = argparse.ArgumentParser(description="Обробка даних робітників підприємства")
    cli_parser.add_argument("--min-income", type=float, help="Мінімальна заробітна плата")
    cli_parser.add_argument("--max-tax", type=float, help="Максимальний сумарний податок")
    cli_parser.add_argument("--fop-group", type=int, help="Група ФОП")

    args = cli_parser.parse_args()

    all_staff = create_random_staff(20)
    ordered_staff = arrange_staff_by_salary(all_staff)

    filtered_results = []
    for worker in ordered_staff:
        if args.fop_group is not None:
            if not (isinstance(worker, FopWorker) and worker.tax_group == args.fop_group):
                continue

        if args.min_income is not None:
            if worker.calculate_salary() < args.min_income:
                continue

        if args.max_tax is not None:
            if worker.calculate_tax() > args.max_tax:
                continue

        filtered_results.append(worker)

    render_staff_report(filtered_results)


if __name__ == "__main__":
    main()