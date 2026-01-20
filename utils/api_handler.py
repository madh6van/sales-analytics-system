
# utils/api_handler.py
import requests

BASE_URL = "https://dummyjson.com/products"

def fetch_all_products():
    """
    Fetches all products from DummyJSON API
    Returns list of product dictionaries
    """
    try:
        response = requests.get(f"{BASE_URL}?limit=100", timeout=10)
        response.raise_for_status()
        data = response.json()
        print("✅ Successfully fetched products from API")
        return data.get("products", [])
    except Exception as e:
        print("❌ Failed to fetch products:", e)
        return []


def create_product_mapping(api_products):
    """
    Creates mapping of product ID to product information
    """
    mapping = {}

    for product in api_products:
        pid = product.get("id")
        mapping[pid] = {
            "title": product.get("title"),
            "category": product.get("category"),
            "brand": product.get("brand"),
            "rating": product.get("rating")
        }

    return mapping


def enrich_sales_data(transactions, product_mapping):
    """
    Enriches transaction data using API product mapping
    """
    enriched = []

    for txn in transactions:
        new_txn = txn.copy()
        product_id = txn.get("ProductID", "")

        try:
            numeric_id = int(product_id[1:])  # P101 → 101
        except:
            numeric_id = None

        api_product = product_mapping.get(numeric_id)

        if api_product:
            new_txn["API_Category"] = api_product.get("category")
            new_txn["API_Brand"] = api_product.get("brand")
            new_txn["API_Rating"] = api_product.get("rating")
            new_txn["API_Match"] = True
        else:
            new_txn["API_Category"] = None
            new_txn["API_Brand"] = None
            new_txn["API_Rating"] = None
            new_txn["API_Match"] = False

        enriched.append(new_txn)

    return enriched

def save_enriched_data(enriched_transactions, filename="data/enriched_sales_data.txt"):
    """
    Saves enriched transactions back to file
    """
    headers = [
        "TransactionID", "Date", "ProductID", "ProductName",
        "Quantity", "UnitPrice", "CustomerID", "Region",
        "API_Category", "API_Brand", "API_Rating", "API_Match"
    ]

    with open(filename, "w", encoding="utf-8") as f:
        f.write("|".join(headers) + "\n")

        for txn in enriched_transactions:
            row = []
            for h in headers:
                val = txn.get(h)
                row.append("" if val is None else str(val))
            f.write("|".join(row) + "\n")

    print(f"✅ Enriched data saved to {filename}")
