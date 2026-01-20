from utils.file_handler import (
    read_sales_data,
    parse_transactions,
    validate_and_filter
)

from utils.data_processor import (
    calculate_total_revenue,
    region_wise_sales,
    top_selling_products,
    customer_analysis,
    daily_sales_trend,
    find_peak_sales_day,
    low_performing_products
)

from utils.api_handler import (
    fetch_all_products,
    create_product_mapping,
    enrich_sales_data,
    save_enriched_data
)

if __name__ == "__main__":

    # =====================
    # Q2: FILE HANDLING
    # =====================
    raw = read_sales_data("data/sales_data.txt")
    parsed = parse_transactions(raw)
    final_transactions, invalid_count, summary = validate_and_filter(
        parsed,
        region="North",
        min_amount=1000
    )

    print("\nQ2 SUMMARY")
    print(summary)

    # =====================
    # Q3: DATA PROCESSING
    # =====================
    print("\nTOTAL REVENUE")
    print(calculate_total_revenue(final_transactions))

    print("\nREGION WISE SALES")
    print(region_wise_sales(final_transactions))

    print("\nTOP SELLING PRODUCTS")
    print(top_selling_products(final_transactions))

    print("\nCUSTOMER ANALYSIS")
    print(customer_analysis(final_transactions))

    print("\nDAILY SALES TREND")
    print(daily_sales_trend(final_transactions))

    print("\nPEAK SALES DAY")
    print(find_peak_sales_day(final_transactions))

    print("\nLOW PERFORMING PRODUCTS")
    print(low_performing_products(final_transactions))

    # =====================
    # Q4: API INTEGRATION
    # =====================
    print("\nFETCHING PRODUCTS FROM API...")
    api_products = fetch_all_products()

    product_mapping = create_product_mapping(api_products)

    enriched_transactions = enrich_sales_data(
        final_transactions,
        product_mapping
    )

    save_enriched_data(enriched_transactions)

    print("\nQ4 COMPLETED: Enriched sales data saved")
