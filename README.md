# PdfExtractor

# PDF Table Extractor 🧾➡️📊

This project extracts tables (both bordered and borderless) from system-generated PDF documents and exports them into an Excel workbook. It uses `pdfplumber` for PDF parsing and `pandas` for data processing.

---

## 📦 Features

- Detects and extracts **bordered** tables using PDF lines
- Fallback support for **borderless** tables using word position clustering
- Exports extracted tables to an Excel file (each table gets its own sheet)
- Handles multiple pages and multiple tables per page
- Simple and modular design

---


## 🚀 How to Run

### 1. Clone the repository


git clone https://github.com/your-username/pdfExtractor.git
cd pdfExtractor

2. Create and activate a virtual environment (optional but recommended)
python -m venv venv

# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate

3. Install dependencies
pip install -r requirements.txt
If requirements.txt is missing, install manually:

pip install pdfplumber pandas openpyxl

4. Add a sample PDF
Place your PDF inside the sample_pdfs/ folder and update the filename in extractor.py if needed.

5. Run the script
python extractor.py

🧠 How it Works

Bordered Tables: Extracted using pdfplumbers built-in table parser based on ruling lines.

Borderless Tables: If no lines exist, it uses custom logic to group text lines based on y-coordinate proximity.

Excel Output: All extracted tables are exported to output/extracted_tables.xlsx, with each table on its own sheet.

🛠 Dependencies

pdfplumber

pandas

openpyxl
