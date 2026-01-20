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

def read_sales_data(filename):
    """
    Reads sales data from file handling encoding issues
    Returns: list of raw transaction lines (strings)
    """
    encodings = ['utf-8', 'latin-1', 'cp1252']
    lines = None

    for enc in encodings:
        try:
            with open(filename, 'r', encoding=enc) as file:
                lines = file.readlines()
            break
        except UnicodeDecodeError:
            continue
        except FileNotFoundError:
            print(f"Error: File '{filename}' not found.")
            return []

    if not lines:
        print("Error: Unable to read file with supported encodings.")
        return []

    # Remove header and empty lines
    data_lines = []
    for line in lines[1:]:
        if line.strip():
            data_lines.append(line.strip())

    return data_lines

def parse_transactions(raw_lines):
    """
    Parses raw lines into clean list of dictionaries
    """
    transactions = []

    for line in raw_lines:
        parts = line.split('|')

        if len(parts) != 8:
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

        try:
            product_name = product_name.replace(',', '')
            quantity = int(quantity.replace(',', ''))
            unit_price = float(unit_price.replace(',', ''))
        except ValueError:
            continue

        transactions.append({
            'TransactionID': transaction_id,
            'Date': date,
            'ProductID': product_id,
            'ProductName': product_name,
            'Quantity': quantity,
            'UnitPrice': unit_price,
            'CustomerID': customer_id,
            'Region': region
        })

    return transactions

def validate_and_filter(transactions, region=None, min_amount=None, max_amount=None):
    """
    Validates transactions and applies optional filters
    """
    total_input = len(transactions)
    invalid_count = 0
    valid_transactions = []

    for tx in transactions:
        if (
            tx['Quantity'] <= 0 or
            tx['UnitPrice'] <= 0 or
            not tx['TransactionID'].startswith('T') or
            not tx['ProductID'].startswith('P') or
            not tx['CustomerID'].startswith('C')
        ):
            invalid_count += 1
            continue

        valid_transactions.append(tx)

    # Display available regions
    regions = sorted(set(tx['Region'] for tx in valid_transactions))
    print(f"Available regions: {regions}")

    # Display transaction amount range
    amounts = [tx['Quantity'] * tx['UnitPrice'] for tx in valid_transactions]
    if amounts:
        print(f"Transaction amount range: {min(amounts)} - {max(amounts)}")

    filtered_by_region = 0
    filtered_by_amount = 0

    filtered = valid_transactions

    if region:
        before = len(filtered)
        filtered = [tx for tx in filtered if tx['Region'] == region]
        filtered_by_region = before - len(filtered)
        print(f"Records after region filter: {len(filtered)}")

    if min_amount is not None or max_amount is not None:
        before = len(filtered)
        result = []
        for tx in filtered:
            amount = tx['Quantity'] * tx['UnitPrice']
            if min_amount is not None and amount < min_amount:
                continue
            if max_amount is not None and amount > max_amount:
                continue
            result.append(tx)
        filtered = result
        filtered_by_amount = before - len(filtered)
        print(f"Records after amount filter: {len(filtered)}")

    summary = {
        'total_input': total_input,
        'invalid': invalid_count,
        'filtered_by_region': filtered_by_region,
        'filtered_by_amount': filtered_by_amount,
        'final_count': len(filtered)
    }

    return filtered, invalid_count, summary
