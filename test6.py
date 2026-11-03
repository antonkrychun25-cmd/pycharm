import unittest
import subprocess
import sys

from lab6 import (
    HourlyWorker,
    MonthlyWorker,
    FopWorker,
    PieceworkWorker,
    create_random_staff,
    arrange_staff_by_salary,
    extract_sorting_tuple,
    determine_category_title,
)


class TestEmployeeManagement(unittest.TestCase):

    def setUp(self):
        self.w_hourly = HourlyWorker(
            emp_id=1, first_name="Іван", last_name="Коваленко", hourly_rate=20.0
        )
        self.w_monthly = MonthlyWorker(
            emp_id=2, first_name="Оксана", last_name="Шевченко", fixed_salary=3000.0
        )
        self.w_fop2 = FopWorker(
            emp_id=3, first_name="Андрій", last_name="Бондар", hourly_rate=30.0, tax_group=2
        )
        self.w_fop3 = FopWorker(
            emp_id=4, first_name="Ірина", last_name="Коваль", hourly_rate=40.0, tax_group=3
        )
        self.w_piecework = PieceworkWorker(
            emp_id=5,
            first_name="Максим",
            last_name="Ткач",
            line_price=1.5,
            code_lines=2000,
        )

    def test_create_random_staff_quantity(self):
        staff = create_random_staff(15)
        self.assertEqual(len(staff), 15)

    def test_determine_category_title(self):
        self.assertEqual(determine_category_title(self.w_hourly), "Погодинний")
        self.assertEqual(determine_category_title(self.w_monthly), "Ставка")
        self.assertEqual(determine_category_title(self.w_fop2), "ФОП")
        self.assertEqual(determine_category_title(self.w_piecework), "За рядки коду")

    def test_extract_sorting_tuple(self):
        sort_key = extract_sorting_tuple(self.w_monthly)
        self.assertEqual(sort_key, (-3000.0, "Шевченко"))

    def test_arrange_staff_by_salary(self):
        staff = [self.w_hourly, self.w_monthly, self.w_piecework]
        sorted_list = arrange_staff_by_salary(staff)

        for i in range(len(sorted_list) - 1):
            sal1 = sorted_list[i].calculate_salary()
            sal2 = sorted_list[i + 1].calculate_salary()
            self.assertGreaterEqual(sal1, sal2)

    def test_fop_group_filter(self):
        staff = [self.w_hourly, self.w_fop2, self.w_fop3, self.w_monthly]

        fop2_only = [
            w for w in staff
            if isinstance(w, FopWorker) and w.tax_group == 2
        ]

        self.assertEqual(len(fop2_only), 1)
        self.assertEqual(fop2_only[0].last_name, "Бондар")

    def test_income_filter(self):
        low_hourly_worker = HourlyWorker(
            emp_id=1, first_name="Іван", last_name="Коваленко", hourly_rate=10.0, hours_worked=50
        )
        staff = [self.w_monthly, low_hourly_worker]
        min_limit = 2500.0

        filtered = [
            w for w in staff
            if w.calculate_salary() >= min_limit
        ]

        self.assertEqual(len(filtered), 1)
        self.assertEqual(filtered[0], self.w_monthly)

    def test_cli_subprocess(self):

        ret_code = subprocess.call([
            sys.executable, "lab6.py", "--fop-group", "3"
        ])
        self.assertEqual(ret_code, 0)


if __name__ == "__main__":
    unittest.main()