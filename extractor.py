import os
import pdfplumber
from utils.table_detection import detect_tables
from utils.excel_writer import save_to_excel

INPUT_PDF = "sample_pdfs/sample.pdf"
OUTPUT_DIR = "output"

def main():
    INPUT_PDF = "sample_pdfs/sample.pdf"
    OUTPUT_EXCEL = "output/extracted_tables.xlsx"
    all_tables = []

    os.makedirs("output", exist_ok=True)

    with pdfplumber.open(INPUT_PDF) as pdf:
        for i, page in enumerate(pdf.pages):
            try:
                print(f"Processing page {i+1}")
                page_tables = detect_tables(page)
                if page_tables:
                    print(f"✅ Found {len(page_tables)} table(s) on page {i+1}")
                    all_tables.extend(page_tables)  # flattening here
                else:
                    print(f"⚠️ No tables found on page {i+1}")
            except Exception as e:
                print(f"⚠️ Skipping page {i+1} due to error: {e}")

    if all_tables:
        save_to_excel(all_tables, OUTPUT_EXCEL)
        print("✅ Extraction complete.")
    else:
        print("❌ No tables found.")



if __name__ == "__main__":
    main()