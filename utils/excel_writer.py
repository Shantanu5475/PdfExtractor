import pandas as pd


def save_to_excel(tables, output_path):
    with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
        for i, df in enumerate(tables):
            sheet_name = f"Table_{i+1}"
            df.to_excel(writer, sheet_name=sheet_name, index=False)
