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
    low_performing_products,
    generate_sales_report
)

from utils.api_handler import (
    fetch_all_products,
    create_product_mapping,
    enrich_sales_data,
    save_enriched_data
)


def main():
    print("=" * 40)
    print("SALES ANALYTICS SYSTEM")
    print("=" * 40)

    try:
        # [1/10] Read file
        print("\n[1/10] Reading sales data...")
        raw = read_sales_data("data/sales_data.txt")
        print(f"✓ Successfully read {len(raw)} transactions")

        # [2/10] Parse
        print("\n[2/10] Parsing and cleaning data...")
        parsed = parse_transactions(raw)
        print(f"✓ Parsed {len(parsed)} records")

        # [3/10] Filter options
        regions = sorted(set(t["Region"] for t in parsed))
        amounts = [t["Quantity"] * t["UnitPrice"] for t in parsed]

        print("\n[3/10] Filter Options Available")
        print(f"Regions: {', '.join(regions)}")
        print(f"Amount Range: ₹{min(amounts):,.0f} - ₹{max(amounts):,.0f}")

        apply_filter = input("\nDo you want to filter data? (y/n): ").strip().lower()

        region = None
        min_amount = None

        if apply_filter == "y":
            region = input("Enter region: ").strip()
            min_amount = float(input("Enter minimum amount: "))

        # [4/10] Validate
        print("\n[4/10] Validating transactions...")
        final_transactions, invalid_count, summary = validate_and_filter(
            parsed,
            region=region,
            min_amount=min_amount
        )
        print(f"✓ Valid: {len(final_transactions)} | Invalid: {invalid_count}")

        # [5/10] Analysis
        print("\n[5/10] Analyzing sales data...")
        calculate_total_revenue(final_transactions)
        region_wise_sales(final_transactions)
        top_selling_products(final_transactions)
        customer_analysis(final_transactions)
        daily_sales_trend(final_transactions)
        find_peak_sales_day(final_transactions)
        low_performing_products(final_transactions)
        print("✓ Analysis complete")

        # [6/10] API fetch
        print("\n[6/10] Fetching product data from API...")
        api_products = fetch_all_products()
        print(f"✓ Fetched {len(api_products)} products")

        # [7/10] Enrich
        print("\n[7/10] Enriching sales data...")
        product_mapping = create_product_mapping(api_products)
        enriched_transactions = enrich_sales_data(
            final_transactions,
            product_mapping
        )
        enriched_count = sum(1 for t in enriched_transactions if t["API_Match"])
        print(f"✓ Enriched {enriched_count}/{len(enriched_transactions)} transactions")

        # [8/10] Save enriched data
        print("\n[8/10] Saving enriched data...")
        save_enriched_data(enriched_transactions)
        print("✓ Saved to data/enriched_sales_data.txt")

        # [9/10] Report
        print("\n[9/10] Generating report...")
        generate_sales_report(final_transactions, enriched_transactions)
        print("✓ Report saved to output/sales_report.txt")

        # [10/10] Done
        print("\n[10/10] Process Complete!")
        print("=" * 40)

    except Exception as e:
        print("\n❌ ERROR")
        print(str(e))
        print("Program terminated safely.")


if __name__ == "__main__":
    main()
