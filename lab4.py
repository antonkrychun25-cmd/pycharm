import re


def get_file_chunks(stream, buffer_size=4096):
    while True:
        data = stream.read(buffer_size)
        if not data:
            break
        yield data


def parse_log_entries(log_file):
    status_bytes_regex = re.compile(r'"\s+(\d{3})\s+(\d+|-)')
    for entry in log_file:
        raw_size = len(entry.encode("utf-8")) if isinstance(entry, str) else len(entry)

        text_entry = entry if isinstance(entry, str) else entry.decode("utf-8", errors="ignore")
        match_obj = status_bytes_regex.search(text_entry)

        if match_obj:
            sent_str = match_obj.group(2)
            out_bytes = int(sent_str) if sent_str.isdigit() else 0
        else:
            out_bytes = 0

        yield raw_size, out_bytes


def analyze_traffic(path_to_log):
    sum_received = 0
    sum_sent = 0

    with open(path_to_log, "r", encoding="utf-8", errors="ignore") as file_stream:
        # Рахуємо вхідний і вихідний трафік за один цикл
        for read_bytes, sent_bytes in parse_log_entries(file_stream):
            sum_received += read_bytes
            sum_sent += sent_bytes

    return sum_received, sum_sent


if __name__ == "__main__":
    target_log = "2017_05_07_nginx.txt"
    try:
        accepted_bytes, transferred_bytes = analyze_traffic(target_log)
        print(f"Accepted: {accepted_bytes} bytes")
        print(f"Sent: {transferred_bytes} bytes")
    except FileNotFoundError:
        print(f"File not found: {target_log}")