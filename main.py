# main.py

from utils.file_handler import read_and_clean_sales_data

if __name__ == "__main__":
    file_path = "data/sales_data.txt"
    cleaned_data = read_and_clean_sales_data(file_path)
