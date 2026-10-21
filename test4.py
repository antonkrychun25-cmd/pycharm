import unittest
from unittest.mock import mock_open, patch
from lab4 import analyze_traffic, get_file_chunks, parse_log_entries


class UnitTestCase(unittest.TestCase):
    def setUp(self):
        self.sample_log = (
            '213.109.238.193 - - [07/May/2017:00:08:35 +0300] "GET /index.php HTTP/1.0" 200 440 "-" "Mozilla/5.0"\n'
            '213.109.238.193 - - [07/May/2017:00:08:35 +0300] "POST /login.php HTTP/1.0" 303 - "-" "Mozilla/5.0"\n'
        )

    def test_parse_log_entries(self):
        lines = self.sample_log.strip().splitlines(True)
        results = list(parse_log_entries(lines))
        self.assertEqual(len(results), 2)

        record1, sent1 = results[0]
        self.assertEqual(record1, len(lines[0].encode("utf-8")))
        self.assertEqual(sent1, 440)

        record2, sent2 = results[1]
        self.assertEqual(record2, len(lines[1].encode("utf-8")))
        self.assertEqual(sent2, 0)

    def test_get_file_chunks(self):
        mk_open = mock_open(read_data="1234567890")
        with patch("builtins.open", mk_open):
            with open("dummy.log", "r") as f:
                chunk = list(get_file_chunks(f, buffer_size=3))
                self.assertEqual(chunk, ["123", "456", "789", "0"])

    def test_analyze_traffic(self):
        mk_open = mock_open(read_data=self.sample_log)
        with patch("builtins.open", mk_open):
            accepted, sent = analyze_traffic("dummy.log")
            self.assertEqual(accepted, len(self.sample_log.encode("utf-8")))
            self.assertEqual(sent, 440)


if __name__ == "__main__":
    unittest.main()