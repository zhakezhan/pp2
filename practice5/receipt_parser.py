import re
import json


def clean_money(value):
    # convert "1 234,56" → 1234.56
    value = value.replace(" ", "").replace(",", ".")
    return float(value)


def parse_receipt(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()

    # extract prices
    prices = re.findall(r'\d+[ ]?\d*,\d+', text)
    prices = [clean_money(p) for p in prices]

    # extract date and time
    datetime_match = re.search(r'\d{2}\.\d{2}\.\d{4}\s\d{2}:\d{2}:\d{2}', text)
    datetime_value = datetime_match.group() if datetime_match else None

    # extract payment method
    payment_match = re.search(r'Банковская карта|Наличные', text)
    payment_method = payment_match.group() if payment_match else None

    # extract receipt total
    total_match = re.search(r'ИТОГО:\s*([\d\s]+,\d+)', text)
    receipt_total = clean_money(total_match.group(1)) if total_match else None

    return {
        "prices": prices,
        "receipt_total": receipt_total,
        "datetime": datetime_value,
        "payment_method": payment_method
    }


if __name__ == "__main__":
    result = parse_receipt("raw.txt")
    print(json.dumps(result, indent=4, ensure_ascii=False))