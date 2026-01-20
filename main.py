from utils.file_handler import (
    read_sales_data,
    parse_transactions,
    validate_and_filter
)

from utils.data_processor import (
    calculate_total_revenue,
    region_wise_sales,
    top_selling_products,
    customer_analysis
)


if __name__ == "__main__":
    # -------- Q2 PIPELINE --------
    raw = read_sales_data("data/sales_data.txt")
    parsed = parse_transactions(raw)
    final_transactions, invalid_count, summary = validate_and_filter(
        parsed,
        region="North",
        min_amount=1000
    )

    print("\nQ2 SUMMARY")
    print(summary)

    # -------- Q3 ANALYSIS --------
    print("\nTOTAL REVENUE")
    print(calculate_total_revenue(final_transactions))

    print("\nREGION WISE SALES")
    print(region_wise_sales(final_transactions))

    print("\nTOP SELLING PRODUCTS")
    print(top_selling_products(final_transactions))

    print("\nCUSTOMER ANALYSIS")
    print(customer_analysis(final_transactions))


from utils.data_processor import (
    daily_sales_trend,
    find_peak_sales_day,
    low_performing_products
)

print("\nDAILY SALES TREND")
print(daily_sales_trend(final_transactions))

print("\nPEAK SALES DAY")
print(find_peak_sales_day(final_transactions))

print("\nLOW PERFORMING PRODUCTS")
print(low_performing_products(final_transactions))
