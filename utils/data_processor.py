def calculate_total_revenue(transactions):
    """
    Calculates total revenue from all transactions
    """
    total = 0.0
    for tx in transactions:
        total += tx['Quantity'] * tx['UnitPrice']
    return total

def region_wise_sales(transactions):
    """
    Analyzes sales by region
    """
    region_data = {}
    overall_total = 0.0

    for tx in transactions:
        region = tx['Region']
        amount = tx['Quantity'] * tx['UnitPrice']
        overall_total += amount

        if region not in region_data:
            region_data[region] = {
                'total_sales': 0.0,
                'transaction_count': 0
            }

        region_data[region]['total_sales'] += amount
        region_data[region]['transaction_count'] += 1

    # Calculate percentage
    for region in region_data:
        region_data[region]['percentage'] = round(
            (region_data[region]['total_sales'] / overall_total) * 100, 2
        )

    # Sort by total_sales descending
    sorted_regions = dict(
        sorted(
            region_data.items(),
            key=lambda x: x[1]['total_sales'],
            reverse=True
        )
    )

    return sorted_regions


def top_selling_products(transactions, n=5):
    """
    Finds top n products by total quantity sold
    """
    product_stats = {}

    for tx in transactions:
        product = tx['ProductName']
        qty = tx['Quantity']
        revenue = qty * tx['UnitPrice']

        if product not in product_stats:
            product_stats[product] = {
                'quantity': 0,
                'revenue': 0.0
            }

        product_stats[product]['quantity'] += qty
        product_stats[product]['revenue'] += revenue

    # Convert to list of tuples
    result = [
        (product, data['quantity'], data['revenue'])
        for product, data in product_stats.items()
    ]

    # Sort by quantity sold descending
    result.sort(key=lambda x: x[1], reverse=True)

    return result[:n]


def customer_analysis(transactions):
    """
    Analyzes customer purchase patterns
    """
    customers = {}

    for tx in transactions:
        customer = tx['CustomerID']
        amount = tx['Quantity'] * tx['UnitPrice']
        product = tx['ProductName']

        if customer not in customers:
            customers[customer] = {
                'total_spent': 0.0,
                'purchase_count': 0,
                'products': set()
            }

        customers[customer]['total_spent'] += amount
        customers[customer]['purchase_count'] += 1
        customers[customer]['products'].add(product)

    # Final formatting
    result = {}
    for customer, data in customers.items():
        avg_order_value = round(
            data['total_spent'] / data['purchase_count'], 2
        )

        result[customer] = {
            'total_spent': data['total_spent'],
            'purchase_count': data['purchase_count'],
            'avg_order_value': avg_order_value,
            'products_bought': sorted(list(data['products']))
        }

    # Sort by total_spent descending
    sorted_result = dict(
        sorted(
            result.items(),
            key=lambda x: x[1]['total_spent'],
            reverse=True
        )
    )

    return sorted_result

def daily_sales_trend(transactions):
    daily = {}

    for tx in transactions:
        date = tx["Date"]
        revenue = tx["Quantity"] * tx["UnitPrice"]
        customer = tx["CustomerID"]

        if date not in daily:
            daily[date] = {
                "revenue": 0.0,
                "transaction_count": 0,
                "customers": set()
            }

        daily[date]["revenue"] += revenue
        daily[date]["transaction_count"] += 1
        daily[date]["customers"].add(customer)

    # Format output and sort by date
    result = {}
    for date in sorted(daily.keys()):
        result[date] = {
            "revenue": round(daily[date]["revenue"], 2),
            "transaction_count": daily[date]["transaction_count"],
            "unique_customers": len(daily[date]["customers"])
        }

    return result


def find_peak_sales_day(transactions):
    daily = {}

    for tx in transactions:
        date = tx["Date"]
        revenue = tx["Quantity"] * tx["UnitPrice"]

        if date not in daily:
            daily[date] = {
                "revenue": 0.0,
                "transaction_count": 0
            }

        daily[date]["revenue"] += revenue
        daily[date]["transaction_count"] += 1

    peak_date = max(daily.items(), key=lambda x: x[1]["revenue"])

    return (
        peak_date[0],
        round(peak_date[1]["revenue"], 2),
        peak_date[1]["transaction_count"]
    )


def low_performing_products(transactions, threshold=10):
    products = {}

    for tx in transactions:
        name = tx["ProductName"]
        qty = tx["Quantity"]
        revenue = qty * tx["UnitPrice"]

        if name not in products:
            products[name] = {
                "quantity": 0,
                "revenue": 0.0
            }

        products[name]["quantity"] += qty
        products[name]["revenue"] += revenue

    result = []
    for name, data in products.items():
        if data["quantity"] < threshold:
            result.append(
                (name, data["quantity"], round(data["revenue"], 2))
            )

    result.sort(key=lambda x: x[1])
    return result
