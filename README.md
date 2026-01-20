# Sales Analytics System

A Python-based sales analytics application that processes raw sales data, performs business analysis, enriches data using an external API, and generates a comprehensive text report.

## Project Structure

sales-analytics-system/
├── README.md
├── main.py
├── utils/
│   ├── file_handler.py
│   ├── data_processor.py
│   └── api_handler.py
├── data/
│   └── sales_data.txt
├── output/
│   ├── enriched_sales_data.txt
│   └── sales_report.txt
├── requirements.txt

## Features

* Read and parse raw sales data from file
* Validate and filter transactions
* Perform sales analysis:

  * Total revenue
  * Region-wise sales
  * Top selling products
  * Customer analysis
  * Daily sales trend
  * Peak sales day
  * Low performing products
* Fetch product data from DummyJSON API
* Enrich sales data with API information
* Save enriched data to file
* Generate a comprehensive formatted sales report
* End-to-end execution via `main.py`

## Prerequisites

* Python 3.8 or higher
* Internet connection (for API integration)

## Installation

1. Clone the repository:

```bash
git clone https://github.com/madh6van/sales-analytics-system.git
cd sales-analytics-system
```

2. Install required dependencies:

```bash
pip install -r requirements.txt
```

## How to Run

Run the main application using:

```bash
python main.py
```

## Output Files

After successful execution, the following files are generated:

* `data/enriched_sales_data.txt`
  → Sales data enriched with API product information

* `output/sales_report.txt`
  → Detailed sales analytics report with all required sections


## Notes

* Ensure `sales_data.txt` is present in the `data/` folder
* Do not modify folder names or file paths
* The repository must remain public until evaluation is completed

## Author

Madhavan
