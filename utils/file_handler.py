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

    Returns: list of raw lines (strings)

    Expected Output Format:
    ['T001|2024-12-01|P101|Laptop|2|45000|C001|North', ...]

    Requirements:
    - Use 'with' statement
    - Handle different encodings (try 'utf-8', 'latin-1', 'cp1252')
    - Handle FileNotFoundError with appropriate error message
    - Skip the header row
    - Remove empty lines
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

    Returns: list of dictionaries with keys:
    ['TransactionID', 'Date', 'ProductID', 'ProductName',
     'Quantity', 'UnitPrice', 'CustomerID', 'Region']

    Expected Output Format:
    [
        {
            'TransactionID': 'T001',
            'Date': '2024-12-01',
            'ProductID': 'P101',
            'ProductName': 'Laptop',
            'Quantity': 2,           # int type
            'UnitPrice': 45000.0,    # float type
            'CustomerID': 'C001',
            'Region': 'North'
        },
        ...
    ]

    Requirements:
    - Split by pipe delimiter '|'
    - Handle commas within ProductName (remove or replace)
    - Remove commas from numeric fields and convert to proper types
    - Convert Quantity to int
    - Convert UnitPrice to float
    - Skip rows with incorrect number of fields
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

    Parameters:
    - transactions: list of transaction dictionaries
    - region: filter by specific region (optional)
    - min_amount: minimum transaction amount (Quantity * UnitPrice) (optional)
    - max_amount: maximum transaction amount (optional)

    Returns: tuple (valid_transactions, invalid_count, filter_summary)

    Expected Output Format:
    (
        [list of valid filtered transactions],
        5,  # count of invalid transactions
        {
            'total_input': 100,
            'invalid': 5,
            'filtered_by_region': 20,
            'filtered_by_amount': 10,
            'final_count': 65
        }
    )

    Validation Rules:
    - Quantity must be > 0
    - UnitPrice must be > 0
    - All required fields must be present
    - TransactionID must start with 'T'
    - ProductID must start with 'P'
    - CustomerID must start with 'C'

    Filter Display:
    - Print available regions to user before filtering
    - Print transaction amount range (min/max) to user
    - Show count of records after each filter applied
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
