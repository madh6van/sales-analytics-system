def read_and_clean_sales_data(file_path):
    total_records = 0
    invalid_records = 0
    valid_records = []

    with open(file_path, mode="r", encoding="latin-1", errors="replace") as file:
        lines = file.readlines()

    data_lines = lines[1:]  # skip header

    for line in data_lines:
        if not line.strip():
            continue

        total_records += 1
        parts = line.strip().split("|")

        if len(parts) != 8:
            invalid_records += 1
            continue

        (
            transaction_id,
            date,
            product_id,
            product_name,
            quantity,
            unit_price,
            customer_id,
            region
        ) = parts

        if not transaction_id.startswith("T"):
            invalid_records += 1
            continue

        if not customer_id.strip() or not region.strip():
            invalid_records += 1
            continue

        try:
            product_name = product_name.replace(",", "")
            quantity = int(quantity.replace(",", ""))
            unit_price = float(unit_price.replace(",", ""))

            if quantity <= 0 or unit_price < 0:
                invalid_records += 1
                continue

        except ValueError:
            invalid_records += 1
            continue

        valid_records.append({
            "TransactionID": transaction_id,
            "Date": date,
            "ProductID": product_id,
            "ProductName": product_name,
            "Quantity": quantity,
            "UnitPrice": unit_price,
            "CustomerID": customer_id,
            "Region": region
        })

    print(f"Total records parsed: {total_records}")
    print(f"Invalid records removed: {invalid_records}")
    print(f"Valid records after cleaning: {len(valid_records)}")

    return valid_records
