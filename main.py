from utils.file_handler import (
    read_sales_data,
    parse_transactions,
    validate_and_filter
)

if __name__ == "__main__":
    raw = read_sales_data("data/sales_data.txt")
    parsed = parse_transactions(raw)
    final, invalid, summary = validate_and_filter(
        parsed,
        region="North",
        min_amount=1000
    )

    print(summary)
