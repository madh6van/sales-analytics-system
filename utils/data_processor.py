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


from datetime import datetime
from collections import defaultdict


def generate_sales_report(transactions, enriched_transactions, output_file="output/sales_report.txt"):
    with open(output_file, "w", encoding="utf-8") as f:

        # 1. HEADER
        f.write("SALES ANALYTICS REPORT\n")
        f.write("=" * 40 + "\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Records Processed: {len(transactions)}\n")
        f.write("=" * 40 + "\n\n")

        # 2. OVERALL SUMMARY
        total_revenue = calculate_total_revenue(transactions)
        total_txns = len(transactions)
        avg_order = total_revenue / total_txns if total_txns else 0

        dates = [t["Date"] for t in transactions]
        f.write("OVERALL SUMMARY\n")
        f.write("-" * 40 + "\n")
        f.write(f"Total Revenue: ₹{total_revenue:,.2f}\n")
        f.write(f"Total Transactions: {total_txns}\n")
        f.write(f"Average Order Value: ₹{avg_order:,.2f}\n")
        f.write(f"Date Range: {min(dates)} to {max(dates)}\n\n")

        # 3. REGION-WISE PERFORMANCE
        regions = region_wise_sales(transactions)
        f.write("REGION-WISE PERFORMANCE\n")
        f.write("-" * 40 + "\n")
        f.write(f"{'Region':<10}{'Sales':>15}{'% Total':>12}{'Txns':>10}\n")

        for r, s in regions.items():
            f.write(
                f"{r:<10}₹{s['total_sales']:>14,.2f}"
                f"{s['percentage']:>11.2f}%"
                f"{s['transaction_count']:>10}\n"
            )
        f.write("\n")

        # 4. TOP 5 PRODUCTS
        top_products = top_selling_products(transactions, n=5)
        f.write("TOP 5 PRODUCTS\n")
        f.write("-" * 40 + "\n")
        f.write(f"{'Rank':<6}{'Product':<15}{'Qty':>8}{'Revenue':>12}\n")

        for i, (p, q, r) in enumerate(top_products, 1):
            f.write(f"{i:<6}{p:<15}{q:>8}₹{r:>11,.2f}\n")
        f.write("\n")

        # 5. TOP 5 CUSTOMERS
        customers = customer_analysis(transactions)
        f.write("TOP 5 CUSTOMERS\n")
        f.write("-" * 40 + "\n")
        f.write(f"{'Rank':<6}{'Customer':<12}{'Spent':>12}{'Orders':>10}\n")

        for i, (c, d) in enumerate(list(customers.items())[:5], 1):
            f.write(
                f"{i:<6}{c:<12}₹{d['total_spent']:>11,.2f}{d['purchase_count']:>10}\n"
            )
        f.write("\n")

        # 6. DAILY SALES TREND
        daily = daily_sales_trend(transactions)
        f.write("DAILY SALES TREND\n")
        f.write("-" * 40 + "\n")
        f.write(f"{'Date':<12}{'Revenue':>12}{'Txns':>8}{'Customers':>12}\n")

        for d, s in daily.items():
            f.write(
                f"{d:<12}₹{s['revenue']:>11,.2f}"
                f"{s['transaction_count']:>8}"
                f"{s['unique_customers']:>12}\n"
            )
        f.write("\n")

        # 7. PRODUCT PERFORMANCE
        peak = find_peak_sales_day(transactions)
        low = low_performing_products(transactions)

        f.write("PRODUCT PERFORMANCE ANALYSIS\n")
        f.write("-" * 40 + "\n")
        f.write(f"Best Selling Day: {peak[0]} (₹{peak[1]:,.2f}, {peak[2]} txns)\n")

        if low:
            f.write("Low Performing Products:\n")
            for p, q, r in low:
                f.write(f" - {p}: {q} units, ₹{r:,.2f}\n")
        else:
            f.write("No low performing products.\n")
        f.write("\n")

        # 8. API ENRICHMENT SUMMARY
        matched = [t for t in enriched_transactions if t.get("API_Match")]
        failed = [t for t in enriched_transactions if not t.get("API_Match")]
        rate = (len(matched) / len(enriched_transactions) * 100) if enriched_transactions else 0

        f.write("API ENRICHMENT SUMMARY\n")
        f.write("-" * 40 + "\n")
        f.write(f"Total Products Enriched: {len(matched)}\n")
        f.write(f"Success Rate: {rate:.2f}%\n")

        if failed:
            f.write("Products Not Enriched:\n")
            for t in failed:
                f.write(f" - {t['ProductID']}\n")

    print(f"✅ Sales report generated at {output_file}")
