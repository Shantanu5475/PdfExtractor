import pandas as pd

def detect_tables(page):
    result = []

    # Try to extract tables using PDF's lines (bordered tables)
    tables = page.extract_tables()
    if tables:
        for table in tables:
            if table:  # make sure table isn't None
                df = pd.DataFrame(table)
                result.append(df)
    else:
        # Borderless table fallback using text position clustering
        words = page.extract_words(use_text_flow=True)
        if words:
            lines = group_words_to_rows(words)
            if lines:
                df = pd.DataFrame(lines)
                result.append(df)

    return result

def group_words_to_rows(words):
    """Group words into lines by y-coordinate proximity."""
    rows = []
    threshold = 3  # vertical proximity tolerance in points
    words.sort(key=lambda x: x['top'])  # sort top-down

    current_row = []
    current_top = None

    for word in words:
        if current_top is None or abs(word['top'] - current_top) <= threshold:
            current_row.append(word)
            if current_top is None:
                current_top = word['top']
        else:
            # finalize the current row
            row = [w['text'] for w in sorted(current_row, key=lambda x: x['x0'])]  # left to right
            rows.append(row)
            # start new row
            current_row = [word]
            current_top = word['top']

    # add the last row if exists
    if current_row:
        row = [w['text'] for w in sorted(current_row, key=lambda x: x['x0'])]
        rows.append(row)

    return rows
