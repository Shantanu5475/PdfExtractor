import pdfplumber
import pandas as pd
import os

def extract_full_table_from_pdf(pdf_path, output_excel_path):
    all_tables = []

    with pdfplumber.open(pdf_path) as pdf:
        for page_number, page in enumerate(pdf.pages, start=1):
            print(f"Processing page {page_number}")
            # Extract words to handle missing first column (custom logic)
            words = page.extract_words()
            rows = group_words_to_rows(words)
            if rows:
                df = pd.DataFrame(rows)
                df.columns = [f"Column {i+1}" for i in range(len(df.columns))]  # Set generic column names
                df.insert(0, 'Page', page_number)
                all_tables.append(df)

    # Combine and save
    if all_tables:
        final_df = pd.concat(all_tables, ignore_index=True)
        os.makedirs(os.path.dirname(output_excel_path), exist_ok=True)
        final_df.to_excel(output_excel_path, index=False)
        print(f"✅ Extraction complete. Saved to {output_excel_path}")
    else:
        print("❌ No tables extracted.")

def group_words_to_rows(words, y_threshold=3):
    """
    Groups words into rows based on their vertical positions.
    Returns a list of lists, where each sublist is a row.
    """
    rows = []
    words = sorted(words, key=lambda w: w['top'])
    current_row = []
    current_top = None

    for word in words:
        if current_top is None or abs(word['top'] - current_top) <= y_threshold:
            current_row.append(word)
            current_top = word['top']
        else:
            row = [w['text'] for w in sorted(current_row, key=lambda x: x['x0'])]
            rows.append(row)
            current_row = [word]
            current_top = word['top']

    if current_row:
        row = [w['text'] for w in sorted(current_row, key=lambda x: x['x0'])]
        rows.append(row)

    return rows

# Run the code
pdf_path = "sample_pdfs/sample1.pdf"
output_excel_path = "output/out.xlsx"
extract_full_table_from_pdf(pdf_path, output_excel_path)

