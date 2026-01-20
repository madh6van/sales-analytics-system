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
